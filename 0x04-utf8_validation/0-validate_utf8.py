#!/usr/bin/python3
"""UTF-8 validation module."""


def validUTF8(data):
    """Checks if list of integers are valid UTF-8 encoded bytes."""
    skip = 0
    n = len(data)

    for i in range(n):
        if skip > 0:
            skip -= 1
            continue

        # Check for single-byte ASCII characters (0x00 to 0x7F)
        if data[i] <= 0x7F:
            continue

        # Check for multi-byte UTF-8 sequences
        # 4-byte UTF-8 character (11110xxx)
        if data[i] & 0b11111000 == 0b11110000:
            span = 4
        # 3-byte UTF-8 character (1110xxxx)
        elif data[i] & 0b11110000 == 0b11100000:
            span = 3
        # 2-byte UTF-8 character (110xxxxx)
        elif data[i] & 0b11100000 == 0b11000000:
            span = 2
        # Not a valid UTF-8 start byte
        else:
            return False

        # Check if there's enough data for the multi-byte character
        if i + span > n:
            return False

        # Validate continuation bytes (they should start with 10xxxxxx)
        for j in range(1, span):
            if (data[i + j] & 0b11000000) != 0b10000000:
                return False

        # Skip continuation bytes
        skip = span - 1

    return True
