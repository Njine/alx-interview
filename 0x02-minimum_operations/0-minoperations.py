#!/usr/bin/python3
"""Module calculates the fewest number of operations needed to
result in exactly `n` H characters in the file.
"""


def minOperations(n):
    """Calculate the minimum number of operations to reach `n` H characters.
    Operations allowed:
    - Copy All
    - Paste
    """
    if not isinstance(n, int) or n <= 0:
        return 0

    # Initialize variables
    ops_count = 0  # Total operations
    clipboard = 0  # Number of characters in the clipboard
    current = 1    # Initial count of H characters in the file

    # While the desired number of H characters hasn't been reached
    while current < n:
        # If the clipboard is empty, copy all and paste
        if clipboard == 0:
            clipboard = current
            current += clipboard
            ops_count += 2  # Two operations: Copy All, Paste

        # If the remaining amount to reach `n` is divisible by `current`
        elif (n - current) % current == 0:
            clipboard = current
            current += clipboard
            ops_count += 2  # Two operations: Copy All, Paste

        # Otherwise, just paste the clipboard's content
        else:
            current += clipboard
            ops_count += 1  # One operation: Paste

    return ops_count
