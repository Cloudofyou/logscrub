#!/usr/bin/env python3

import re
from collections import defaultdict
from dataclasses import dataclass
import argparse

@dataclass
class LogErrors:
    devtype: str
    devnum: str
    count: int

def create_errorstruct(counter, logerrors):
    for key, loc_count in counter.items():
        parts = key.split('-', 1)
        loc_logerrors = LogErrors(devtype=parts[0], devnum=parts[1], count=loc_count)
        logerrors.append(loc_logerrors)

def show_device_errors(logerrors):
    print("Device name        Error            Count")
    print("-----------------  ---------------  -----")
    for errors in logerrors:
        print(f"{errors.devtype:12}       {errors.devnum:10}     {errors.count:4}")    

def process_file(inputfile, counter, start_line, end_line):
    pattern = r'\b(NVSwitch_\d+|GPU_SXM_\d+)\b.*?\b(S?X?ID) (\d+)\b'
    line_count = 0
    with open(inputfile, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            line_count += 1
            if (line_count >= start_line) and ((line_count <= end_line) or (end_line == 0)):
               match = re.search(pattern, line)
               if match:
                   key = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                   counter[key] += 1

##def search_file(inputfile, counter, start_line, end_line):
##    pattern = 

def main():
    parser = argparse.ArgumentParser(description='logscrub v1')
    parser.add_argument('input_file', type=str, help='Filename of log file to inspect')
    parser.add_argument('start_line', type=int, nargs='?', default=0, help='Start processing on this line number')
    parser.add_argument('end_line', type=int, nargs='?', default=0, help='End processing on this line number')
    args = parser.parse_args()

    logerrors = []
    counter = defaultdict(int)

    process_file(args.input_file, counter, args.start_line, args.end_line)
    create_errorstruct(counter, logerrors)
    show_device_errors(logerrors)

if __name__ == '__main__':
    main()

