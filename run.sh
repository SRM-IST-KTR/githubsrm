#!/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"

if [ $# -ne 1 ]; then
    echo -e "$ERROR_TEXT Correct Usage: ./run.sh <PORT>"
    exit 1
fi

# run the django server
cd server/
source ./env/bin/activate
cd githubsrm/
echo -e "$INFO_TEXT Server starting on Port $1 [...]"
gunicorn core.wsgi:application --bind 0.0.0.0:$1 --access-logfile - --error-logfile - --reload
