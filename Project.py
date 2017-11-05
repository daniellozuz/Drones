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

#city += Drone(1, 2400, 8, base=city.position)
# city += Drone(2, 203, 15)
# city += Drone(3, 300, 10)
# city += Drone(4, 250, 50)

#for i in range(75):
#    city += Parcel(i + 1, randint(10, 40), Pos(randint(-20, 20), randint(-20, 20)))

city.rload("djibouti.txt")
city += Drone(1, 2400, 8, base=city.position)

# Computations and Visualization
city.assign()
print(city.total_distance)
plots.show_parcels(city)
plots.show_drone_paths(city)
prev_best = city.total_distance
prev = city.total_distance

scale = 1
temperature = 1000

while temperature > 0.1:
    city.simulated_annealing(scale, temperature)
    print('Now', round(city.total_distance), 'Before', round(prev), 'Best', round(prev_best), 'Temp', temperature)
    print('\n')
    temperature *= 0.9997
    prev = city.total_distance
    if city.total_distance < prev_best:
        plots.show_drone_paths(city)
        prev_best = city.total_distance
    #plots.show_drone_paths(city)

print("before final sweep")
plots.show_drone_paths(city, final=True)
for _ in range(100):
    city.final_sweep()
print("after final sweepings")
plots.show_drone_paths(city, final=True)

plots.show_distance_history(city)
