from common import Position as Pos
from common import dist
from Parcel import Parcel


class Drone(object):
    """Provides drone implementation."""


    def __init__(self, number, max_capacity, max_speed, parcels=None):
        self.number = number
        self.max_capacity = max_capacity
        self.max_speed = max_speed
        self.path = []
        self.path_length = 0
        # Passing [] by default does not work. Objects share parcels (because list is MUTABLE)
        if parcels is None:
            parcels = []
        self.parcels = parcels


    def __add__(self, parcels):
        if isinstance(parcels, Parcel):
            parcels = [parcels]
        for parcel in parcels:
            if isinstance(parcel, Parcel):
                self.parcels.append(parcel)
        return self


    def __str__(self):
        string = '{:>20}'.format(self.number)
        string += '{:>20}'.format(self.max_capacity)
        string += '{:>20}'.format(self.max_speed)
        string += '{:>20}\n'.format(len(self.parcels))
        return string


    def __repr__(self):
        string = 'Number: {}, '.format(self.number)
        string += 'Cap: {}, '.format(self.max_capacity)
        string += 'Speed: {}, '.format(self.max_speed)
        string += 'Parcels: {}\n'.format([repr(parcel) for parcel in self.parcels])
        return string


    def update(self, base=Pos(0, 0)):
        """Recalculates drone's parameters after modifications/alterations."""

        # Update drone's path
        occupied_capacity = 0
        self.path = [base]
        for parcel in self.parcels:
            occupied_capacity += parcel.weight
            if occupied_capacity > self.max_capacity:
                self.path.append(base)
                occupied_capacity = 0
            self.path.append(parcel.position)
        self.path.append(base)

        # Update drone's path_length
        self._recalculate_path_length()


    def _recalculate_path_length(self):
        """Recalculates path length."""

        self.path_length = 0
        for point1, point2 in zip(self.path[:-1], self.path[1:]):
            self.path_length += dist(point1, point2)
