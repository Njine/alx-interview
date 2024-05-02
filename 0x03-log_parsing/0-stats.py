#!/usr/bin/python3
'''A script for parsing HTTP request logs and reporting statistics.'''

import re


def extract_input(line):
    '''Extract status code & file size from a line of an HTTP request log.'''
    # Define the expected pattern for a valid HTTP request log line
    pattern = (
        r'\s*(?P<ip>\S+)\s*'  # IP Address
        r'\s*\[(?P<date>[^]]+)\]\s*'  # Date
        r'\s*"(?P<request>[^"]*)"\s*'  # HTTP Request
        r'(?P<status_code>\d+)\s*'  # Status code
        r'(?P<file_size>\d+)'  # File size
    )

    match = re.fullmatch(pattern, line)
    if not match:
        return None

    # Extract relevant information from the regex match
    status_code = match.group('status_code')
    file_size = int(match.group('file_size'))

    return {
        'status_code': status_code,
        'file_size': file_size,
    }


def print_statistics(total_file_size, status_codes_count):
    '''Prints the accumulated file size and status code statistics.'''
    print(f'File size: {total_file_size}', flush=True)
    for status_code in sorted(status_codes_count.keys()):
        count = status_codes_count[status_code]
        if count > 0:
            print(f'{status_code}: {count}', flush=True)


def update_metrics(line, total_file_size, status_codes_count):
    '''Updates the metrics from a given HTTP request log line.'''
    data = extract_input(line)
    if data is None:
        return total_file_size

    # Increment status code count if it is one of the tracked ones
    status_code = data['status_code']
    if status_code in status_codes_count:
        status_codes_count[status_code] += 1

    # Add the file size to the total
    total_file_size += data['file_size']
    return total_file_size


def run():
    '''Reads from stdin & prints statistics every 10 lines.'''
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
            line = input()
            total_file_size = update_metrics(line, total_file_size, status_codes_count)
            line_count += 1

            if line_count % 10 == 0:
                print_statistics(total_file_size, status_codes_count)
    except (KeyboardInterrupt, EOFError):
        # On interruption or end of file, print final statistics
        print_statistics(total_file_size, status_codes_count)


if __name__ == '__main__':
    run()
