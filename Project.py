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
city.rload("pr76.txt")
city += Drone(1, 2400, 8, base=city.position)

# Computations and Visualization
city.assign()
plots.show_parcels(city)
plots.show_drone_paths(city)
prev_best = city.total_distance
prev = city.total_distance

# TODO Calculate scale from loaded data, just before launching simulated annealing.
scale = 1
temperature = 1000

# TODO Implement this loop inside City class.
while temperature > 0.1:
    city.simulated_annealing(scale, temperature)
    print('Now', round(city.total_distance), 'Before', round(prev), 'Best', round(prev_best), 'Temp', temperature)
    print('\n')
    temperature *= 0.9997
    prev = city.total_distance
    if city.total_distance < prev_best:
        plots.show_drone_paths(city)
        prev_best = city.total_distance

print("before final sweep")
plots.show_drone_paths(city, final=True)
for _ in range(100):
    city.final_sweep()
print("after final sweepings")
plots.show_drone_paths(city, final=True)

plots.show_distance_history(city)
