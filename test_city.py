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

        self.city = City(position=Pos(0, 0), wind=(1, 2))

        self.drone0 = Drone(0, 50, 10) # Empty drone
        self.drone1 = Drone(1, 140, 8) # Drone with parcels

        self.parcel1 = Parcel(1, 10, Pos(1, 1))
        self.parcel2 = Parcel(2, 5, Pos(-20, -1))

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


    def test_calculate_total_distance(self):
        """Checks total distance recalculation for a single drone with a single parcel."""

        self.assertEqual(self.city.total_distance, 0)

        self.city += self.drone0
        self.city += self.parcel1
        self.city.prepare_algorithm()

        self.assertEqual(self.city.total_distance, 2.8284271247461903)


    def test_jload(self):
        """Checks loading data from json formatted txt file."""

        self.city += self.drone0
        self.city += self.parcel1

        self.assertEqual(self.city.drones, [self.drone0])
        self.assertEqual(self.city.parcels, [self.parcel1])

        self.city.jload("stub.txt")

        self.assertEqual(len(self.city.drones), 2)
        self.assertIsInstance(self.city.drones[0], Drone)
        self.assertIsInstance(self.city.drones[1], Drone)
        self.assertEqual(len(self.city.parcels), 2)
        self.assertIsInstance(self.city.parcels[0], Parcel)
        self.assertIsInstance(self.city.parcels[1], Parcel)


    def test_store(self):
        """Checks storing data to json formatted txt file."""

        self.city.jload("stub.txt")
        self.city.store("stub2.txt")
        self.city.drones = []
        self.city.parcels = []

        self.assertEqual(self.city.drones, [])
        self.assertEqual(self.city.parcels, [])

        self.city.jload("stub2.txt")

        self.assertEqual(len(self.city.drones), 2)
        self.assertEqual(len(self.city.parcels), 2)
        self.assertIsInstance(self.city.parcels[0], Parcel)
        self.assertIsInstance(self.city.parcels[1], Parcel)





if __name__ == '__main__':
    unittest.main()
