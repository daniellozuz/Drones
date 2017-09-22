"""Module provides unit tests for the whole program."""


import unittest

from Parcel import Parcel
from Drone import Drone


class TestEmployee(unittest.TestCase):
    """Class provides tests for all modules (might be a good idea to split them in the future)."""


    def setUp(self):
        """Prepare environment for testing."""

        self.drone0 = Drone(0, 50, 10) # Empty drone
        self.drone1 = Drone(1, 140, 8) # Drone with parcels

        self.parcel1 = Parcel(1, 10, (1, 1))
        self.parcel2 = Parcel(2, 5, (-20, -1))

        self.drone1 += self.parcel1
        self.drone1 += self.parcel2


    def test___add__(self):
        """Check adding a parcel to the drone."""

        self.assertEqual(self.drone0.parcels, [])
        self.drone0 += Parcel(0, 50, (10, 10))
        self.assertEqual(len(self.drone0.parcels), 1)
        self.assertIsInstance(self.drone0.parcels[0], Parcel)
        self.assertEqual(self.drone0.path, [])
        self.assertEqual(self.drone0.path_length, 0)


    def test_recalculate_path_length(self):
        """Check path and path_length recalculations before and after an update."""

        # Drones paths were not updated yet, so path recalculation does not have effect.
        self.assertEqual(self.drone0.path_length, 0)
        self.assertEqual(self.drone1.path_length, 0)
        Drone._recalculate_path_length(self.drone0)
        Drone._recalculate_path_length(self.drone1)
        self.assertEqual(self.drone0.path_length, 0)
        self.assertEqual(self.drone1.path_length, 0)

        # Drone update recalculates path and path_length
        self.assertEqual(len(self.drone0.path), 0)
        self.assertEqual(len(self.drone1.path), 0)
        self.drone0.update()
        self.drone1.update()
        self.assertEqual(len(self.drone0.path), 2)
        self.assertEqual(len(self.drone1.path), 4)
        self.assertEqual(self.drone0.path_length, 0)
        self.assertEqual(self.drone1.path_length, 42.53422106660287)


if __name__ == '__main__':
    unittest.main()
