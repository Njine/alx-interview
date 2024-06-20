#!/usr/bin/python3
""" Prime Game Problem """

def sieve(n):
    """ Sieve of Eratosthenes algorithm to find all primes up to n """
    is_prime = [True] * (n + 1)
    p = 2
    while (p * p <= n):
        if (is_prime[p] == True):
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    is_prime[0], is_prime[1] = False, False  # 0 and 1 are not primes
    prime_counts = [0] * (n + 1)
    count = 0
    for i in range(n + 1):
        if is_prime[i]:
            count += 1
        prime_counts[i] = count
    return prime_counts

def isWinner(x, nums):
    """
    Determines the winner in the prime game using
    Eratosthenes prime sieving algorithm
    """
    if x <= 0 or not nums:
        return None
    
    n = max(nums)
    prime_counts = sieve(n)
    
    Ben = 0
    Maria = 0

    for round in range(x):
        prime_count = prime_counts[nums[round]]
        if prime_count % 2 == 0:
            Ben += 1
        else:
            Maria += 1

    if Ben == Maria:
        return None
    return 'Ben' if Ben > Maria else 'Maria'
