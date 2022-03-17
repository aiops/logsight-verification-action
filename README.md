<a href="https://logsight.ai/"><img src="https://logsight.ai/assets/img/logol.png" width="150"/></a>

**Your Ally for Intelligent DevOps Pipelines**

logsight.ai infuses deep learning and AI-powered analytics to enable continuous software delivery and proactive troubleshooting

## Stage Verifier Report

###[:page_with_curl: :bar_chart: Detailed online report]({verification_result['link']})

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




# log-verification-action

This action compares logs from a new deployment of a service with the logs from the previous running deployment using
logsight.ai [Stage Verifier.](https://docs.logsight.ai/#/monitor_deployments/stage_verifier)

## Inputs
#### `github_token` 
**Required** Github token needed to create an issue if the quality check fails.
#### `username`
**Required**  Basic auth username.
#### `password`
**Required**  Basic auth password.
#### `application_id`
**Required**  IDs of logsight application.
#### `baseline_tag`
**Required**  Tag that refers to the baseline version (e.g., already running deployment in production.
#### `compare_tag`
**Required**  Tag that refers to the compare version (e.g., the one that you want to check currently).
#### `compare_tag`
**Required**  Tag that refers to the compare version (e.g., the one that you want to check currently).

## Outputs

#### `verification_result`
The verification result is a report as following:
```

[Detailed online report](URL with details fromt the report)

Baseline tag: bcb9b6784d93136d27c4ba30a35618836a68087c
Compare tag: 42f7bf7cc759b5320f1ebd9c200e456ea1d29571
Result
+ Deployment failure risk 🔴: 0%
Overview
- Total log count: 0
- Baseline log count: 0
- Compare log count: 0
- Change percentage: 0.0%
- Added states total: 0 (0.0% Fault 🔴, 0.0% Report)
- Deleted states total: 0 (0.0% Fault 🔴, 0.0% Report)
- Frequency change states: 0 (None% Fault 🔴, None% Report)
- Recurring states total: 0 (0.0% Fault 🔴, 0.0% Report)
```

Read more about the Stage Verifier Output at [logsight.ai docs.](https://docs.logsight.ai/#/monitor_deployments/using_the_rest_api?id=verify)

## Example usage

```
uses: actions/logsight-verification@v1.0
with:
  github_token: {{ secrets.GITHUB_TOKEN }}
  username: admin
  password: mypassword
  application_id: {{ steps.logsight-init.outputs.application-id }}
  baseline_tag: {{github.event.before}}
  compare_tag: {{github.sha}}
  risk_threshold: "50"  
```