import random


class Algorithms():
    """Provides numerical methods for City, just to 'hide' ugly numerical computations."""


    def scramble_parcels(self):
        """Distributes parcels in random fashion among drones."""

        for drone in self.drones:
            drone.parcels = []

        for parcel in self.parcels:
            drone = random.choice(self.drones)
            drone += parcel
