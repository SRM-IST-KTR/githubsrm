#!/bin/bash
echo "SECRET_KEY=$SECRET_KEY" >> .env
echo "TEST_MONGO_DB=$TEST_MONGO_DB" >> .env
echo "MONGO_DB=$MONGO_DB" >> .env
echo "MONGO_URI=$MONGO_URI" >> .env
parallel -j 2 :::: test-config.txt
exit 0