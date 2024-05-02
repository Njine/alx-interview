#!/usr/bin/python3
'''Script for parsing HTTP request logs and reporting statistics.'''

import re


# Function to extract the status code and file size from a log line
def extract_log_info(line):
    '''Extracts the status code and file size from a log line.'''
    # Define the regex pattern to match the expected log line format
    pattern = (
        r'\s*(?P<ip>\S+)\s*',  # IP address
        r'\s*\[(?P<date>[^\]]+)\]\s*',  # Date and time
        r'\s*"[^"]+"\s*',  # HTTP request
        r'\s*(?P<status_code>\d{3})\s*',  # Status code
        r'\s*(?P<file_size>\d+)\s*',  # File size
    )

    # Match the log line against the pattern
    full_pattern = '{}-{}{}{}{}$'.format(*pattern)
    match = re.fullmatch(full_pattern, line)

    # Return None if the line doesn't match the expected format
    if not match:
        return None

    # Return the status code and file size
    return {
        'status_code': match.group('status_code'),
        'file_size': int(match.group('file_size')),
    }


# Function to print accumulated statistics
def print_statistics(total_file_size, status_code_counts):
    '''Prints the total file size and counts for each status code.'''
    print(f'File size: {total_file_size}', flush=True)
    # Print the counts for each valid status code in ascending order
    for status_code in sorted(status_code_counts):
        count = status_code_counts[status_code]
        if count > 0:  # Only print non-zero status code counts
            print(f'{status_code}: {count}', flush=True)


# Function to update metrics based on log line information
def update_metrics(log_info, total_file_size, status_code_counts):
    '''Updates total file size and status code counts based on the log line.'''
    # If the extracted log information is invalid, return the current total
    if log_info is None:
        return total_file_size

    # Add to the total file size
    total_file_size += log_info['file_size']

    # Increment the count for the given status code
    status_code = log_info['status_code']
    if status_code in status_code_counts:
        status_code_counts[status_code] += 1

    return total_file_size


# Main function to process stdin and compute metrics
def run_log_parser():
    '''Processes standard input and computes statistics every 10 lines.'''
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
            # Read a line from standard input
            line = input().strip()
            if not line:  # If it's an empty line, stop reading
                break

            # Extract the relevant log information and update the metrics
            log_info = extract_log_info(line)
            total_file_size = update_metrics(log_info, total_file_size, status_code_counts)
            line_count += 1

            # Print statistics every 10 lines
            if line_count % 10 == 0:
                print_statistics(total_file_size, status_code_counts)

    except (KeyboardInterrupt, EOFError):
        # Print final statistics on keyboard interruption or EOF
        print_statistics(total_file_size, status_code_counts)


# If this script is being run directly, execute the main function
if __name__ == '__main__':
    run_log_parser()
