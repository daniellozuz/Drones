"""This module is an interface to the while program.

We instantiate a city, provide it with data, and call appropriate
methods to manupulate data and receive results or visualization
(mostly Plots and Algorithms classes)."""


from random import randint

from City import City
from Drone import Drone
from Parcel import Parcel

import Algorithms
import plots


# City creation
city = City(position=(0, 0), wind=(1, 2))

city += Drone(1, 40, 8)
city += Drone(2, 103, 15)

for i in range(25):
    city += Parcel(i + 1, randint(10, 40), (randint(-20, 20), randint(-20, 20)))


# Computations and Visualization
city.scramble_parcels()
print(city.total_distance)
city.scramble_parcels()
print(city.total_distance)
plots.show_parcels(city)
plots.show_drone_paths(city)

