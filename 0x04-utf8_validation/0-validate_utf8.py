#!/usr/bin/env python3
"""UTF-8 Validation Module."""


def validUTF8(data):
    """
    Check if a list of integers represents valid UTF-8 encoding.
    Each integer is a byte, so only the 8 least significant bits are considered.
    """
    skip = 0  # To track continuation bytes to skip
    n = len(data)
    
    for i in range(n):
        if skip > 0:
            skip -= 1
            continue
        
        # Check leading byte to determine the type of UTF-8 sequence
        leading_byte = data[i]
        if leading_byte <= 127:
            # ASCII character, single byte
            continue
        
        # Determine the number of bytes in the UTF-8 sequence
        if leading_byte & 0b11100000 == 0b11000000:
            span = 2
        elif leading_byte & 0b11110000 == 0b11100000:
            span = 3
        elif leading_byte & 0b11111000 == 0b11110000:
            span = 4
        else:
            return False  # Invalid leading byte pattern
        
        # Ensure there's enough data for the complete sequence
        if i + span > n:
            return False
        
        # Validate continuation bytes in the UTF-8 sequence
        for j in range(1, span):
            continuation_byte = data[i + j]
            if continuation_byte & 0b11000000 != 0b10000000:
                return False
        
        skip = span - 1  # Mark bytes to skip
    
    return True  # If all checks pass
