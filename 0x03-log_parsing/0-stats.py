#!/usr/bin/python3
'''Script for parsing HTTP request logs and computing statistics.'''

import re
import sys


# Regular expression pattern to extract relevant log details
LOG_PATTERN = (
    r'^\s*(?P<ip>\S+)\s*'  # IP Address
    r'\s*\[(?P<date>[^\]]+)\]\s*'  # Date and time
    r'\s*"GET /projects/260 HTTP/1.1"\s*'  # HTTP request
    r'\s*(?P<status_code>\d{3})\s*'  # Status code
    r'\s*(?P<file_size>\d+)\s*$'  # File size
)

# Extracts the status code and file size from a given log line
def extract_log_info(line):
    match = re.fullmatch(LOG_PATTERN, line)
    if not match:
        return None  # If the line doesn't match the pattern, return None
    
    # Extract the status code and file size as a dictionary
    return {
        'status_code': match.group('status_code'),
        'file_size': int(match.group('file_size')),
    }


# Function to print the accumulated statistics
def print_statistics(total_file_size, status_code_counts):
    '''Prints the total file size and counts for each status code.'''
    print(f'File size: {total_file_size}', flush=True)

    for status_code in sorted(status_code_counts):
        count = status_code_counts[status_code]
        if count > 0:  # Print only status codes with a count greater than zero
            print(f'{status_code}: {count}', flush=True)


# Updates metrics based on a valid log line
def update_metrics(log_info, total_file_size, status_code_counts):
    '''Updates total file size and status code counts based on a log line.'''
    if log_info is None:
        return total_file_size  # If the log line is invalid, retain the current total

    status_code = log_info['status_code']
    file_size = log_info['file_size']

    # Update the total file size
    total_file_size += file_size

    # Update the status code counts if it's a valid code
    if status_code in status_code_counts:
        status_code_counts[status_code] += 1

    return total_file_size


# The main function to run the log parser
def process_logs():
    '''Processes stdin line by line and computes statistics.'''
    total_file_size = 0
    line_count = 0
    status_code_counts = {
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
            if not line:
                break  # If there's no more input, exit the loop

            log_info = extract_log_info(line)  # Extract relevant log info
            total_file_size = update_metrics(log_info, total_file_size, status_code_counts)
            line_count += 1

            # Print statistics every 10 lines
            if line_count % 10 == 0:
                print_statistics(total_file_size, status_code_counts)

    except (KeyboardInterrupt, EOFError):
        # Handle keyboard interruptions and EOF gracefully
        print_statistics(total_file_size, status_code_counts)


# Entry point for the script
if __name__ == '__main__':
    process_logs()
