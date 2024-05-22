#!/usr/bin/env python3

############### deltatime.py

import sys
import re
from datetime import datetime
import openpyxl
from openpyxl import Workbook

def process_file(input_file, highdelta_time):
    # Generate output file name
    base_name = input_file[:20] if len(input_file) > 20 else input_file
    # Read the input file and process lines
    processed_lines = []
    lasttime = 0
    highdelta = 0
    totlines = 0
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            totlines = totlines + 1
            original_line = line.strip()
            modified_line = original_line
            # Check if the line begins with a timestamp and convert it
            timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', original_line)
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                curtime = timestamp.second + timestamp.minute*60 + timestamp.hour*3600
                deltatime = curtime - lasttime
                if (deltatime >= highdelta_time) and (lasttime):
                    highdelta = highdelta + 1
                    print(f"{highdelta:3}) Time delta (in seconds): {deltatime} -- Timestamp: {timestamp} ({totlines})")
                lasttime = curtime
                formatted_timestamp = timestamp.strftime('%b-%d %H:%M:%S')
                modified_line = formatted_timestamp + original_line[len(timestamp_str):]
                # Remove the second timestamp if it exists
                second_timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|\+\d{2}:\d{2}))', modified_line)
                if second_timestamp_match:
                    second_timestamp_str = second_timestamp_match.group(1)
                    modified_line = modified_line.replace(second_timestamp_str, '')
            # Enumerate each line
            enumerated_line = f"{i + 1}. {modified_line}"
            processed_lines.append(enumerated_line)
    print(f"Processed {totlines} total lines and found {highdelta} times crossed {highdelta_time} threshold.")

#    # Create a new Excel workbook and add processed lines
#    wb = Workbook()
#    ws = wb.active
#    ws.title = "Processed Lines"
#    for line in processed_lines:
#        ws.append([line])
#    # Save the workbook to an Excel file
#    wb.save(output_file)
#    # Print completion message
#    print("Processing complete. Output saved to:", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python deltatime.py <input_file> <time_threshold_in_seconds>")
        sys.exit(1)
    input_file = sys.argv[1]
    highdeltatime = int(sys.argv[2])
    # Check if the input file has a valid extension
    if not (input_file.endswith('.txt') or input_file.endswith('.csv')):
        print("Error: Input file must be of type .txt or .csv")
        sys.exit(1)
    process_file(input_file, highdeltatime)
