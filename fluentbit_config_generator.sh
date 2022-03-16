#!/bin/bash

inputName=$1
fileLocation=$2
matchPattern=$3
applicationId=$4
tag=$5
message=$6
host=$7
port=$8
logsightUsername=$9
logsightPassword=${10}


echo "[INPUT]
    Name $inputName
    Path $fileLocation
    multiline.parser  docker, cri
    DB /tail_docker.db
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
    tls On
    uri /api/v1/logs/singles
    Format json
    json_date_format iso8601
    json_date_key timestamp"