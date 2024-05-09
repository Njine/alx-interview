#!/usr/bin/env python3
"""UTF-8 Validation Module.
"""


def validUTF8(data):
    """Check if a list of integers represents valid UTF-8 encoding."""
    skip = 0
    n = len(data)
    for i in range(n):
        # Skip checking continuation bytes
        if skip > 0:
            skip -= 1
            continue

        # Check if current byte is valid
        if data[i] < 0 or data[i] > 255:
            return False

        if data[i] <= 127:
            # 1-byte (ASCII)
            continue

        # Determine byte pattern for multi-byte characters
        if data[i] & 0b11100000 == 0b11000000:
            span = 2  # 2-byte sequence
        elif data[i] & 0b11110000 == 0b11100000:
            span = 3  # 3-byte sequence
        elif data[i] & 0b11111000 == 0b11110000:
            span = 4  # 4-byte sequence
        else:
            return False  # Invalid leading byte

        # Ensure there are enough continuation bytes
        if i + span > n:
            return False

        # Check that the continuation bytes are valid
        for j in range(1, span):
            if data[i + j] & 0b11000000 != 0b10000000:
                return False

        skip = span - 1  # Skip checked continuation bytes

    return True  # All checks passed
