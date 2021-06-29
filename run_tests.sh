#!/bin/bash
# run tests on the API
cd server
python3 -m unittest tests/test_apis.py 
# TEMPORARY FIX
sleep 10
# TEMPORARY FIX
cd ..
fuser -k 8000/tcp
