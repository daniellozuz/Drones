"""Provides drone implementation."""


from common import Position as Pos
from common import dist
from Parcel import Parcel


class Drone(object):
    """Provides drone implementation."""


    def __init__(self, number, max_capacity, max_speed, parcels=None):
        self.number = number
        self.max_capacity = max_capacity
        self.max_speed = max_speed
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


    @property
    def path(self, base=Pos(0, 0)):
        """Returns drone's path after recalculating it."""

        occupied_capacity = 0
        path = [base]
        for parcel in self.parcels:
            occupied_capacity += parcel.weight
            if occupied_capacity > self.max_capacity:
                path.append(base)
                occupied_capacity = parcel.weight
            path.append(parcel.position)
        path.append(base)

        return path


    @property
    def path_length(self):
        """Recalculates path length."""

        path = self.path

        return sum(dist(point1, point2) for point1, point2 in zip(path[:-1], path[1:]))
