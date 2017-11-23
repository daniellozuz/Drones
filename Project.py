"""This module defines program behaviour.

    A programmer is supposed to specify the problem using the interface provided in City module."""

from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel
import plots


# City creation
city = City()
city.cload("punktykrakow.txt")
city += Drone(1, 24000, 8, base=city.position)
city += Drone(2, 24000, 8, base=city.position)

# Computations
# city.full_simulated_annealing(iterations=1000, initial_temperature=10, final_temperature=0.001)

# city.test_tsp(iterations=1000, initial_temperature=10000000, final_temperature=1000)
# city.test_tsp(iterations=1000, initial_temperature=0.00001, final_temperature=0.000000001)
# city.test_tsp(iterations=1000, initial_temperature=10000, final_temperature=1)
# city.test_tsp(iterations=10000, initial_temperature=10, final_temperature=0.001)
# city.test_tsp(iterations=1000, initial_temperature=0.01, final_temperature=0.000001)

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









# # Przyklad - Testowanie zaleznosci od iteracji.
# city = City(metric='simple')
# city += Drone(1, 24000, 8, base=city.position)
# city.test_tsp(iterations=1000, initial_temperature=10000000, final_temperature=1000)
# city.test_tsp(iterations=5000, initial_temperature=0.00001, final_temperature=0.000000001)
# city.test_tsp(iterations=10000, initial_temperature=10000, final_temperature=1)
# plots.show_test_results()

# Przyklad - Testowanie zaleznosci od temperatury.
# city = City(metric='simple')
# city += Drone(1, 24000, 8, base=city.position)
# city.test_tsp(iterations=10000, initial_temperature=10000000000000, final_temperature=1000000000)
# city.test_tsp(iterations=10000, initial_temperature=10000000000, final_temperature=1000000)
# city.test_tsp(iterations=10000, initial_temperature=10000000, final_temperature=1000)
# city.test_tsp(iterations=10000, initial_temperature=10000, final_temperature=1)
# city.test_tsp(iterations=10000, initial_temperature=10, final_temperature=0.001)
# city.test_tsp(iterations=10000, initial_temperature=0.01, final_temperature=0.000001)
# city.test_tsp(iterations=10000, initial_temperature=0.00001, final_temperature=0.000000001)
# city.test_tsp(iterations=10000, initial_temperature=0.00000001, final_temperature=0.000000000001)
# city.test_tsp(iterations=10000, initial_temperature=0.00000000001, final_temperature=0.000000000000001)
# plots.show_test_results()

# # Przyklad - Separacja na dwie strefy.
# city = City()
# city.cload("punktykrakow.txt")
# city += Drone(1, 24000, 8, base=city.position)
# city += Drone(2, 24000, 8, base=city.position)
# city.full_simulated_annealing(iterations=10000, initial_temperature=10, final_temperature=0.001)
