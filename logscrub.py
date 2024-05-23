#!/usr/bin/env python3

import sys
import re
from datetime import datetime
from collections import defaultdict

def show_xids(occurrences):
    for key, count in occurrences.items():
        print(f"{key}: {count} times")

# This function is not currently used but can be used to extract and manipulate the 1st timestamp per line
def process_timestamp(oneline):
    # Detect if the line starts with a datecode
    timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', oneline)
    if timestamp_match:
        timpstamp_str = timestamp_match.group(1)
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
        formatted_timestamp = timestamp.strftime('%b-%d %H:%M:%S') + oneline[len(timestamp_str):]
    else:
        formatted_timestamp = oneline
    return formatted_timestamp

def process_file(inputfile, occurrences):
    pattern = r'(NVSwitch_\d+|GPU_SXM_\d+).*?XID (\d+)'

    with open(inputfile, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            match = re.search(pattern, line)
            if match:
                keyword = match.group(1)
                xid = match.group(2)
                key = f"{keyword}-XID-{xid}"
                occurrences[key] += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: logscrub.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    occurrences = defaultdict(int)
 
    process_file(input_file, occurrences)
    show_xids(occurrences)
