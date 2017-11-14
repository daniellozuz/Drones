"""This module defines program behaviour.

    A programmer is supposed to specify the problem using the interface provided in City module."""


from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel


# # City creation
# city = City(metric='simple')
# city.rload("a280.txt")
# city += Drone(1, 2400, 8, base=city.position)

# # Computations
# city.full_simulated_annealing()

# #city.test_everything(cooling_rate=0.9)




city = City(metric='total_time')
city += Parcel(1, 6, Pos(1000, 0))
city += Parcel(2, 6, Pos(-1000, 0))
city += Parcel(3, 2, Pos(1100, 100))
city += Parcel(4, 2, Pos(-1100, 100))
city += Drone(1, 10, 10)
city += Drone(2, 10, 10)
city.store('test1.txt')

city.full_simulated_annealing()
