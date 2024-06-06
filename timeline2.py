#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse
import glob

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

def process_file(input_file, offset):
    if offset < 1 or offset > 2:
        offset = 1
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            timestamp_match = extract_datetimes(line.strip())
            if timestamp_match:
                timestamp_str = timestamp_match[offset-1]
                timestamp = clean_and_convert_datetime(timestamp_str)
                print(f"{timestamp}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='timeline v2')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    parser.add_argument('-o', '--offset', type=int, default=1, help='Timestamp offset index (Default: 1)')
    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))

    for input_file in expanded_files:
        process_file(input_file, args.offset)

