#!/bin/bash

if [ -z $1 ]
then
  echo "Use: runtest.sh <filename>"
  exit 0
fi

for filename in "$@"; do
    python3 deltatime.py $filename -q
    exit_code=$?
    echo "Highmark for " $filename " -> " $exit_code
done
