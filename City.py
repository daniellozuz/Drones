"""This class serves as a data representation of the whole system.

    Calling its methods enables:
        - city parameters specification - wind, base(s) position,
        - drone and parcel creation,
        - numerical computations - rearranging parcels among drones and recalculating results."""


from copy import deepcopy
from itertools import permutations
import json
import math
from random import choice, randint, random, randrange, betavariate, sample
import os

from common import Position as Pos
from common import dist
from Drone import Drone
from Parcel import Parcel
import plots


class City():
    """Main interface with the data."""


    def __init__(self, position=Pos(0, 0), wind=(0, 0)):
        self.scale = 1000
        self.solution = 0
        self.position = position
        self.wind = wind
        self.drones = []
        self.parcels = []
        self.total_distance = 0
        self.best_total_distance = math.inf
        self.accepted_total_distances = []
        self.attempted_total_distances = []
        self.best_total_distances = [] # TODO list(accumulate(best_total_distances, min)) - similar?


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


    def jload(self, json_file_name):
        """Loads data from json .txt file stored in "test_json" folder."""
        with open(os.path.join("json_test", json_file_name)) as json_file:
            data = json.load(json_file)
        self.wind = tuple(data['wind'])
        self.position = Pos(data['position'][0], data['position'][1])
        self.parcels = []
        self.drones = []
        for parcel in data['parcels']:
            self += Parcel(parcel['number'], parcel['weight'], Pos(parcel['x'], parcel['y']))
        for drone in data['drones']:
            self += Drone(drone['number'], drone['max_capacity'], drone['max_speed'])


    def rload(self, raw_file_name):
        """Loads testing data from .txt file in raw format (used for testing algorithm performance)."""
        with open(os.path.join("raw_test", raw_file_name)) as raw_file:
            data = raw_file.read()
        self.wind = tuple([0, 0])
        self.parcels = []
        self.solution = int(data.strip('\n').split('\n')[0])
        for line in data.strip('\n').split('\n')[1:]:
            parcel_number, pos_x, pos_y = line.split(' ')
            self += Parcel(int(parcel_number), 1, Pos(float(pos_x), float(pos_y)))
            self.position = Pos(float(pos_x), float(pos_y)) # Base overlaps with one point.


    def jstore(self, json_file_name):
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
        with open(os.path.join("json_test", json_file_name), 'w') as json_file:
            json.dump(data, json_file, indent=4)


    def set_wind(self, wind):
        """Sets wind to given value."""
        if isinstance(wind, tuple) and len(wind) == 2:
            self.wind = wind
        else:
            raise TypeError


    def assign(self):
        """Assigns parcels at random among drones.""" # XXX make it initialization procedure
        for drone in self.drones:
            drone.parcels = []
        for parcel in sample(self.parcels, len(self.parcels)):
            drone = choice(self.drones)
            drone += parcel
        self.calculate_total_distance()
        max_x = max([parcel.position.x for parcel in self.parcels])
        max_y = max([parcel.position.y for parcel in self.parcels])
        min_x = min([parcel.position.x for parcel in self.parcels])
        min_y = min([parcel.position.y for parcel in self.parcels])
        self.scale = max(max_x - min_x, max_y - min_y)


    def calculate_total_distance(self):
        """Returns total distance covered by drones."""
        # TODO Replace distance with time (distance tends to assign most parcels to single drone).
        self.total_distance = sum(drone.path_length for drone in self.drones)


    def full_simulated_annealing(self, initial_temperature=1000, final_temperature=0.1):
        """Loops over sim annealing."""
        temperature = initial_temperature
        prev_best = self.total_distance
        prev = self.total_distance
        while temperature > final_temperature:
            self.simulated_annealing(temperature)
            print('Now', round(self.total_distance), 'Before', round(prev), 'Best', round(prev_best), 'Temp', temperature)
            print('\n')
            temperature *= 0.9997
            prev = self.total_distance
            if self.total_distance < prev_best:
                plots.show_drone_paths(self)
                prev_best = self.total_distance


    def simulated_annealing(self, temperature):
        """Performs one iteration of simulated annealing algorithm."""
        # TODO needs major refactoring.
        previous_drones = [deepcopy(drone) for drone in self.drones]
        previous_distance = self.total_distance
        self.randomly_reinsert_parcels_between_drones(int(math.sqrt(math.sqrt(temperature)) - 3))
        self.randomly_reinsert_parcels_in_a_drone(int(math.sqrt(math.sqrt(temperature)) - 3))
        self.swap_two_adjacent(int(math.sqrt(math.sqrt(temperature))))
        self.swallow_neighbour()
        self.catch_neighbour_chain(int(30 * betavariate(1, 5))) # TODO change 30 into sth appropriate
        self.calculate_total_distance()
        self.attempted_total_distances.append(self.total_distance)
        if self.total_distance < self.best_total_distance:
            self.best_total_distance = self.total_distance
        weird_value = math.e ** (10 * len(self.parcels) * (previous_distance - self.total_distance) / (temperature * self.scale))
        print('Weird value:', weird_value)
        if weird_value > random():
            print('Passed.')
        else:
            print('Revert.')
            for i in range(len(self.drones)):
                self.drones[i] = previous_drones[i]
            self.calculate_total_distance()
        self.best_total_distances.append(self.best_total_distance)
        self.accepted_total_distances.append(self.total_distance)


    def swap_two_adjacent(self, amount):
        """Swaps two adjacent parcels in a random drone's path amount number of times."""
        for _ in range(amount):
            drone = choice(self.drones)
            if len(drone.parcels) > 1:
                i = randrange(0, len(drone.parcels) - 1)
                drone.parcels[i], drone.parcels[i + 1] = drone.parcels[i + 1], drone.parcels[i]


    def swallow_neighbour(self):
        """Insert closest neighbour into path before or after selected parcel."""
        to_drone = choice(self.drones)
        selected_parcel_index = randrange(0, len(to_drone.parcels))
        selected_parcel = to_drone.parcels[selected_parcel_index]
        closest_parcel, from_drone = self.get_closest_neighbour_info(selected_parcel)
        from_drone.parcels.remove(closest_parcel)
        to_drone.parcels.insert(selected_parcel_index + randint(0, 1), closest_parcel)


    def get_closest_neighbour_info(self, selected_parcel):
        """Returns selected_parcel's closest neighbour and drone to which it belonged."""
        closest_distance = math.inf
        for drone in self.drones:
            for neighbour in drone.parcels:
                if neighbour != selected_parcel:
                    new_dist = dist(selected_parcel.position, neighbour.position)
                    if new_dist < closest_distance:
                        closest_distance = new_dist
                        closest_parcel, from_drone = neighbour, drone
        return closest_parcel, from_drone


    def catch_neighbour_chain(self, max_length):
        """Reinserts chain of parcels (maximum max_length parcels) from one drone to another, preserving order - reversing or not."""
        # TODO needs major refactoring.
        selected_drone = choice(self.drones)
        neighbour = choice(self.drones)
        if not neighbour.parcels or not selected_drone.parcels:
            return
        selected_drone_parcel_index = randrange(0, len(selected_drone.parcels))
        neighbour_parcel_index = randrange(0, len(neighbour.parcels))
        parcel_chain = []
        direction = randint(0, 1)
        amount = 0
        while len(neighbour.parcels) - 1 >= neighbour_parcel_index and amount <= max_length and amount <= len(neighbour.parcels):
            parcel_chain.append(neighbour.parcels[neighbour_parcel_index])
            neighbour.parcels.pop(neighbour_parcel_index)
            neighbour_parcel_index -= direction
            amount += 1
        offset = randint(0, 1)
        for parcel in choice([parcel_chain, reversed(parcel_chain)]):
            selected_drone.parcels.insert(selected_drone_parcel_index + offset, parcel)
        print('Chain length:', amount)


    def randomly_reinsert_parcels_between_drones(self, amount):
        """Moves random parcel between random drones amount number of times."""
        for _ in range(amount):
            from_drone = choice(self.drones)
            if not from_drone.parcels:
                continue
            to_drone = choice(self.drones)
            pop_index = randrange(0, len(from_drone.parcels))
            insert_index = randint(0, len(to_drone.parcels))
            to_drone.parcels.insert(insert_index, from_drone.parcels.pop(pop_index))


    def randomly_reinsert_parcels_in_a_drone(self, amount):
        """Moves random parcel in a drone to another position amount number of times."""
        for _ in range(amount):
            drone = choice(self.drones)
            if not drone.parcels:
                continue
            pop_index = randrange(0, len(drone.parcels))
            insert_index = randint(0, len(drone.parcels))
            drone.parcels.insert(insert_index, drone.parcels.pop(pop_index))
    

    def final_sweep(self, length=4):
        """Performs final optimization (selects length points in series and selects their best ordering), repeated for all points."""
        # TODO Should not randomly choose index, instead it should go through every index in drone. If drone has less than length parcels it should devour what is available.
        for drone in self.drones:
            i = choice(range(0, len(drone.parcels) - length))
            previous_drones = [deepcopy(dr) for dr in self.drones]
            previous_distance = self.total_distance
            chain = []
            print('Popping 3 to create a chain.')
            for _ in range(length):
                chain.append(drone.parcels.pop(i))
            print(chain)
            print(len(drone.parcels))
            better = False
            for p in permutations(chain, len(chain)):
                print('Inserting 3 to try one of permutations.')
                for par in p:
                    drone.parcels.insert(i, par)
                print('Permutation:', p)
                print(len(drone.parcels))
                self.calculate_total_distance()
                distance = self.total_distance
                if distance < previous_distance:
                    better = True
                    print('Better!')
                    break
                else:
                    print('Popping 3 because this perutation did not work.')
                    for _ in range(length):
                        drone.parcels.pop(i)
                self.calculate_total_distance()
            # Revert
            if not better:
                print('Reverting because no permutation was better.')
                print('Amount of parcels before revert:', len(drone.parcels))
                for k in range(len(self.drones)):
                    self.drones[k] = previous_drones[k]
                self.calculate_total_distance()
                break





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

    city.simulated_annealing(1000)

    print(city.total_distance)
    print('Parcelki 0 :)', city.drones[0].parcels)
    print('Parcelki 1 :)', city.drones[1].parcels)
    print('Drone 0 length: ', city.drones[0].path_length)
    print('Drone 1 length: ', city.drones[1].path_length)
    city.swap_two_adjacent(1)
    city.calculate_total_distance()
    print(city.total_distance)
    print('Parcelki 0 :)', city.drones[0].parcels)
    print('Parcelki 1 :)', city.drones[1].parcels)
    print('Drone 0 length: ', city.drones[0].path_length)
    print('Drone 1 length: ', city.drones[1].path_length)
    plots.show_drone_paths(city)
