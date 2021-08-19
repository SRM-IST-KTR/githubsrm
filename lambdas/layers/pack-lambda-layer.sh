#!/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"
WORKING_DIR=$(pwd)

if [ $# -ne 1 ]; then
    echo -e "$ERROR_TEXT Correct Usage: ./pack-lambda-layer.sh <Version Number; Example: v1>"
    exit 1
fi
if [ ! -d node_modules ]; then
    echo -e "$ERROR_TEXT node_modules folder not found! Exiting..."
    exit 1
fi
if [ ! -f package.json ]; then
    echo -e "$ERROR_TEXT package.json file not found! Exiting..."
    exit 1
fi
if [ ! -f "$WORKING_DIR/..layers/$1/nodejs" ]; then
    NORMAL_PATH=$(realpath "$WORKING_DIR/../layers")
    echo -e "$INFO_TEXT '$NORMAL_PATH/v1/nodejs' was not found. Creating directory..."
    mkdir -p "$NORMAL_PATH/v1/nodejs"
fi
echo -e "$INFO_TEXT Copying node_modules..."
cp -r node_modules "$WORKING_DIR/../layers/$1/nodejs/node_modules"
echo -e "$INFO_TEXT Copying package.json..."
cp package.json "$WORKING_DIR/../layers/$1/nodejs/package.json"
echo -e "$INFO_TEXT Zipping '$1' lambda layer..."
cd "$WORKING_DIR/../layers/$1"
zip -r "$WORKING_DIR/../layers/$1.zip" "nodejs"
echo -e "$INFO_TEXT Lambda layer '$1' ready to be uploaded!"