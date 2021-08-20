#!/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"
WORKING_DIR=$(pwd)

if [ $# -ne 1 ]; then
    echo -e "$ERROR_TEXT Correct Usage: ./upload-lambda-layer.sh <Version Number; Example: v1>"
    exit 1
fi
if [ ! -f "$1.zip" ]; then
    echo -e "$ERROR_TEXT $1.zip file not found! Exiting..."
    exit 1
fi
echo -e "\e[1;33m Uploading Lambda Layer '$1'... \e[0m"
aws lambda publish-layer-version --layer-name "githubcommunitysrm-$1" --description "Layer $1 by GitHub Community SRM" \
    --license-info "MIT" --zip-file "fileb://$1.zip" \
    --compatible-runtimes nodejs14.x \
    --profile gcsrm
if [ $? -eq 0 ]; then
    echo -e "$INFO_TEXT Lambda Layer '$1' succesfully uploaded!"
else
    echo -e "$ERROR_TEXT AWS Upload Error!"
    exit 1
fi
