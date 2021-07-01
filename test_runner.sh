#!/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"

if [ "$1" = "frontend" ]
then
echo -e "$INFO_TEXT Running Front-end Tests [...]"
parallel -j 2 --ungroup :::: test.frontend.config
exit 0
fi
if [ "$1" = "backend" ]
then
echo -e "$INFO_TEXT Running Back-end Tests [...]"
parallel -j 2 --ungroup :::: test.backend.config
exit 0
fi
echo -e "$ERROR_TEXT Correct Usage: ./test_runner.sh <backend|frontend>"
exit 1