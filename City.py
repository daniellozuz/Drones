"""This class serves as a data representation of the whole system.

Calling its methods enables:

    city parameters specification - wind, base(s) position,

    drone and parcel creation,

    numerical computations - rearranging parcels among drones and recalculating results."""


import copy
import json
import math
from random import choice, randint, random

from common import Position as Pos
from Drone import Drone
from Parcel import Parcel

import plots


class City():
    """Main interface with the data."""


    def __init__(self, position=Pos(0, 0), wind=(0, 0)):
        # TODO implement a way to create random data (specify number of drones and parcels to be randomly added).
        # TODO implement saving to and reading from a file (testing purposes, samples, which would be a reference to algorithm performance).

        self.position = position
        self.wind = wind
        self.total_distance = 0
        self.best_total_distance = math.inf
        self.best_total_distances = []
        self.total_distances = []
        self.drones = []
        self.parcels = []


    def __add__(self, items):
        if isinstance(items, Drone) or isinstance(items, Parcel):
            items = [items]
        for item in items:
            if isinstance(item, Drone):
                self.drones.append(item)
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


    def load(self, json_file_name):
        """Loads data (city parameters, drones and parcels) from json .txt file."""

        with open(json_file_name) as json_file:
            data = json.load(json_file)

        self.wind = tuple(data['wind'])
        self.position = Pos(data['position'][0], data['position'][1])
        self.parcels = []
        self.drones = []
        for parcel in data['parcels']:
            self += Parcel(parcel['number'], parcel['weight'], Pos(parcel['x'], parcel['y']))
        for drone in data['drones']:
            self += Drone(drone['number'], drone['max_capacity'], drone['max_speed'])


    def set_wind(self, wind):
        """Sets wind to given value."""

        if isinstance(wind, tuple) and len(wind) == 2:
            self.wind = wind
        else:
            raise TypeError


    def distribute(self):
        """Distributes parcels at random among drones.""" # XXX initialization procedure

        for drone in self.drones:
            drone.parcels = []
        for parcel in self.parcels:
            drone = choice(self.drones)
            drone += parcel
        self._calculate_total_distance()


    def try_scrambling_parcels(self):
        """Performs random redistribution of parcels to drones (undone if no improvement)."""

        # Save previous state.
        prev_drones = []
        prev_distance = self.total_distance
        for drone in self.drones:
            prev_drones.append(copy.deepcopy(drone))

        # Clear state and reassign parcels randomly.
        for drone in self.drones:
            drone.parcels = []
        for parcel in self.parcels:
            drone = choice(self.drones)
            drone += parcel

        # Check results and decide whether the new solution is kept
        # TODO there is the part of simulated annealing I need to implement
        self._calculate_total_distance()
        self.total_distances.append(self.total_distance)
        if self.total_distance >= prev_distance:
            for drone, prev_drone in self.drones, prev_drones:
                drone = prev_drone
            self._calculate_total_distance()


    # TODO add swapping method in parameter?
    def simulated_annealing(self, k, temperature):
        """Performs simulated annealing algorithm."""

        # Save previous state.
        prev_drones = []
        prev_distance = self.total_distance
        for drone in self.drones:
            prev_drones.append(copy.deepcopy(drone))

        self._move(int(math.sqrt(temperature) - 3))
        print('Moving: ', int(math.sqrt(temperature) - 3))
        self._swap_neighbour(int(math.sqrt(math.sqrt(temperature))))
        print('Swapping: ', int(math.sqrt(math.sqrt(temperature))))

        # Pop and insert.
        # self._move()

        # Check results and decide whether the new solution is kept
        self._calculate_total_distance()
        self.total_distances.append(self.total_distance)
        if self.total_distance < self.best_total_distance:
            self.best_total_distance = self.total_distance

        weird_value = math.e ** (k * (prev_distance - self.total_distance) / temperature)
        print('Weird value:', weird_value)
        if weird_value > random():
            print('Passed.')
        else:
            print('Revert.')
            for i in range(len(self.drones)):
                self.drones[i] = prev_drones[i]
            self._calculate_total_distance()

        self.best_total_distances.append(self.best_total_distance)


    def _calculate_total_distance(self):
        """Returns total distance covered by drones."""
        # TODO Replace distance with time (distance tends to assign most parcels to single drone).

        distance = 0

        for drone in self.drones:
            drone.update()
            distance += drone.path_length

        self.total_distance = distance


    def _swap(self, between_drones, in_drone):
        """Performs given amount of parcel swaps."""
        # TODO make it not swap but pop and insert?
        # XXX errors when no parcels assigned to a drone (random function goes mad).

        for _ in range(between_drones):
            drone1index = randint(0, len(self.drones) - 1)
            drone2index = randint(0, len(self.drones) - 1)

            drone1 = self.drones[drone1index]
            drone2 = self.drones[drone2index]

            parcel1index = randint(0, len(drone1.parcels) - 1)
            parcel2index = randint(0, len(drone2.parcels) - 1)

            self.drones[drone1index].parcels[parcel1index], self.drones[drone2index].parcels[parcel2index] = self.drones[drone2index].parcels[parcel2index], self.drones[drone1index].parcels[parcel1index]

        for drone in self.drones:
            drone.update()
    
    
    def _swap_neighbour(self, amount):
        """Swaps two neighbouring parcels in a random drone amount number of times."""
        # Fine part of an algorithm.

        for _ in range(amount):
            drone_index = randint(0, len(self.drones) - 1)

            drone = self.drones[drone_index]

            if len(drone.parcels) < 2:
                continue

            parcel_index = randint(0, len(drone.parcels) - 2)

            drone.parcels[parcel_index], drone.parcels[parcel_index + 1] = drone.parcels[parcel_index + 1], drone.parcels[parcel_index]

        for drone in self.drones:
            drone.update()


    def _move(self, amount):
        """Moves random parcel between two random drones amount number of times."""
        # Crude part of an algorithm.

        for _ in range(amount):
            drone_from_index = randint(0, len(self.drones) - 1)
            drone_to_index = randint(0, len(self.drones) - 1)

            drone_from = self.drones[drone_from_index]
            drone_to = self.drones[drone_to_index]

            if not drone_from.parcels:
                continue

            parcel_pop_index = randint(0, len(drone_from.parcels) - 1)
            parcel_insert_index = randint(0, len(drone_to.parcels))

            drone_to.parcels.insert(parcel_insert_index, drone_from.parcels.pop(parcel_pop_index))

        for drone in self.drones:
            drone.update()





