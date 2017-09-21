"""This module defines program behaviour.

We instantiate a city, provide it with data, and call appropriate
methods to manupulate data and receive results or visualization."""


from random import randint

from City import City
from Drone import Drone
from Parcel import Parcel

import plots


# City creation
city = City(position=(0, 0), wind=(1, 2))

city += Drone(1, 140, 8)
city += Drone(2, 103, 15)

for i in range(25):
    city += Parcel(i + 1, randint(10, 40), (randint(-20, 20), randint(-20, 20)))


# Computations and Visualization
city.scramble_parcels()
print(city.total_distance)
plots.show_parcels(city)
plots.show_drone_paths(city)
prev_best = city.total_distance

for i in range(1000):
    city.try_scrambling_parcels()
    print(city.total_distance)
    if city.total_distance < prev_best:
        plots.show_drone_paths(city)
        prev_best = city.total_distance

plots.show_distance_history(city)
