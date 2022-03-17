import os
from github import Github

def create_verification_report(verification_result, baseline_tag, compare_tag):
    github_branch = os.environ['GITHUB_REF']
    github_actor = os.environ['GITHUB_ACTOR']
    github_workflow = os.environ['GITHUB_WORKFLOW']
    report = f"""
<a href="https://logsight.ai/"><img src="https://logsight.ai/assets/img/logol.png" width="120"/></a>
<a href="https://docs.logsight.ai/#/">Docs</a>

## Report

### [:page_with_curl: :bar_chart: :link: Detailed online report]({verification_result['link']})

Github actor : {github_actor}
Workflow     : {github_workflow}
Baseline tag : {github_branch} {baseline_tag}
Compare tag  : {github_branch} {compare_tag}

### Deployment risk
### 🔴 {verification_result['risk']}%

### Result Overview

- Total log count       : {verification_result['totalLogCount']}
- Baseline log count    : {verification_result['baselineLogCount']}
- Compare log count     : {verification_result['candidateLogCount']}
- Change percentage     : {verification_result['candidateChangePercentage']}%
- Added states total    : :heavy_plus_sign: {verification_result['addedStatesTotalCount']} (🔴 {verification_result['addedStatesFaultPercentage']}% Fault, :green_circle: {verification_result['addedStatesReportPercentage']}% Report )
- Deleted states total  : {verification_result['deletedStatesTotalCount']} (🔴 {verification_result['deletedStatesFaultPercentage']}% Fault, :green_circle: {verification_result['deletedStatesReportPercentage']}% Report)
- Freq. change states   : {verification_result['frequencyChangeTotalCount']} (🔴 {verification_result['frequencyChangeFaultPercentage']}% Fault, :green_circle: {verification_result['frequencyChangeReportPercentage']}% Report)
- Recurring states total: {verification_result['recurringStatesTotalCount']} (🔴 {verification_result['recurringStatesFaultPercentage']}% Fault, :green_circle: {verification_result['recurringStatesReportPercentage']}% Report)
    """
    return report


def create_github_issue(verification_report):
    # extracting all the input from environments
    title = "Log verification report " + os.environ['INPUT_BASELINE_TAG'][:6] + " : " + os.environ['INPUT_BASELINE_TAG'][:6]
    token = os.environ['INPUT_GITHUB_TOKEN']
    labels = 'log-verification'
    assignees = os.environ['GITHUB_ACTOR']

    # as I said GitHub expects labels and assignees as list but we supplied as string in yaml as list are not supposed in
    # .yaml format
    if labels and labels != '':
        labels = labels.split(',')  # splitting by , to make a list
    else:
        labels = []  # setting empty list if we get labels as '' or None

    if assignees and assignees != '':
        assignees = assignees.split(',')  # splitting by , to make a list
    else:
        assignees = []  # setting empty list if we get labels as '' or None

    g = Github(token)
    # GITHUB_REPOSITORY is the repo name in owner/name format in Github Workflow
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

    issue = repo.create_issue(
        title=title,
        body=verification_report,
        assignees=assignees,
        labels=labels
    )