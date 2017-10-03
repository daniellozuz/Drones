"""This class serves as a data representation of the whole system.

Calling its methods enables:

    city parameters specification - wind, base(s) position,

    drone and parcel creation,

    numerical computations - rearranging parcels among drones and recalculating results."""


from copy import deepcopy
import json
import math
from random import choice, randint, random, betavariate

from common import Position as Pos
from common import dist
from Drone import Drone
from Parcel import Parcel
import plots


class City():
    """Main interface with the data."""


    def __init__(self, position=Pos(0, 0), wind=(0, 0)):
        self.position = position
        self.wind = wind
        self.drones = []
        self.parcels = []
        self.total_distance = 0
        self.best_total_distance = math.inf
        self.accepted_total_distances = []
        self.attempted_total_distances = []
        self.best_total_distances = []


    def __add__(self, items):
        if isinstance(items, Drone) or isinstance(items, Parcel):
            items = [items]
        for item in items:
            if isinstance(item, Drone):
                self.drones.append(item)
            if isinstance(item, Parcel):
                self.parcels.append(item)
        return self


    def __str__(self):
        string = '=' * 40 + ' City description ' + '=' * 40 + '\n'
        string += f'Wind speed: {self.wind}\n'
        string += f'\nThere are {len(self.drones)} drones in the city:\n'
        string += '{:>20}'.format('Drone ID')
        string += '{:>20}'.format('Max capacity')
        string += '{:>20}'.format('Max speed')
        string += '{:>20}\n'.format('Parcels assigned')
        for drone in self.drones:
            string += str(drone)
        string += f'\nThere are {len(self.parcels)} parcels in the city:\n'
        string += '{:>20}'.format('Parcel ID')
        string += '{:>20}'.format('Weight')
        string += '{:>20}\n'.format('Position')
        for parcel in self.parcels:
            string += str(parcel)
        return string


    def load(self, json_file_name):
        """Loads data (city parameters, drones and parcels) from json .txt file."""

        with open(json_file_name) as json_file:
            data = json.load(json_file)

        self.wind = tuple(data['wind'])
        self.position = Pos(data['position'][0], data['position'][1])
        self.parcels = []
        self.drones = []
        for parcel in data['parcels']:
            self += Parcel(parcel['number'], parcel['weight'], Pos(parcel['x'], parcel['y']))
        for drone in data['drones']:
            self += Drone(drone['number'], drone['max_capacity'], drone['max_speed'])


    def store(self, json_file_name):
        """Stores data (city parameters, drones and parcels) to json .txt file."""

        data = {}
        data['wind'] = list(self.wind)
        data['position'] = [self.position.x, self.position.y]
        data['drones'] = []
        data['parcels'] = []

        for drone in self.drones:
            data['drones'].append({"number" : drone.number,
                                   "max_capacity" : drone.max_capacity,
                                   "max_speed" : drone.max_speed})
        for parcel in self.parcels:
            data['parcels'].append({"number" : parcel.number,
                                    "weight" : parcel.weight,
                                    "x" : parcel.position.x,
                                    "y" : parcel.position.y})

        with open(json_file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)


    def set_wind(self, wind):
        """Sets wind to given value."""

        if isinstance(wind, tuple) and len(wind) == 2:
            self.wind = wind
        else:
            raise TypeError


    def assign(self):
        """Assigns parcels at random among drones.""" # XXX initialization procedure

        for drone in self.drones:
            drone.parcels = []
        for parcel in self.parcels:
            drone = choice(self.drones)
            drone += parcel
        self._calculate_total_distance()


    def simulated_annealing(self, scale, temperature):
        """Performs simulated annealing algorithm."""

        prev_drones = [deepcopy(drone) for drone in self.drones]
        prev_distance = self.total_distance

        self._move(int(math.sqrt(math.sqrt(temperature)) - 3))
        print('Moving: ', int(math.sqrt(math.sqrt(temperature)) - 3))
        self._swap_neighbour(int(math.sqrt(math.sqrt(temperature))))
        print('Swapping: ', int(math.sqrt(math.sqrt(temperature))))
        # self.catch_neighbour()
        self.catch_neighbour_chain()

        self._calculate_total_distance()
        self.attempted_total_distances.append(self.total_distance)
        if self.total_distance < self.best_total_distance:
            self.best_total_distance = self.total_distance

        weird_value = math.e ** (scale * (prev_distance - self.total_distance) / temperature)
        print('Weird value:', weird_value)
        if weird_value > random():
            print('Passed.')
        else:
            print('Revert.')
            for i in range(len(self.drones)):
                self.drones[i] = prev_drones[i]
            self._calculate_total_distance()

        self.best_total_distances.append(self.best_total_distance)
        self.accepted_total_distances.append(self.total_distance)


    def _calculate_total_distance(self):
        """Returns total distance covered by drones."""

        # TODO Replace distance with time (distance tends to assign most parcels to single drone).
        self.total_distance = sum(drone.path_length for drone in self.drones)


    def _swap_neighbour(self, amount):
        """Swaps two neighbouring parcels in a random drone amount number of times."""

        for _ in range(amount):
            drone = choice(self.drones)
            if len(drone.parcels) > 1:
                i = randint(0, len(drone.parcels) - 2)
                drone.parcels[i], drone.parcels[i + 1] = drone.parcels[i + 1], drone.parcels[i]


    def catch_neighbour(self):
        """Insert closest neighbour into path before selected position."""

        d1 = choice(self.drones)
        p1_index = randint(0, len(d1.parcels) - 1)
        p1 = d1.parcels[p1_index]
        closest_parcel = p1

        closest_distance = math.inf

        for drone in self.drones:
            for parcel in drone.parcels:
                if parcel != p1:
                    new_dist = dist(p1.position, parcel.position)
                    if new_dist < closest_distance:
                        closest_parcel = parcel
                        closest_distance = new_dist

        if closest_parcel != p1:
            for drone in self.drones:
                for parcel_index in range(len(drone.parcels)):
                    parcel = drone.parcels[parcel_index]
                    if parcel == closest_parcel:
                        drone.parcels.pop(parcel_index)
                        d1.parcels.insert(p1_index + randint(0, 1), parcel) # TODO Make it insert randomly after or before.
                        return


    def catch_neighbour_chain(self):
        """Insert closest neighbour chain into path before selected position."""

        drone = choice(self.drones)
        neighbour = choice(self.drones)
        parcel1_index = randint(0, len(drone.parcels) - 1)
        parcel2_index = randint(0, len(neighbour.parcels) - 1)
        chain = []
        direction = randint(0, 1)
        amount = 0
        while len(neighbour.parcels) - 1 >= parcel2_index and amount <= int(len(neighbour.parcels) * betavariate(1, 5)):
            chain.append(neighbour.parcels[parcel2_index])
            neighbour.parcels.pop(parcel2_index)
            parcel2_index -= direction
            amount += 1
        offset = randint(0, 1)
        for parcel in choice([chain, reversed(chain)]): # or reversed chain
            drone.parcels.insert(parcel1_index + offset, parcel)
        print('Chain length:', amount)


    def _move(self, amount):
        """Moves random parcel between two random drones amount number of times."""

        for _ in range(amount):
            drone_from = choice(self.drones)
            drone_to = choice(self.drones)

            if not drone_from.parcels:
                continue

            parcel_pop_index = randint(0, len(drone_from.parcels) - 1)
            parcel_insert_index = randint(0, len(drone_to.parcels))

            drone_to.parcels.insert(parcel_insert_index, drone_from.parcels.pop(parcel_pop_index))





