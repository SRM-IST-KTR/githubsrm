#!/bin/bash
# run tests on the API
cd server
python3 -m unittest tests/test_schema.py 
python3 -m unittest tests/test_apis.py 
cd ..
