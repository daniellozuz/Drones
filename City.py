"""This class serves as a data representation of the whole system.

Calling its methods enables:
    
    city parameters specification - wind, base(s) position,

    drone and parcel creation,

    numerical computations - rearranging parcels among drones and recalculating results."""


import random

from Drone import Drone
from Parcel import Parcel

import plots


# TODO @classmethods as means of reading data from txt file and loading it into City
# XXX I need only 1 City, should I even bother to make object or work on a class?

class City():
    """Main interface with the data."""


    def __init__(self, position=(0, 0), wind=(0, 0)):
        # TODO implement a way to create random data (specify number of drones and parcels to be randomly added).
        # TODO implement saving to and reading from a file (testing purposes, samples, which would be a reference to algorithm performance).

        self.position = position
        self.wind = wind
        self.total_distance = 0
        self.total_distances = []
        self.drones = []
        self.parcels = []


    def __add__(self, item):
        # TODO implement additions of whole lists of drones and/or parcels.

        if isinstance(item, Drone):
            self.drones.append(item)
            return self

        if isinstance(item, Parcel):
            self.parcels.append(item)
            return self


    def __str__(self):
        string = '=' * 40 + ' City description ' + '=' * 40 + '\n'
        string += f'Wind speed: {self.wind}\n'
        string += f'\nThere are {len(self.drones)} drones in the city:\n'
        string += '{:>20}'.format('Drone ID')
        string += '{:>20}'.format('Max capacity')
        string += '{:>20}'.format('Max speed')
        string += '{:>20}\n'.format('Parcels assigned')
        for drone in self.drones:
            string += str(drone)
        string += f'\nThere are {len(self.parcels)} parcels in the city:\n'
        string += '{:>20}'.format('Parcel ID')
        string += '{:>20}'.format('Weight')
        string += '{:>20}\n'.format('Position')
        for parcel in self.parcels:
            string += str(parcel)
        return string


    @classmethod
    def set_wind(cls, wind):
        """Sets class attribute wind to given value."""

        if isinstance(wind, tuple) and len(wind) == 2:
            cls.wind = wind
        else:
            raise TypeError


    def scramble_parcels(self):
        """Distributes parcels at random among drones.""" # XXX initialization procedure

        for drone in self.drones:
            drone.parcels = []

        for parcel in self.parcels:
            drone = random.choice(self.drones)
            drone += parcel

        self.total_distance = self._calculate_total_distance()


    def try_scrambling_parcels(self):
        """Performs random redistribution of parcels to drones (undone if no improvement)."""

        import copy

        prev_drones = []
        prev_distance = self.total_distance

        for drone in self.drones:
            prev_drones.append(copy.deepcopy(drone))
            drone.parcels = []

        for parcel in self.parcels:
            drone = random.choice(self.drones)
            drone += parcel

        self.total_distance = self._calculate_total_distance()
        self.total_distances.append(self.total_distance)

        if self.total_distance >= prev_distance:
            for drone, prev_drone in self.drones, prev_drones:
                drone = prev_drone
            self.total_distance = self._calculate_total_distance()


    def _calculate_total_distance(self):
        """Returns total distance covered by drones."""
        # TODO Replace distance with time (distance tends to assign most parcels to single drone).

        distance = 0

        for drone in self.drones:
            drone.update()
            distance += drone.path_length

        return distance





if __name__ == '__main__':
    # TODO Create tests, check how to do this (doctest or unittest)
    from random import randint
    city = City(position=(0, 0), wind=(1, 2))
    city += Drone(1, 40, 8)
    city += Drone(2, 103, 15)

    for i in range(25):
        city += Parcel(i + 1, randint(10, 40), (randint(-20, 20), randint(-20, 20)))

    print(city)
    print(city.total_distance)
    city.scramble_parcels()
    print(city)
    print(city.total_distance)

    plots.show_parcels(city)
    plots.show_drone_paths(city)

    # TODO XXX Class City and its object city or class City as a container for data (operating on class)
    print(city.wind)
    city.set_wind((10, 20))
    print(city.wind)
    print(City.wind)