if __name__ == '__main__':

    city = City(position=Pos(0, 0), wind=(1, 2))
    city += Drone(1, 140, 8)
    city += Drone(2, 103, 15)

    for i in range(5):
        city += Parcel(i + 1, randint(10, 40), Pos(randint(-20, 20), randint(-20, 20)))

    print(city)
    print(city.total_distance)
    city.distribute()
    print(city)
    print(city.total_distance)

    plots.show_parcels(city)
    plots.show_drone_paths(city)

    print(city.wind)
    city.set_wind((10, 20))
    print(city.wind)

    city.simulated_annealing(0.01, 1000)

    print(city.total_distance)
    print('Parcelki 0 :)', city.drones[0].parcels)
    print('Parcelki 1 :)', city.drones[1].parcels)
    print('Drone 0 length: ', city.drones[0].path_length)
    print('Drone 1 length: ', city.drones[1].path_length)
    city._swap(1, 2)
    city._calculate_total_distance()
    print(city.total_distance)
    print('Parcelki 0 :)', city.drones[0].parcels)
    print('Parcelki 1 :)', city.drones[1].parcels)
    print('Drone 0 length: ', city.drones[0].path_length)
    print('Drone 1 length: ', city.drones[1].path_length)
    plots.show_drone_paths(city)
