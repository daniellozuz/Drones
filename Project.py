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
city.rload("westernsahara29.txt")
city += Drone(1, 2400, 8, base=city.position)

# Computations and Visualization
city.assign()
plots.show_parcels(city)
plots.show_drone_paths(city)

city.full_simulated_annealing()

print("before final sweep")
plots.show_drone_paths(city, final=True)
for _ in range(100):
    city.final_sweep()
print("after final sweepings")
plots.show_drone_paths(city, final=True)

plots.show_distance_history(city)
