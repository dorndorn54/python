###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

# ================================
# Part B: Golden Eggs
# ================================

import time


# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    # sorts the tuple into a descending list
    sorted_weights = sorted(egg_weights, reverse=True)
    egg_count_total = 0  # number of eggs transported
    # iterate through the various egg_weights
    weight_limit = target_weight
    for eggs in sorted_weights:
        # give the floor value of egg_count
        egg_count = weight_limit // eggs
        egg_count_total += egg_count
        weight_limit -= eggs * egg_count
        if weight_limit == 0:  # max weight reached
            break
    return egg_count_total


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")

    start = time.time()
    print("Actual output:", dp_make_weight(egg_weights, n))
    end = time.time()
    print(end - start)
    print()