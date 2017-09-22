"""This class serves as a data representation of the whole system.

Calling its methods enables:
    
    city parameters specification - wind, base(s) position,

    drone and parcel creation,

    numerical computations - rearranging parcels among drones and recalculating results."""


import math
import random

from Drone import Drone
from Parcel import Parcel

import plots


# TODO @classmethods as means of reading data from txt file and loading it into City


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


    def __add__(self, items):
        if isinstance(items, Drone) or isinstance(items, Parcel):
            items = [items]
        for item in items:
            if isinstance(item, Drone):
                self.drones.append(item)
                return self
            if isinstance(item, Parcel):
                self.parcels.append(item)
                return self
        return NotImplemented


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

        # Save previous state.
        import copy
        prev_drones = []
        prev_distance = self.total_distance
        for drone in self.drones:
            prev_drones.append(copy.deepcopy(drone))
        
        # Clear state and reassign parcels randomly.
        for drone in self.drones:
            drone.parcels = []
        for parcel in self.parcels:
            drone = random.choice(self.drones)
            drone += parcel

        # Check results and decide whether the new solution is kept
        # TODO there is the part of simulated annealing I need to implement
        self.total_distance = self._calculate_total_distance()
        self.total_distances.append(self.total_distance)
        if self.total_distance >= prev_distance:
            for drone, prev_drone in self.drones, prev_drones:
                drone = prev_drone
            self.total_distance = self._calculate_total_distance()


    def simulated_annealing(self, k, t):
        """Performs simulated annealing algorithm."""

        # Save previous state.
        import copy
        prev_drones = []
        prev_distance = self.total_distance
        for drone in self.drones:
            prev_drones.append(copy.deepcopy(drone))

        # Clear state and reassign parcels randomly.
        # TODO instead of this random shit implement a swapping function. swap(between_drones, positions)
        for drone in self.drones:
            drone.parcels = []
        for parcel in self.parcels:
            drone = random.choice(self.drones)
            drone += parcel

        # Check results and decide whether the new solution is kept
        # TODO there is the part of simulated annealing I need to implement
        self.total_distance = self._calculate_total_distance()
        self.total_distances.append(self.total_distance)

        # TODO check how does this behave
        #print('Improvement:', self.total_distance - prev_distance)
        #print('Weird value:', (1 / (math.e ** ((self.total_distance - prev_distance) / (k * t)) + 1)))
        if (1 / (math.e ** ((self.total_distance - prev_distance) / (k * t)) + 1) > random.random()):
            print('Passed.')
        else:
            print('Revert.')
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


    def _swap(self, x, y):
        # TODO try fixing it so that it really swaps those parcels
        print('Showing before')
        plots.show_drone_paths(self)

        drone1index = random.randint(0, len(self.drones)-1)
        drone2index = random.randint(0, len(self.drones)-1)
        print(drone1index, drone2index)

        drone1 = self.drones[drone1index]
        drone2 = self.drones[drone2index]

        parcel1index = random.randint(0, len(drone1.parcels)-1)
        parcel2index = random.randint(0, len(drone2.parcels)-1)
        print(parcel1index, parcel2index)
        print(self.drones[drone1index].parcels[parcel1index], self.drones[drone2index].parcels[parcel2index])

        self.drones[drone1index].parcels[parcel1index], self.drones[drone2index].parcels[parcel2index] = self.drones[drone2index].parcels[parcel2index], self.drones[drone1index].parcels[parcel1index]
        print(self.drones[drone1index].parcels[parcel1index], self.drones[drone2index].parcels[parcel2index])
        for drone in self.drones:
            drone.update()
        print('Showing after')
        plots.show_drone_paths(self)





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

    city.simulated_annealing(0.01, 1000)

    city._swap(1, 2)
