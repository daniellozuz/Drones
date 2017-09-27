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
city += Drone(3, 100, 10)
city += Drone(4, 50, 50)

for i in range(50):
    city += Parcel(i + 1, randint(10, 40), (randint(-20, 20), randint(-20, 20)))


# Computations and Visualization
city.distribute()
print(city.total_distance)
plots.show_parcels(city)
plots.show_drone_paths(city)
prev_best = city.total_distance

k = 0.01
temperature = 1000

for i in range(1000):
    city.simulated_annealing(k, temperature)
    print('Now', round(city.total_distance), 'Before', round(prev_best), 'Temp', temperature)
    temperature *= 0.999
    if city.total_distance < prev_best:
        plots.show_drone_paths(city)
        prev_best = city.total_distance

plots.show_distance_history(city)
