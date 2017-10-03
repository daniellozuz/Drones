"""Module implementing minor functionalities."""


from collections import namedtuple


Position = namedtuple('Position', ['x', 'y'])

dist = lambda p1, p2: ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
