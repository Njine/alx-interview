#!/usr/bin/python3
'''Module for managing lockboxes.
'''


def can_unlock_all(boxes):
    '''Checks if all boxes in a list of boxes can be unlocked given
    that the first box is unlocked.
    '''
    n = len(boxes)
    seen_boxes = {0}
    unseen_boxes = set(boxes[0]) - {0}
    while len(unseen_boxes) > 0:
        box_idx = unseen_boxes.pop()
        if not box_idx or not 0 <= box_idx < n:
            continue
        if box_idx not in seen_boxes:
            unseen_boxes |= set(boxes[box_idx])
            seen_boxes.add(box_idx)
    return n == len(seen_boxes)

