#!/bin/bash
parallel -j 2 :::: test-config.txt
exit 0