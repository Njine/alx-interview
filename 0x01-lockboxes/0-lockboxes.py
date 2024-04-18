#!/usr/bin/python3
'''Module for managing lockboxes.
'''


def canUnlockAll(boxes):
    '''Checks if all boxes in a list of boxes can be unlocked given
    that the first box is unlocked.
    '''
    n = len(boxes)
    seen_boxes = {0}
    keys_to_check = set(boxes[0]) - {0}
    while keys_to_check:
        key = keys_to_check.pop()
        if not 0 <= key < n:
            continue
        seen_boxes.add(key)
        keys_to_check |= set(boxes[key]) - seen_boxes
    return len(seen_boxes) == n
