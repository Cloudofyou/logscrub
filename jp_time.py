#!/usr/bin/env python3

import re
from datetime import datetime
import os
import glob
import argparse
import sys

datetime_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
human_pattern = r"\[([A-Za-z]{3} [A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2} UTC \d{4})\]"

def extract_datetimes(line, pattern):
    return re.findall(pattern, line)

def clean_and_convert_datetime(datetime_str):
    datetime_str = datetime_str.strip('[]')
    try:
        dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        try:
            dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                dt = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Z %Y')
    return dt.replace(tzinfo=None)

def extract_second_timestamp(line):
    timestamp_match = extract_datetimes(line, datetime_pattern)
    timestamp_match_human = extract_datetimes(line, human_pattern)
    if timestamp_match:
        if timestamp_match_human:
            timestamp_str = timestamp_match_human[0]
        else:
            timestamp_str = timestamp_match[1] if len(timestamp_match) > 1 else timestamp_match[0]
        timestamp = clean_and_convert_datetime(timestamp_str)
        return timestamp, line
    return None, line

def sort_lines_by_timestamp(input_file):
    lines_with_timestamps = []
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            timestamp, line = extract_second_timestamp(line)
            if timestamp:
                lines_with_timestamps.append((timestamp, line))
    sorted_lines = sorted(lines_with_timestamps, key=lambda x: x[0])
    return [line for _, line in sorted_lines]

def save_sorted_lines(input_file, sorted_lines):
    file_dir, file_name = os.path.split(input_file)
    new_file_name = os.path.join(file_dir, f"sorted_{file_name}")
    with open(new_file_name, 'w') as outfile:
        outfile.writelines(sorted_lines)
    return new_file_name

if __name__ == "__main__":
#    if len(sys.argv) != 2:
#        print("Usage: ./delta_jp1.py <filename>")
#        sys.exit(1)
#
#    input_file = sys.argv[1]
    parser = argparse.ArgumentParser(description='jp_time v1')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))
    
    for input_file in expanded_files:
        sorted_lines = sort_lines_by_timestamp(input_file)
        new_file_name = save_sorted_lines(input_file, sorted_lines)
        print(f"Sorted file saved as: {new_file_name}")
