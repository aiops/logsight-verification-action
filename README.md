<a href="https://logsight.ai/"><img src="https://logsight.ai/assets/img/logol.png" width="150"/></a>

**Your Ally for Intelligent DevOps Pipelines**

logsight.ai infuses deep learning and AI-powered analytics to enable continuous software delivery and proactive troubleshooting


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
if the verification result fails then a GitHub issue will be created.

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