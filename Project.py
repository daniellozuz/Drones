"""This module defines program behaviour.

    A programmer is supposed to specify the problem using the interface provided in City module."""


from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel
import plots


# City creation
city = City(metric='simple')
city.cload("ulysses22.txt")
city += Drone(1, 24000, 8, base=city.position)
#city += Drone(2, 24000, 8, base=city.position)

# Computations
#city.full_simulated_annealing(cooling_rate=0.997, initial_temperature=1, final_temperature=0.0001)

# city.test_everything(cooling_rate=0.997, initial_temperature=10000000, final_temperature=1000)
# city.test_everything(cooling_rate=0.997, initial_temperature=0.00001, final_temperature=0.000000001)

plots.show_test_results()




# city = City(metric='total_time')
# city += Parcel(1, 6, Pos(1000, 0))
# city += Parcel(2, 6, Pos(-1000, 0))
# city += Parcel(3, 2, Pos(1100, 100))
# city += Parcel(4, 2, Pos(-1100, 100))
# city += Drone(1, 10, 10)
# city += Drone(2, 10, 10)
# city.store('test1.txt')

# city.full_simulated_annealing()













# # Przyklad - separacja na dwie strefy.
# city = City(metric='total_time')
# city.cload("punkty_krakow.txt")
# city += Drone(1, 24000, 8, base=city.position)
# city += Drone(2, 24000, 8, base=city.position)
# city.full_simulated_annealing(cooling_rate=0.9997, initial_temperature=10, final_temperature=0.001)
