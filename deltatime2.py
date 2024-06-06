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

def process_file(input_file, highdelta_time, quiet, offset, pretty):
    lasttime = 0
    highdelta = 0
    totlines = 0
    highmark = 0
    highmark_linenum = 0
    if offset < 1 or offset > 2:
        offset = 1
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            totlines += 1
            original_line = line.strip()
            timestamp_match = extract_datetimes(line)
            if timestamp_match:
                timestamp_str = timestamp_match[offset-1]
                timestamp = clean_and_convert_datetime(timestamp_str)
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
        if pretty:
            print(f"High water mark ===>  {show_pretty(highmark)} at line number {highmark_linenum} in log {input_file}")
        else:
            print(f"High water mark ===>  {highmark} seconds at line number {highmark_linenum} in log {input_file}")

    return highmark_linenum

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='deltatime v2')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    parser.add_argument('-m', '--mintime', type=int, default=0, help='Time threshold in seconds (Default: 0)')
    parser.add_argument('-o', '--offset', type=int, default=1, help='Timestamp offset index (Default: 1)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Run the program in quiet mode')
    parser.add_argument('-p', '--pretty', action='store_true', help='Display time in pretty format vs seconds')
    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))
    
    for file in expanded_files:
        retcode = process_file(file, args.mintime, args.quiet, args.offset, args.pretty)
    
    exit(retcode)

