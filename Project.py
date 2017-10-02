"""This module defines program behaviour.

We instantiate a city, provide it with data, and call appropriate
methods to manupulate data and receive results or visualization."""


from collections import namedtuple
from random import randint

from City import City
from Drone import Drone
from Parcel import Parcel

import plots


Position = namedtuple('Position', ['x', 'y'])


# City creation
city = City(position=Position(0, 0), wind=(1, 2))

city += Drone(1, 2400, 8)
# city += Drone(2, 203, 15)
# city += Drone(3, 300, 10)
# city += Drone(4, 250, 50)

for i in range(75):
    city += Parcel(i + 1, randint(10, 40), Position(randint(-20, 20), randint(-20, 20)))


# Computations and Visualization
city.distribute()
print(city.total_distance)
plots.show_parcels(city)
plots.show_drone_paths(city)
prev_best = city.total_distance
prev = city.total_distance

k = 1
temperature = 1

for i in range(500):
    city.simulated_annealing(k, temperature)
    print('Now', round(city.total_distance), 'Before', round(prev), 'Best', round(prev_best), 'Temp', temperature)
    print('\n')
    temperature *= 1
    prev = city.total_distance
    if city.total_distance < prev_best:
        plots.show_drone_paths(city)
        prev_best = city.total_distance
    #plots.show_drone_paths(city)

plots.show_distance_history(city)
