#!/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"

if [ $# -ne 1 ]; then
    echo -e "$ERROR_TEXT Correct Usage: ./test.frontend.sh <PORT>"
    exit 1
fi

echo -e "$INFO_TEXT Installing NPM packages [...]"
cd client
npm install
echo -e "$INFO_TEXT Building Next.js [...]"
npm run build
echo -e "$INFO_TEXT Killing Django Proccess on Port $1 [...]"
fuser -k $1/tcp
echo -e "$INFO_TEXT Tests Run Successfully!"
