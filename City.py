"""This class is a data representation of the whole system."""

import plots
import random

from Drone import Drone
from Parcel import Parcel


class City():
    """Class implements city creation, access to drones and parcels, and drone trajectories."""


    def __init__(self, position=(0, 0), wind=(0, 0)):
        """Creates a city, initialized with wind and empty drone and parcels lists."""

        self.drones = []
        self.parcels = []
        self.position = position
        self.wind = wind
        self.total_distance = 0


    def __add__(self, item):
        """Appends a drone or parcel to iternal parcels or drones lists."""

        if isinstance(item, Drone):
            print('A drone added.')
            self.drones.append(item)
            return self

        if isinstance(item, Parcel):
            print('A parcel added.')
            self.parcels.append(item)
            return self


    def __str__(self):
        """Provides printing of a city."""

        string = '=' * 40 + ' City description ' + '=' * 40
        string += "\nWind's strength: {wind}\n".format(wind=self.wind)

        string += '\nThere are {amount} drones in the city:\n'.format(amount=len(self.drones))
        for drone in self.drones:
            string += str(drone)

        string += '\nThere are {amount} parcels in the city:\n'.format(amount=len(self.parcels))
        for parcel in self.parcels:
            string += str(parcel)

        return string


    def scramble_parcels(self):
        """Distributes parcels in random fashion among drones."""

        for drone in self.drones:
            drone.parcels = []

        for parcel in self.parcels:
            drone = random.choice(self.drones)
            drone += parcel

        self.total_distance = self.calculate_total_distance()


    def try_scrambling_parcels(self):
        """Creates a copy of a city, tries redistrubution, reverts back if no progress."""
        import copy

        prev_drones = []
        prev_distance = self.total_distance

        for drone in self.drones:
            prev_drones.append(copy.deepcopy(drone))
            drone.parcels = []

        for parcel in self.parcels:
            drone = random.choice(self.drones)
            drone += parcel

        self.total_distance = self.calculate_total_distance()

        if self.total_distance >= prev_distance:
            for drone, prev_drone in self.drones, prev_drones:
                drone.parcels = prev_drone.parcels[:]
            self.total_distance = self.calculate_total_distance()



    def calculate_total_distance(self):
        """Returns total distance covered by drones."""

        distance = 0

        for drone in self.drones:
            drone.update()
            distance += drone.path_length

        return distance



if __name__ == '__main__':
    from random import randint
    city = City(position=(0, 0), wind=(1, 2))
    city += Drone(1, 40, 8)
    city += Drone(2, 103, 15)

    for i in range(25):
        city += Parcel(i + 1, randint(10, 40), (randint(-20, 20), randint(-20, 20)))

    print(city)
    print(city.total_distance)
    city.distribute()
    print(city)
    print(city.total_distance)

    plots.show_parcels(city)
    plots.show_drone_paths(city)
