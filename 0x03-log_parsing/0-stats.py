#!/usr/bin/python3
'''A script for parsing HTTP request logs and reporting statistics.'''

import re
import sys


def extract_input(line):
    '''Extracts the status code and file size from a line of HTTP request log.'''
    pattern = (
        r'\s*(?P<ip>\S+)\s*'  # IP Address
        r'\s*\[(?P<date>[^\]]+)\]\s*'  # Date
        r'\s*"(?P<request>[^"]+)"\s*'  # HTTP Request
        r'\s*(?P<status_code>\d+)\s*'  # Status code
        r'\s*(?P<file_size>\d+)'  # File size
    )

    match = re.fullmatch(pattern, line)
    if match is None:
        return None  # Return None if line doesn't match expected pattern

    # Extract and return relevant information
    status_code = match.group('status_code')
    file_size = int(match.group('file_size'))

    return {
        'status_code': status_code,
        'file_size': file_size,
    }


def print_statistics(total_file_size, status_codes_count):
    '''Prints the total file size and status code statistics.'''
    print(f'File size: {total_file_size}', flush=True)
    for status_code in sorted(status_codes_count):
        count = status_codes_count[status_code]
        if count > 0:
            print(f'{status_code}: {count}', flush=True)


def update_metrics(line, total_file_size, status_codes_count):
    '''Updates metrics from a given HTTP request log line.'''
    data = extract_input(line)
    if data is None:
        return total_file_size  # No updates if the line is invalid

    # Increment the status code count and update the total file size
    status_code = data['status_code']
    file_size = data['file_size']

    if status_code in status_codes_count:
        status_codes_count[status_code] += 1

    total_file_size += file_size
    return total_file_size


def run():
    '''Reads from stdin line by line and prints statistics every 10 lines or on interruption.'''
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
            line = sys.stdin.readline().strip()  # Read line from stdin
            if not line:
                break  # Stop if no more lines

            total_file_size = update_metrics(line, total_file_size, status_codes_count)
            line_count += 1

            # Print statistics every 10 lines
            if line_count % 10 == 0:
                print_statistics(total_file_size, status_codes_count)

    except (KeyboardInterrupt, EOFError):
        # On interruption or end of file, print final statistics
        print_statistics(total_file_size, status_codes_count)


if __name__ == '__main__':
    run()
