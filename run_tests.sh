#!/usr/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"

if [ $# -ne 1 ]
then
echo -e "${ERROR_TEXT} Correct Usage: ./run_tests.sh <PORT>"
exit 1
fi

# run tests on the API
cd server
echo -e "${INFO_TEXT} Running Unit Tests [...]"
python3 -m unittest tests/test_schema.py
echo -e "${INFO_TEXT} Running Integration Tests [...]"
python3 -m unittest tests/test_apis.py 
# TEMPORARY FIX
sleep 10
# TEMPORARY FIX
cd ..
echo -e "${INFO_TEXT} Killing Django Proccess on Port $1 [...]"
$(fuser -k $1/tcp)
echo -e "${INFO_TEXT} Tests Run Successfully!"