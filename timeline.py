#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse
import glob

def process_file(input_file):
    lasttime = 0
    highdelta = 0
    highdelta_time = 0
    totlines = 0
    highmark = 0
    firsttime_flag = 1
    highmark_linenum = 0
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            totlines += 1 
            original_line = line.strip()
            timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', original_line)
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                if (firsttime_flag > 0):
                    firsttime_flag = 0
                    first_time = timestamp
                curtime = timestamp.second + timestamp.minute*60 + timestamp.hour*3600
                deltatime = curtime - lasttime
                if (deltatime >= highdelta_time) and (lasttime):
                    if deltatime > highmark:
                        highmark = deltatime
                        highmark_linenum = totlines
                        highmark_time = timestamp
                    highdelta += 1
                lasttime = curtime
    last_time = timestamp

    diff_event_first = highmark_time - first_time
    diff_event_last = last_time - highmark_time
    diff_total_time = last_time - first_time

    print(f"First timestamp: {first_time}")
    print(f"Event timestamp: {highmark_time}  ({diff_event_first})")
    print(f"Last timestamp:  {last_time}  ({diff_event_last})")
    print(f"Log total time:  {diff_total_time}")

    return highmark_linenum

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='timeline v1')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))

    for input_file in expanded_files:
        process_file(input_file)

