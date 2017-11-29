"""Dataset preparation for algorithm tuning."""

from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel
import plots
from random import randint

CITY = {'position': (0, 0),
        'wind': (2, 4)}

DRONE = {'amount': (3, 4),
         'mass': (10, 30),
         'capacity': (20, 25),
         'speed': (7, 10),
         'fuel': (3, 5),
         'consumption': (0.001, 0.003),
         'loading_time': (1, 1)}

PARCEL = {'amount': (40, 50),
          'positions': (12_000, 18_000)}

city = City(position=CITY['position'], wind=CITY['wind'])

for drone_number in range(randint(*DRONE['amount'])):
    city += Drone(drone_number + 1,
                  max_capacity=randint(*DRONE['capacity']),
                  max_speed=randint(*DRONE['speed']),
                  drone_mass=randint(*DRONE['mass']),
                  max_fuel=randint(*DRONE['fuel']),
                  base_fuel_consumption=randint(*DRONE['consumption']),
                  loading_time=randint(*DRONE['loading_time']),
                  base=city.position)

for parcel_number in range(randint(*PARCEL['amount'])):
    city += Parcel(parcel_number + 1,
                   position=randint(*PARCEL['position']),
                   weight=randint(*PARCEL['weight']))
