#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse
import glob

datetime_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

def extract_datetimes(line):
    return re.findall(datetime_pattern, line)

def show_pretty(ttime):
    # Calculate hours, minutes, and seconds
    hours = ttime // 3600
    ttime %= 3600
    minutes = ttime // 60
    seconds = ttime % 60

    # Format the string
    result = f"{hours} Hour{'s' if hours != 1 else ''}, {minutes} Minute{'s' if minutes != 1 else ''} and {seconds} Second{'s' if seconds != 1 else ''}"
    return result

def clean_and_convert_datetime(datetime_str):
    # Remove square brackets and replace timezone offset with 'Z'
    cleaned_str = datetime_str.strip('[]').replace('+00:00', 'Z')
    # Convert the cleaned string to a datetime object
    try:
        return datetime.strptime(cleaned_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return datetime.strptime(cleaned_str, '%Y-%m-%d %H:%M:%S')

def process_file(input_file, offset):
    lasttime = 0
    highdelta = 0
    highdelta_time = 0
    totlines = 0
    highmark = 0
    firsttime_flag = 1
    highmark_linenum = 0
    if offset < 1 or offset > 2:
        offset = 1
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            totlines += 1 
            timestamp_match = extract_datetimes(line.strip())
            if timestamp_match:
                timestamp_str = timestamp_match[offset-1]
                timestamp = clean_and_convert_datetime(timestamp_str)
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

    print(f"File:            {input_file}")
    print(f"First timestamp: {first_time}")
    print(f"Event timestamp: {highmark_time}  ({diff_event_first})")
    print(f"Last timestamp:  {last_time}  ({diff_event_last})")
    print(f"Log total time:  {diff_total_time}")

    return highmark_linenum

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='timeline v1')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    parser.add_argument('-o', '--offset', type=int, default=1, help='Timestamp offset index (Default: 1)')
    args = parser.parse_args()


#    parser = argparse.ArgumentParser(description='timeline v1')
#    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
#    parser.add_argument('-o', '--offset', type=int, default=1, help='Timestamp offset index (Default is 1)')
#    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))

    for input_file in expanded_files:
        process_file(input_file, args.offset)

