#!/usr/bin/python3
'''A script for parsing HTTP request logs and computing statistics.'''

import re
import sys


# Define a pattern to extract relevant data from each log line
LOG_PATTERN = (
    r'\s*(?P<ip>\S+)\s*'  # IP Address
    r'\s*\[(?P<date>[^]]+)\]\s*'  # Date and time
    r'\s*"[^"]+"\s*'  # HTTP request method and path
    r'(?P<status_code>\d{3})\s*'  # HTTP status code
    r'(?P<file_size>\d+)\s*'  # File size
)

# Function to extract relevant data from a log line
def extract_input(line):
    match = re.fullmatch(LOG_PATTERN, line)
    if match is None:
        return None  # If the line doesn't match, return None
    
    # Extract and return status code and file size as a dictionary
    return {
        'status_code': match.group('status_code'),
        'file_size': int(match.group('file_size'))
    }


# Function to update metrics (file size and status code count) based on a valid log line
def update_metrics(data, total_file_size, status_codes_count):
    if data is None:
        return total_file_size  # Return current total if data extraction failed

    status_code = data['status_code']
    file_size = data['file_size']

    # Update status code count if the code is one of the tracked ones
    if status_code in status_codes_count:
        status_codes_count[status_code] += 1

    # Update the total file size
    return total_file_size + file_size


# Function to print the current statistics
def print_statistics(total_file_size, status_codes_count):
    print(f'File size: {total_file_size}', flush=True)  # Output total file size
    for status_code in sorted(status_codes_count):
        count = status_codes_count[status_code]
        if count > 0:  # Only print non-zero status codes
            print(f'{status_code}: {count}', flush=True)


# Main function to process log lines and print statistics
def run():
    total_file_size = 0
    line_count = 0
    status_codes_count = {
        '200': 0,
        '301': 0,
        '400': 0,
        '401': 0,
        '403': 0,
        '404': 0,
        '405': 0,
        '500': 0,
    }

    try:
        while True:
            line = sys.stdin.readline().strip()  # Read a line from stdin
            if not line:  # Stop if no more input
                break

            # Extract data from the line
            extracted_data = extract_input(line)
            # Update metrics based on the extracted data
            total_file_size = update_metrics(extracted_data, total_file_size, status_codes_count)

            line_count += 1

            # Print statistics every 10 lines
            if line_count % 10 == 0:
                print_statistics(total_file_size, status_codes_count)

    except (KeyboardInterrupt, EOFError):
        # Print final statistics on interruption or end of file
        print_statistics(total_file_size, status_codes_count)


# Run the script
if __name__ == '__main__':
    run()
