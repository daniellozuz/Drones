"""Drone module tests."""


import unittest

from common import Position as Pos
from Drone import Drone
from Parcel import Parcel


class TestDrone(unittest.TestCase):
    """Class provides tests for drone module functions."""


    def setUp(self):
        """Prepare environment for testing."""

        self.drone0 = Drone(0, 50, 10) # Empty drone
        self.drone1 = Drone(1, 140, 8) # Drone with parcels

        self.parcel1 = Parcel(1, 10, Pos(1, 1))
        self.parcel2 = Parcel(2, 5, Pos(-20, -1))

        self.drone1 += self.parcel1
        self.drone1 += self.parcel2


    def test___add__(self):
        """Check adding a parcel to the drone."""

        self.assertEqual(self.drone0.parcels, [])

        self.drone0 += Parcel(0, 50, Pos(10, 10))

        self.assertEqual(len(self.drone0.parcels), 1)
        self.assertIsInstance(self.drone0.parcels[0], Parcel)
        self.assertEqual(len(self.drone0.path), 3)
        self.assertEqual(self.drone0.path_length, 28.284271247461902)


    def test___add__2(self):
        """Check adding multiple parcels to the drone."""

        self.assertEqual(self.drone0.parcels, [])

        self.drone0 += [Parcel(0, 5, Pos(10, 10)), Parcel(1, 15, Pos(20, 20))]

        self.assertEqual(len(self.drone0.parcels), 2)
        self.assertIsInstance(self.drone0.parcels[0], Parcel)
        self.assertIsInstance(self.drone0.parcels[1], Parcel)
        self.assertEqual(len(self.drone0.path), 4)
        self.assertEqual(self.drone0.path_length, 56.568542494923804)


    def test_path_length(self):
        """Check fetching path and path_length."""

        self.assertEqual(self.drone0.path_length, 0)
        self.assertEqual(self.drone1.path_length, 42.53422106660287)
        self.assertEqual(len(self.drone0.path), 2)
        self.assertEqual(len(self.drone1.path), 4)



if __name__ == '__main__':
    unittest.main()
