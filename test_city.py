"""City module tests."""


import unittest

from City import City
from Drone import Drone
from Parcel import Parcel


class TestCity(unittest.TestCase):
    """Class provides tests for city module functions."""


    def setUp(self):
        """Prepare environment for testing."""

        self.city = City(position=(0, 0), wind=(1, 2))

        self.drone0 = Drone(0, 50, 10) # Empty drone
        self.drone1 = Drone(1, 140, 8) # Drone with parcels

        self.parcel1 = Parcel(1, 10, (1, 1))
        self.parcel2 = Parcel(2, 5, (-20, -1))

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


    def test_set_wind(self):
        """Check changing the wind."""

        self.assertEqual(self.city.wind, (1, 2))

        self.city.set_wind((-6, -7))

        self.assertEqual(self.city.wind, (-6, -7))


    def test_distribute(self):
        """Checks whether distribution assigns parcels to drones."""

        self.assertEqual((sum(len(drone.parcels) for drone in self.city.drones)), 0)

        self.city += [self.drone0, self.drone1]
        self.city += [self.parcel1, self.parcel2]
        self.city.distribute()

        self.assertEqual((sum(len(drone.parcels) for drone in self.city.drones)), 2)


    def test_calculate_total_distance(self):
        """Checks total distance recalculation for a single drone with a single parcel."""

        self.assertEqual(self.city.total_distance, 0)

        self.city += self.drone0
        self.city += self.parcel1
        self.city.distribute()

        self.assertEqual(self.city.total_distance, 2.8284271247461903)


if __name__ == '__main__':
    unittest.main()
