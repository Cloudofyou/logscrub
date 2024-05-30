#!/usr/bin/env python3

import sys
import re
from datetime import datetime
import argparse

def process_file(input_file, startline, endline):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            if i >= startline and (i <= endline or endline == 0):
                print(f"{i:5} {line}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='gshow v1')
    parser.add_argument('input_file', type=str, help='Filename of log file to inspect')
    parser.add_argument('startline', type=int, nargs='?', default=0, help='Line number of file to start view')
    parser.add_argument('endline', type=int, nargs='?', default=0, help='Line number of file to end view')
    args = parser.parse_args()

    process_file(args.input_file, args.startline, args.endline)
