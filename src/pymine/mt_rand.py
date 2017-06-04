import sys
import random


def mt_rand(low=0, high=sys.maxsize):
    """Generate a better random value
    """
    return random.randint(low, high)
