"""This module defines program behaviour.

    A programmer is supposed to provide optimization parameters,
    instantiate a city, provide it with data, and call appropriate
    methods to manupulate data and receive results and visualization.
"""


from random import randint

from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel

import plots


# City creation
city = City()
city.cload("danpolska.txt")
city += Drone(1, 2400, 8, base=city.position)

# Computations
city.full_simulated_annealing()
