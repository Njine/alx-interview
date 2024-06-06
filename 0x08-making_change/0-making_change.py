#!/usr/bin/python3
"""Change making module.
"""


def makeChange(coins, total):
    """Finds the minimum number of coins needed to achieve a given total.

    Args:
        coins (list): The values of the coins available.
        total (int): The target amount to reach.

    Returns:
        int: The minimum number of coins needed to reach the total,
             or -1 if it's not possible.
    """
    if total <= 0:
        return 0

    # Sort coins in descending order to start with the largest denominations
    sorted_coins = sorted(coins, reverse=True)
    rem = total
    coins_count = 0

    for coin in sorted_coins:
        while rem >= coin:
            rem -= coin
            coins_count += 1
        if rem == 0:
            break

    # If loop exits and there is remainder, we cannot meet the total
    if rem > 0:
        return -1

    return coins_count
