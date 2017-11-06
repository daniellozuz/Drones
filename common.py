"""Module implementing minor functionalities."""


from collections import namedtuple
from functools import lru_cache
Position = namedtuple('Position', ['x', 'y'])

# TODO implement it as regular function and use caching (sqrt is expensive, only small portion
# of points change place during path change) eg. @functools.lru_cache(maxsize=128, typed=False)
# maxsize should be a power of 2 for best performance
#dist = lambda p1, p2: ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

#@lru_cache(maxsize=512)
def dist(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
