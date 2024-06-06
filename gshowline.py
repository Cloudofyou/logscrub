#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse

def process_file(input_file, viewline):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            if i == viewline-1:
                print(f"{line.strip()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='gshow v1')
    parser.add_argument('input_file', type=str, help='Filename of log file to inspect')
    parser.add_argument('viewline', type=int, nargs='?', default=1, help='Line number of file to view')
    args = parser.parse_args()

    process_file(args.input_file, args.viewline)
