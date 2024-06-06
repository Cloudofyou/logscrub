#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse

datetime_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

def extract_datetimes(line):
    return re.findall(datetime_pattern, line)

def clean_and_convert_datetime(datetime_str):
    # Remove square brackets and replace timezone offset with 'Z'
    cleaned_str = datetime_str.strip('[]').replace('+00:00', 'Z')
    # Convert the cleaned string to a datetime object
    try:
        return datetime.strptime(cleaned_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return datetime.strptime(cleaned_str, '%Y-%m-%d %H:%M:%S')

def process_file(input_file, highdelta_time, quiet, offset):
    lasttime = 0
    highdelta = 0
    totlines = 0
    highmark = 0
    highmark_linenum = 0
    if offset < 0 or offset > 3:
        offset = 0
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            totlines += 1
            original_line = line.strip()
            timestamp_match = extract_datetimes(line)
#            timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', original_line)
            if timestamp_match:
                timestamp_str = timestamp_match[offset]
                timestamp = clean_and_convert_datetime(timestamp_str)
#                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                curtime = timestamp.second + timestamp.minute*60 + timestamp.hour*3600
                deltatime = curtime - lasttime
                if (deltatime >= highdelta_time) and (lasttime):
                    if deltatime > highmark:
                        highmark = deltatime
                        highmark_linenum = totlines
                    highdelta += 1
                    if highdelta_time > 0:
                        if not quiet:
                            print(f"{highdelta:3}) Time delta (in seconds): {deltatime} -- Timestamp: {timestamp} ({totlines})")
                lasttime = curtime
                formatted_timestamp = timestamp.strftime('%b-%d %H:%M:%S')
    if not quiet:
        print(f"Processed {totlines} total lines and found {highdelta} times where it crossed {highdelta_time} threshold.")
        print(f"High water mark: {highmark} seconds at line number {highmark_linenum} in log.")

    return highmark_linenum

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='deltatime v1')
    parser.add_argument('input_file', type=str, help='Filename of log file to inspect')
    parser.add_argument('highdeltatime', type=int, nargs='?', default=0, help='Time threshold in seconds (Default: 0)')
    parser.add_argument('offset', type=int, nargs='?', default=0, help='Timestamp offset index (Default: 0)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Run the program in quiet mode')
    args = parser.parse_args()

    retcode = process_file(args.input_file, args.highdeltatime, args.quiet, args.offset)
    exit(retcode)