if __name__ == '__main__':

    city = City(position=Pos(0, 0), wind=(1, 2))
    city += Drone(1, 140, 8)
    city += Drone(2, 103, 15)

    for i in range(5):
        city += Parcel(i + 1, randint(10, 40), Pos(randint(-20, 20), randint(-20, 20)))

    print(city)
    print(city.total_distance)
    city.assign()
    print(city)
    print(city.total_distance)

    plots.show_parcels(city)
    plots.show_drone_paths(city)

    print(city.wind)
    city.set_wind((10, 20))
    print(city.wind)

    city.simulated_annealing(0.01, 1000)

    print(city.total_distance)
    print('Parcelki 0 :)', city.drones[0].parcels)
    print('Parcelki 1 :)', city.drones[1].parcels)
    print('Drone 0 length: ', city.drones[0].path_length)
    print('Drone 1 length: ', city.drones[1].path_length)
    city._swap_neighbour(1)
    city._calculate_total_distance()
    print(city.total_distance)
    print('Parcelki 0 :)', city.drones[0].parcels)
    print('Parcelki 1 :)', city.drones[1].parcels)
    print('Drone 0 length: ', city.drones[0].path_length)
    print('Drone 1 length: ', city.drones[1].path_length)
    plots.show_drone_paths(city)
