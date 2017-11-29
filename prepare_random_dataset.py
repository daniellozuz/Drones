"""Dataset preparation for algorithm tuning."""

from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel
import plots
from random import randint, uniform

CITY = {'position': (0, 0),
        'wind': (0, 0)}

DRONE = {'amount': (4, 4),
         'mass': (30, 30),
         'capacity': (25000, 25000),
         'speed': (18, 18),
         'fuel': (5, 5),
         'consumption': (0, 0),
         'altitude': (0, 0),
         'factor': (3, 3),
         'waiting_at_base': (0, 0),
         'waiting_at_client': (0, 0)}

PARCEL = {'amount': (20, 20),
          'position': (-18_000, 18_000),
          'weight': (0, 0)}

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
