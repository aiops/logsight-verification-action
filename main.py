import copy
import time
from datetime import datetime

import logsight.exceptions
from dateutil.tz import tzlocal
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.compare import LogsightCompare
import argparse
from utils import create_verification_report, create_github_issue

SECONDS_SLEEP = 3

# Instantiate the parser
parser = argparse.ArgumentParser(description='Logsight Init')
parser.add_argument('--username', type=str, help='URL of logsight')
parser.add_argument('--password', type=str, help='Basic auth username')
parser.add_argument('--application_id', type=str, help='Application id')
parser.add_argument('--baseline_tag', type=str, help='Baseline tag')
parser.add_argument('--candidate_tag', type=str, help='Compare tag')
parser.add_argument('--risk_threshold', type=int, help='Risk threshold (between 0 and 100)')
args = parser.parse_args()
EMAIL = args.username
PASSWORD = args.password
APPLICATION_ID = args.application_id
BASELINE_TAG = args.baseline_tag
CANDIDATE_TAG = args.candidate_tag
RISK_THRESHOLD = args.risk_threshold

user = LogsightUser(email=EMAIL, password=PASSWORD)

end_stream_log_entry = {'timestamp': datetime.now(tz=tzlocal()).isoformat(), 'message': "End stream."}
g = LogsightLogs(user.token)
r = g.send(APPLICATION_ID, [end_stream_log_entry], tag='end_stream')
time.sleep(SECONDS_SLEEP)
flush_id = g.flush(r['receiptId'])['flushId']
compare = LogsightCompare(user.user_id, user.token)

while True:
    try:
        r = compare.compare(app_id=APPLICATION_ID, baseline_tag=BASELINE_TAG, candidate_tag=CANDIDATE_TAG, flush_id=flush_id)
        break
    except logsight.exceptions.Conflict as conflict:
        time.sleep(SECONDS_SLEEP)
    except Exception as e:
        application_tags = [tag['tag'] for tag in compare.tags(app_id=APPLICATION_ID)]
        if CANDIDATE_TAG not in application_tags and BASELINE_TAG not in application_tags:
            print("Both tags do not exist! We cant perform verification!")
            exit(0)
        if BASELINE_TAG not in application_tags:
            BASELINE_TAG = copy.deepcopy(CANDIDATE_TAG)
        if CANDIDATE_TAG not in application_tags:
            CANDIDATE_TAG = copy.deepcopy(BASELINE_TAG)
        time.sleep(SECONDS_SLEEP)

report = create_verification_report(verification_result=r, baseline_tag=BASELINE_TAG, candidate_tag=CANDIDATE_TAG)
print(report)
if r['risk'] >= RISK_THRESHOLD:
    create_github_issue(report)
    exit(1)
else:
    exit(0)


