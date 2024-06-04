#!/usr/bin/env python3

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import argparse
import glob

@dataclass
class LogErrors:
    devtype: str
    devnum: str
    count: int

def find_highest_delta_time(inputfile):
    ## Returns the line number of the text file that contains the highest time delta between lines
    highest_deltatime = datetime.min - datetime.min
    highest_deltatime_line = 0
    firsttimehere = True
    with open(inputfile, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            find_timestamp = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', line)
            if find_timestamp:
                # The line contains a timestamp
                timestamp = datetime.strptime(find_timestamp.group(1), '%Y-%m-%dT%H:%M:%SZ')
                if (firsttimehere):
                    firsttimehere = False
                    lasttime = timestamp
                deltatime = timestamp - lasttime
                if (deltatime > highest_deltatime) and (i > 1):
                    highest_deltatime = deltatime
                    highest_deltatime_line = i
                lasttime = timestamp
    return highest_deltatime_line

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
    parser = argparse.ArgumentParser(description='logscrub v2')
    parser.add_argument('-s', '--start', type=int, default=0, help='[Start process on this line]')
    parser.add_argument('-e', '--end', type=int, default=0, help='[End process on this line number]') 
    parser.add_argument('-t', '--toggle', action='store_true', help='Toggle whether to find and start at Event')
    parser.add_argument('filenames', nargs='+', help='Filename/wildcard of log file(s) to inspect')
    args = parser.parse_args()

    expanded_files = []
    for pattern in args.filenames:
        expanded_files.extend(glob.glob(pattern))
    event_line = args.start 

    for file in expanded_files:
        logerrors = []
        counter = defaultdict(int)
        if args.toggle:
            event_line = find_highest_delta_time(file)
        process_file(file, counter, event_line, args.end)
        create_errorstruct(counter, logerrors)
        show_device_errors(logerrors)

if __name__ == '__main__':
    main()

