#!/bin/bash

inputName=$1
matchPattern=$2
applicationId=$3
tag=$4
message=$5
host=$6
port=$7
logsightUsername=$8
logsightPassword=$9


echo "[INPUT]
    Name $inputName
[FILTER]
    Name modify
    Match $matchPattern
    Add applicationId $applicationId
    Add tag $tag
    Rename $message message
[OUTPUT]
    Name http
    Host $host
    Port $port
    http_User $logsightUsername
    http_Passwd $logsightPassword
    uri /api/v1/logs/singles
    Format json
    json_date_format iso8601
    json_date_key timestamp"