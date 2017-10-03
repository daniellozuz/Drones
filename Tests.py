"""Testing purposes."""


from random import shuffle

from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel


# City creation
city = City(position=Pos(0, 0), wind=(1, 2))

city += Drone(1, 24000, 10)

parcels = []

n = 1
for i in range(-40, 50, 10):
    for j in range(-40, 50, 10):
        if i != 0 or j != 0:
            parcels.append(Parcel(n, 10, Pos(i, j)))
            n += 1

shuffle(parcels)

city += parcels

city.store("grid.txt")
