"""City module tests."""
# TODO tests are not up to date, they might pass, but prove nothing.


import unittest

from City import City
from common import Position as Pos
from Drone import Drone
from Parcel import Parcel


class TestCity(unittest.TestCase):
    """Class provides tests for city module functions."""


    def setUp(self):
        """Prepare environment for testing."""

        self.city = City(position=Pos(0, 0), wind=(1, 2), metric='simple')

        self.drone0 = Drone(0, max_capacity=50, max_speed=10) # Empty drone
        self.drone1 = Drone(1, max_capacity=140, max_speed=8) # Drone with parcels

        self.parcel1 = Parcel(1, Pos(1, 1), 10)
        self.parcel2 = Parcel(2, Pos(-20, -1), 5)

        self.drone1 += self.parcel1
        self.drone1 += self.parcel2


    def test___add__(self):
        """Check adding single drones and single parcels to the city."""

        self.assertEqual(self.city.drones, [])
        self.assertEqual(self.city.parcels, [])

        self.city += self.drone0
        self.city += self.drone1
        self.city += self.parcel1
        self.city += self.parcel2

        self.assertEqual(self.city.drones, [self.drone0, self.drone1])
        self.assertEqual(self.city.parcels, [self.parcel1, self.parcel2])



    def test___add__2(self):
        """Check adding multiple drones and multiple parcels to the city."""

        self.assertEqual(self.city.drones, [])
        self.assertEqual(self.city.parcels, [])

        self.city += [self.drone0, self.drone1]
        self.city += [self.parcel1, self.parcel2]

        self.assertEqual(self.city.drones, [self.drone0, self.drone1])
        self.assertEqual(self.city.parcels, [self.parcel1, self.parcel2])


    def test_prepare_algorithm(self):
        """Checks whether parcels are assigned to drones."""

        self.assertEqual((sum(len(drone.parcels) for drone in self.city.drones)), 0)

        self.city += [self.drone0, self.drone1]
        self.city += [self.parcel1, self.parcel2]
        self.city.prepare_algorithm()

        self.assertEqual((sum(len(drone.parcels) for drone in self.city.drones)), 2)


    def test_calculate_cost(self):
        """Checks cost recalculation for a single drone with a single parcel."""

        self.assertEqual(self.city.total_cost, 0)

        self.city += self.drone0
        self.city += self.parcel1
        self.city.prepare_algorithm()

        self.assertEqual(self.city.total_cost, 2.8284271247461903)


if __name__ == '__main__':
    unittest.main()
