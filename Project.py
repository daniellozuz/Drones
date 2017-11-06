"""This module defines program behaviour.

    A programmer is supposed to specify the problem using the interface provided in City module."""


from City import City
#from common import Position as Pos
from Drone import Drone
#from Parcel import Parcel


# City creation
city = City()
#city.cload("danpolska.txt")
city += Drone(1, 2400, 8, base=city.position)

# Computations
#city.full_simulated_annealing()

city.test_everything(cooling_rate=0.999)
