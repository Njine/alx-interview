#!/usr/bin/python3
'''A script for parsing HTTP request logs and reporting statistics.'''

import re
import sys

# Regular expression pattern to match log format
LOG_PATTERN = (
    r'^\s*(?P<ip>\S+)\s*'  # IP Address
    r'\s*\[(?P<date>[^]]+)\]\s*'  # Date and time
    r'\s*"[^"]+"\s*'  # HTTP Request
    r'\s*(?P<status_code>\d{3})\s*'  # Status code
    r'\s*(?P<file_size>\d+)\s*'  # File size
)

# Function to extract status code and file size from a given line
def extract_input(input_line):
    match = re.fullmatch(LOG_PATTERN, input_line)
    if match is None:
        return None

    return {
        'status_code': match.group('status_code'),
        'file_size': int(match.group('file_size'))
    }

# Function to print statistics
def print_statistics(total_file_size, status_codes_count):
    '''Prints the accumulated statistics of the HTTP request log.'''
    print(f'File size: {total_file_size}', flush=True)
    for status_code in sorted(status_codes_count):
        count = status_codes_count[status_code]
        if count > 0:
            print(f'{status_code}: {count}', flush=True)

# Function to update metrics based on a log line
def update_metrics(line, total_file_size, status_codes_count):
    '''Updates the metrics from a given HTTP request log.'''
    data = extract_input(line)
    if data is None:
        return total_file_size  # Ignore invalid lines

    # Update total file size and status code count if valid data
    status_code = data['status_code']
    file_size = data['file_size']

    if status_code in status_codes_count:
        status_codes_count[status_code] += 1

    return total_file_size + file_size

# Main function to process log lines and print statistics at intervals
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
            line = sys.stdin.readline().strip()  # Read from stdin
            if not line:  # Stop if no more input
                break

            total_file_size = update_metrics(line, total_file_size, status_codes_count)
            line_count += 1

            # Print statistics every 10 lines
            if line_count % 10 == 0:
                print_statistics(total_file_size, status_codes_count)

    except (KeyboardInterrupt, EOFError):
        # Print final statistics upon interruption or end of input
        print_statistics(total_file_size, status_codes_count)


# Entry point of the script
if __name__ == '__main__':
    run()
