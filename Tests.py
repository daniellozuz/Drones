"""Testing purposes."""


from City import City
from common import Position as Pos
from Drone import Drone
from random import randint
from Parcel import Parcel


# City creation
city = City(position=Pos(0, 0), wind=(1, 2))

city += Drone(1, 2400, 8)
for i in range(5):
    city += Parcel(i + 1, randint(10, 40), Pos(randint(-20, 20), randint(-20, 20)))
city.store("rand.txt")
city.parcels = []
print(city.parcels)
city.load("rand.txt")
print(city.parcels)