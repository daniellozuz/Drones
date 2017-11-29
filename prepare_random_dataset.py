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
         'altitude': (50, 70),
         'factor': (2.5, 3),
         'waiting_at_base': (50, 100),
         'waiting_at_client': (30, 60)}

PARCEL = {'amount': (40, 50),
          'positions': (12_000, 18_000)}

city = City(position=CITY['position'], wind=CITY['wind'])

for drone_number in range(randint(*DRONE['amount'])):
    city += Drone(drone_number + 1,
                  base=city.position,
                  wind=CITY['wind'],
                  drone_mass=randint(*DRONE['mass']),
                  max_capacity=randint(*DRONE['capacity']),
                  max_speed=randint(*DRONE['speed']),
                  max_fuel=randint(*DRONE['fuel']),
                  base_fuel_consumption=randint(*DRONE['consumption']),
                  altitude=randint(*DRONE['altitude']),
                  factor=randint(*DRONE['factor']),
                  waiting_at_base=randint(*DRONE['waiting_at_base']),
                  waiting_at_client=randint(*DRONE['waiting_at_client']))

for parcel_number in range(randint(*PARCEL['amount'])):
    city += Parcel(parcel_number + 1,
                   randint(*PARCEL['position']),
                   randint(*PARCEL['weight']))
