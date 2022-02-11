#!/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"
WORKING_DIR=$(pwd)

if [ $# -ne 1 ]; then
    echo -e "$ERROR_TEXT Correct Usage: ./upload-lambda.sh <Version Number; Example: v1>"
    exit 1
fi
if [ ! -d "dist" ]; then
    echo -e "$ERROR_TEXT 'dist' folder not found!"
    echo -e "\e[1;33mDo you want to attempt building the function? (N/y)? \e[0m"
    read INPUT_CHOICE
    case $INPUT_CHOICE in
    Y | y)
        yarn build
        ;;
    *)
        echo -e "$ERROR_TEXT Please build before uploading! Exiting..."
        exit 1
        ;;
    esac
fi
if [ -f "dist-$1.zip" ]; then
    echo -e "$INFO_TEXT Removing old 'dist-$1.zip' archive..."
    rm "dist-$1.zip"
fi
echo -e "$INFO_TEXT Zipping the lambda source code..."
cd dist
zip -r "../dist-$1.zip" .
cd -
echo -e "\e[1;33m Uploading Lambda 'githubcommunitysrm-$1'... \e[0m"
aws lambda update-function-code \
    --function-name "githubcommunitysrm-$1" \
    --zip-file "fileb://dist-$1.zip" --publish \
    --profile gcsrm
if [ $? -eq 0 ]; then
    echo -e "$INFO_TEXT Lambda 'githubcommunitysrm-$1' succesfully uploaded!"
    echo -e "$INFO_TEXT WARNING: Please remember to update the Lambda Layer to the latest version in the AWS Dashboard!"
else
    echo -e "$ERROR_TEXT AWS Upload Error!"
    exit 1
fi
