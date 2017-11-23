"""Provides drone implementation."""

# TODO implement interface for external specification of drone parameters, that is:
# formulae/discrete characteristics of fuel_consumption or max_speed.

from math import e, sqrt, sin, cos, atan2
from random import randrange

from common import Position as Pos
from common import dist
from Parcel import Parcel

class Drone(object):
    """Provides drone implementation."""

    def __init__(self, number, max_capacity, max_speed, base=Pos(0, 0), parcels=None,
                 drone_mass=20, max_fuel=5, wind=(0, 0), loading_time=5, base_fuel_consumption=0.001):
        self.position = base
        self.number = number
        self.mass = drone_mass
        self.max_capacity = max_capacity
        self.used_capacity = 0
        self.max_speed = max_speed
        self.max_fuel = max_fuel
        self.fuel = max_fuel
        self.base_fuel_consumption = base_fuel_consumption
        self.base = base
        self.cargo = []
        if parcels is None:
            parcels = []
        self.parcels = parcels
        self.wind = wind
        self.loading_time = loading_time # Rising + falling + refuelling + maintenance + reloading

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
    def speed(self):
        """Calculate speed according to drone's state."""
        return self.max_speed / e ** ((self.fuel + self.used_capacity) / self.mass)

    @property
    def fuel_consumption(self):
        """Calculate fuel consumption according to drone's state."""
        return self.base_fuel_consumption * e ** ((self.fuel + self.used_capacity) / self.mass)

    @property
    def path_length(self):
        """Get recalculated path length."""
        path = self.path
        return sum(dist(point1, point2) for point1, point2 in zip(path[:-1], path[1:]))

    @property
    def path(self):
        """Get recalculated drone's path."""
        self.used_capacity = 0
        path = [self.base]
        for parcel in self.parcels:
            self.used_capacity += parcel.weight
            if self.used_capacity > self.max_capacity:
                path.append(self.base)
                self.used_capacity = parcel.weight
            path.append(parcel.position)
        path.append(self.base)
        return path

    @property
    def total_time(self):
        """Calculate everything inside this function, then separate it into a few if possible."""
        # TODO add constant time of landing / starting / refuelling-preparing to flight.
        # (where? included in fuel_consumption? - is_possible or trip_time or total_time)
        self.used_capacity = 0
        total_time = 0
        self.fuel = self.max_fuel
        self.position = self.base
        self.cargo = []
        for parcel in self.parcels:
            time = self.trip_time(self.cargo)
            self.cargo.append(parcel)
            if not self.is_possible():
                self.cargo = []
                total_time += time
                self.cargo.append(parcel)
        time = self.trip_time(self.cargo)
        total_time += time
        self.cargo = []
        return total_time

    def is_possible(self):
        """Check whether such a cargo is possible to be delivered in one go."""
        self.position = self.base
        cargo_weight = sum(parcel.weight for parcel in self.cargo)
        if cargo_weight > self.max_capacity:
            return False
        self.used_capacity = cargo_weight
        self.fuel = self.max_fuel
        for parcel in self.cargo:
            distance = dist(self.position, parcel.position)
            velocity = self.absolute_speed(self.position, parcel.position)
            # include wind and reloading/preparing times. TODO check it.
            self.position = parcel.position
            time = distance / velocity + self.loading_time
            fuel_cost = self.fuel_consumption * time
            self.fuel -= fuel_cost
            self.used_capacity -= parcel.weight
            if self.fuel < 0:
                return False
        distance = dist(self.position, self.base)
        velocity = self.absolute_speed(self.position, self.base)
        # include wind and reloading/preparing times. TODO check it.
        time = distance / velocity + self.loading_time
        fuel_cost = self.fuel_consumption * time
        if self.fuel < 0:
            return False
        return True

    def trip_time(self, cargo):
        """Calculate time needed to deliver cargo."""
        total_time = 0
        position = self.base
        cargo_weight = sum(parcel.weight for parcel in cargo)
        self.used_capacity = cargo_weight
        self.fuel = self.max_fuel
        for parcel in cargo:
            distance = dist(position, parcel.position)
            velocity = self.absolute_speed(self.position, parcel.position)
            position = parcel.position
            # include wind and reloading/preparing times. TODO check it.
            time = distance / velocity + self.loading_time
            total_time += time
            fuel_cost = self.fuel_consumption * time
            self.fuel -= fuel_cost
            self.used_capacity -= parcel.weight
        distance = dist(position, self.base)
        velocity = self.absolute_speed(self.position, self.base)
        # include wind and reloading/preparing times. TODO check it.
        time = distance / velocity + self.loading_time
        total_time += time
        fuel_cost = self.fuel_consumption * time
        return total_time

    def absolute_speed(self, start_position, end_position):
        """Calculate speed with respect to the ground (due to wind and flight direction)."""
        wind_speed = sqrt(self.wind[0] ** 2 + self.wind[1] ** 2)
        drone_speed = self.speed
        assert drone_speed > wind_speed, "Wind is too strong."
        angle1 = atan2(end_position.y - start_position.y, end_position.x - start_position.x)
        angle2 = atan2(self.wind[1], self.wind[0])
        alpha = abs(angle2 - angle1)
        return wind_speed * cos(alpha) + sqrt(drone_speed ** 2 - wind_speed ** 2 * sin(alpha) ** 2)

    def twoopt(self):
        """Performs a 2-opt modification of parcels."""
        if not self.parcels:
            return
        #assert len(self.parcels) > 0, 'No parcels!'
        i, k = sorted([randrange(len(self.parcels)), randrange(len(self.parcels))]) # XXX what if the same indeces?
        new_parcels = []
        new_parcels.extend(self.parcels[:i])
        new_parcels.extend(reversed(self.parcels[i:k]))
        new_parcels.extend(self.parcels[k:])
        self.parcels = new_parcels
