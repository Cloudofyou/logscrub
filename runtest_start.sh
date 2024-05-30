#!/bin/bash

if [ -z $1 ]
then
  echo "Use: runtest.sh <filename>"
  exit 0
fi

for filename in "$@"; do
    python3 logscrub.py $filename 
done
