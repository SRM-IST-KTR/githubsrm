#!/usr/bin/bash
parallel -j 2 :::: test.config
exit 0