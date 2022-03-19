import os
from github import Github

def create_verification_report(verification_result, baseline_tag, candidate_tag):
    github_branch = os.environ['GITHUB_REF']
    github_actor = os.environ['GITHUB_ACTOR']
    github_workflow = os.environ['GITHUB_WORKFLOW']
    report = f"""
<a href="https://logsight.ai/"><img src="https://logsight.ai/assets/img/logol.png" width="120"/></a>
<a href="https://docs.logsight.ai/#/">Docs</a>

## Report

| Name       | Value |
| :---        |    :----:   |  
| Github actor      |   {github_actor}     |
| Workflow     |   {github_workflow}  | 
| Baseline branch    |   {github_branch}  | 
| Baseline tag  |   {baseline_tag}  | 
| Candidate branch  |   {github_branch} | 
| Candidate tag  |    {candidate_tag}  | 

#### [:page_with_curl: :bar_chart: Detailed online report :link:]({verification_result['link']})

#### Deployment risk
#### :zap: {verification_result['risk']}%

#### Result Overview

| Name       | Value |
| :---        |    :----:   |  
| Total log count      |   {verification_result['totalLogCount']}     |
| Baseline log count   |   {verification_result['baselineLogCount']}  | 
| Compare log count    |   {verification_result['candidateLogCount']}  | 
| Change from compare to baseline  |   {verification_result['candidateChangePercentage']}%  | 

#### State analysis

| Name       | Total | 🔴 Failed % | :green_circle: Report % |
| :---        |    :----:   |          ---: |          ---: |
| :arrow_right: Added states    |   {verification_result['addedStatesTotalCount']}     | {verification_result['addedStatesFaultPercentage']} |  {verification_result['addedStatesReportPercentage']} |
|  :arrow_left: Deleted states   |   {verification_result['deletedStatesTotalCount']} | {verification_result['deletedStatesFaultPercentage']} |  {verification_result['addedStatesReportPercentage']} |
| :arrow_right_hook: Recurring states |   {verification_result['recurringStatesTotalCount']}  |  {verification_result['recurringStatesFaultPercentage']} |  {verification_result['recurringStatesReportPercentage']}| 
| :arrows_counterclockwise: Freq. change states    |    {verification_result['frequencyChangeTotalCount']}  | :arrow_up: {verification_result['frequencyChangeFaultPercentage']['increase']} :arrow_down: {verification_result['frequencyChangeFaultPercentage']['decrease']} |  :arrow_up: {verification_result['frequencyChangeReportPercentage']['increase']} :arrow_down: {verification_result['frequencyChangeReportPercentage']['decrease']}  |

    """
    return report


def create_github_issue(verification_report):
    # extracting all the input from environments
    title = "Stage Verifier logsight.ai [baseline: " + os.environ['INPUT_BASELINE_TAG'][:6] + " | candidate:" + os.environ['INPUT_CANDIDATE_TAG'][:6] + "]"
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
        labels=labels
    )