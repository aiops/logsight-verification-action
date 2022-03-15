import os
from github import Github

def create_verification_report(verification_result, baseline_tag, compare_tag):
    report = f"""
## Report

[Detailed online report]({verification_result['link']})

Baseline tag: {baseline_tag}
Compare tag: {compare_tag}
Result
+ Deployment failure risk 🔴: {verification_result['risk']}%
Overview
- Total log count: {verification_result['totalLogCount']}
- Baseline log count: {verification_result['baselineLogCount']}
- Compare log count: {verification_result['candidateLogCount']}
- Change percentage: {verification_result['candidateChangePercentage']}%
- Added states total: {verification_result['addedStatesTotalCount']} ({verification_result['addedStatesFaultPercentage']}% Fault 🔴, {verification_result['addedStatesReportPercentage']}% Report)
- Deleted states total: {verification_result['deletedStatesTotalCount']} ({verification_result['deletedStatesFaultPercentage']}% Fault 🔴, {verification_result['deletedStatesReportPercentage']}% Report)
- Frequency change states: {verification_result['frequencyChangeTotalCount']} ({verification_result['frequencyChangeFaultPercentage']}% Fault 🔴, {verification_result['frequencyChangeReportPercentage']}% Report)
- Recurring states total: {verification_result['recurringStatesTotalCount']} ({verification_result['recurringStatesFaultPercentage']}% Fault 🔴, {verification_result['recurringStatesReportPercentage']}% Report)
    """
    return report


def create_github_issue(verification_report):
    # extracting all the input from environments
    title = "Log verification report " + os.environ['INPUT_BASELINE_TAG'] + " : " + os.environ['INPUT_BASELINE_TAG']
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