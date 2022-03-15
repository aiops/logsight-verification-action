#!/bin/bash

username=$1
password=$2
inputName=$3
applicationId=$4
tag=$5
message=$6
host=$7
port=$8
basicAuthToken=`echo -n $username:$password | base64`
echo "[INPUT]
    Name $inputName
[FILTER]
    Name modify
    Match *
    Add applicationId $applicationId
    Add tag $tag
    Rename $message message
    Add basicAuthToken $basicAuthToken
[OUTPUT]
    Name http
    Host $host
    Port $port
    Format json_lines
    json_date_format iso8601"