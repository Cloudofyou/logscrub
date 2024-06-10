#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse
import glob

datetime_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

def extract_datetimes(line, pattern):
    return re.findall(pattern, line)

def clean_and_convert_datetime(datetime_str):
    # Remove square brackets and replace timezone offset with 'Z'
    cleaned_str = datetime_str.strip('[]').replace('+00:00', 'Z')
    # Convert the cleaned string to a datetime object
    try:
        return datetime.strptime(cleaned_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return datetime.strptime(cleaned_str, '%Y-%m-%d %H:%M:%S')

def process_file(input_file, verbose):
    p_input_file = input_file.split('/')[-1]
    print(f"Input Filename: {p_input_file}")
    output_file_name = p_input_file+".sort"
    print(f"Output Filename: {output_file_name}")
    first_timestamp = True
    with open(output_file_name, 'w') as outfile:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
            for i, line in enumerate(lines):
                timestamp_match = extract_datetimes(line, datetime_pattern)
                if len(timestamp_match) > 1: 
                    timestamp_str = timestamp_match[1]
                    timestamp = clean_and_convert_datetime(timestamp_str)
                    formatted_timestamp = timestamp.strftime('%m-%d-%Y %H:%M:%S')
                    if first_timestamp:
                        previous_timestamp = timestamp 
                        first_timestamp = False
                    delta_timestamp = timestamp - previous_timestamp
                    if (previous_timestamp > timestamp) and verbose:
                        print(f"Reverse timestamp detected at line number {i} - Timestamp delta: {delta_timestamp}")
                    previous_timestamp = timestamp
                    outfile.write(formatted_timestamp+"[ @@@ ]"+line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='sortbytime v1')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show when reverse timestamps are detected to stdout') 
    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))
    
    for input_file in expanded_files:
        process_file(input_file, args.verbose)
    
