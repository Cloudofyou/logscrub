#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse
import glob

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    newlines = []
    for line in lines:
        templine = line.split('[ @@@ ]')[1]
        newlines.append(templine)
#        print(f"{line}")
#        print(f"{templine}")
#        input("Press enter")

    return newlines

def extract_datetime(line):
#    datetime_str = line.split('[ @@@ ]')[0]
    cleaned_str = line.strip('[]').replace('+00:00', 'Z')
    try:
        return datetime.strptime(cleaned_str, '%m-%d-%YT%H:%M:%SZ')
    except ValueError:
        return datetime.strptime(cleaned_str, '%m-%d-%Y %H:%M:%S')


#    cleaned_str = datetime_str.strip('[]').replace('+00:00', 'Z')
#    try:
#        return datetime.strptime(cleaned_str, '%Y-%m-%dT%H:%M:%SZ')
#    except ValueError:
#        return datetime.strptime(cleaned_str, '%Y-%m-%d %H:%M:%S')


def sort_lines_by_datetime(lines):
    return sorted(lines, key=extract_datetime)

def write_file(lines, filename):
    with open(filename, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='sortbytime2 v1')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))

    for input_file in expanded_files:
        lines = read_file(input_file)
        sorted_lines = sort_lines_by_datetime(lines)
        output_filename = input_file+".out"
        write_file(sorted_lines, output_filename)

