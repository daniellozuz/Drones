"""Dataset preparation for algorithm tuning."""

from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel
import plots
from random import randint, uniform

CITY = {'position': (0, 0),
        'wind': (2, 1)}

DRONE = {'amount': (3, 4),
         'mass': (10, 30),
         'capacity': (20, 25),
         'speed': (12, 18),
         'fuel': (3, 5),
         'consumption': (0.001, 0.003),
         'altitude': (50, 70),
         'factor': (2.5, 3),
         'waiting_at_base': (50, 100),
         'waiting_at_client': (30, 60)}

PARCEL = {'amount': (40, 50),
          'position': (-18_000, 18_000),
          'weight': (0.1, 5)}

city = City(position=Pos(*CITY['position']), wind=CITY['wind'])

for drone_number in range(randint(*DRONE['amount'])):
    city += Drone(drone_number + 1,
                  base=city.position,
                  wind=CITY['wind'],
                  drone_mass=randint(*DRONE['mass']),
                  max_capacity=randint(*DRONE['capacity']),
                  max_speed=randint(*DRONE['speed']),
                  max_fuel=randint(*DRONE['fuel']),
                  base_fuel_consumption=uniform(*DRONE['consumption']),
                  altitude=randint(*DRONE['altitude']),
                  factor=uniform(*DRONE['factor']),
                  waiting_at_base=randint(*DRONE['waiting_at_base']),
                  waiting_at_client=randint(*DRONE['waiting_at_client']))

for parcel_number in range(randint(*PARCEL['amount'])):
    city += Parcel(parcel_number + 1,
                   Pos(randint(*PARCEL['position']), randint(*PARCEL['position'])),
                   uniform(*PARCEL['weight']))

# Testing?
city.full_simulated_annealing(iterations=10000, initial_temperature=10, final_temperature=0.0000001, show_solution=False)
