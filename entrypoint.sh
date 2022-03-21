#!/bin/bash

# Diagnostic output:
echo "Using options $INPUT_USERNAME $INPUT_PASSWORD $INPUT_APPLICATION_ID $INPUT_BASELINE_TAG $INPUT_CANDIDATE_TAG $INPUT_RISK_THRESHOLD  $GITHUB_TOKEN"
ls /
ls /code
pwd
# Runs misspell-fixes:
output=$(python3 /code/main.py --username "$INPUT_USERNAME" --password "$INPUT_PASSWORD" --application_id "$INPUT_APPLICATION_ID" --baseline_tag "$INPUT_BASELINE_TAG" --candidate_tag "$INPUT_CANDIDATE_TAG" --risk_threshold "$INPUT_RISK_THRESHOLD")
status="$?"
#
## Sets the output variable for GitHub Action API:
## See: https://help.github.com/en/articles/development-tools-for-github-action
echo "::set-output name=verification_report::$output"
echo '================================='
echo
#
# Fail the build in case status code is not 0:
if [ "$status" -ne 0 ]; then
  echo 'Failing with output:'
  echo "$output"
  echo "Process failed with the status code: $status"
  exit "$status"
fi