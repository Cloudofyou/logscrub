#!/bin/bash

python3 deltatime.py test_file.csv -q
exit_code=$?
echo "Highmark / Starting line -> " $exit_code

python3 logscrub.py test_file.csv $exit_code
