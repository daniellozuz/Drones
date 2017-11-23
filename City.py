"""Engine."""

import datetime
import json
import os
from copy import deepcopy
from math import cos, radians, inf, e
from random import choice, randint, random, randrange, sample
from statistics import mean
import csv

from common import Position as Pos
from Drone import Drone
from Parcel import Parcel
import plots


class City():
    """Engine implementation and main interface."""

    def __init__(self, position=Pos(0, 0), wind=(0, 0), metric='simple'):
        self.metric = metric
        self.scale = None
        self.solution = None
        self.position = position
        self.wind = wind
        self.drones = []
        self.parcels = []
        self.total_distance = 0
        self.best_total_distance = inf
        self.total_distances = {'accepted' : [], 'attempted' : [], 'best' : []}

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
        """Loads performance testing data from .txt file in raw format."""
        with open(os.path.join("raw_test", raw_file_name)) as raw_file:
            data = raw_file.read().strip('\n')
        self.solution = int(data.split('\n')[0])
        self.parcels = []
        for line in data.split('\n')[1:]:
            parcel_number, pos_x, pos_y = line.split(' ')
            self += Parcel(int(parcel_number), 1, Pos(float(pos_x), float(pos_y)))
            self.position = Pos(float(pos_x), float(pos_y)) # Base overlaps with last point.

    def cload(self, coord_file_name):
        """Loads data from GPS coordinates. The solutions are approximate due to conversion to
            xy coordinates."""
        with open(os.path.join("coord_test", coord_file_name)) as coord_file:
            data = coord_file.read().strip('\n')
        self.solution = int(data.split('\n')[0])
        self.parcels = []
        th0 = mean(float(line.split(' ')[1]) for line in data.split('\n')[1:])
        for line in data.split('\n')[1:]:
            parcel_number, pos_x, pos_y = self.convert(line, th0)
            self += Parcel(parcel_number, 0.0001, Pos(pos_x, pos_y))
            self.position = Pos(pos_x, pos_y) # Base overlaps with last point.

    def convert(self, line, th0):
        """Converts a line into a tuple: (number, pox_x, pos_y)."""
        parcel_number, latitude, longitude = line.split(' ')
        earth_radius = 6371000
        pos_x = round(earth_radius * radians(float(longitude)) * cos(radians(th0)))
        pos_y = round(earth_radius * radians(float(latitude)))
        return int(parcel_number), pos_x, pos_y

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
        with open(os.path.join("json_test", json_file_name), 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def prepare_algorithm(self):
        """Initialization procedure to prepare simulated annealing algorithm."""
        self.reassign_parcels()
        self.calculate_cost()
        self.calculate_scale()

    def reassign_parcels(self):
        """Reassigns parcels among drones at random."""
        for drone in self.drones:
            drone.parcels = []
        for parcel in sample(self.parcels, len(self.parcels)):
            drone = choice(self.drones)
            drone += parcel

    def calculate_cost(self):
        """Returns total distance or time covered by drones (depending on metric used)."""
        if self.metric == 'simple':
            self.total_distance = sum(drone.path_length for drone in self.drones)
        if self.metric == 'total_time':
            self.total_distance = max(drone.total_time for drone in self.drones)

    def calculate_scale(self):
        """Calculates scale according to data range."""
        max_x = max([parcel.position.x for parcel in self.parcels])
        max_y = max([parcel.position.y for parcel in self.parcels])
        min_x = min([parcel.position.x for parcel in self.parcels])
        min_y = min([parcel.position.y for parcel in self.parcels])
        self.scale = max(max_x - min_x, max_y - min_y)

    def test_everything(self, cooling_rate=0.99, initial_temperature=1000, final_temperature=0.1):
        """Performs simulated annealing for all test cases and creates .txt file with summary."""
        raw_test_cases = [f for f in os.listdir(os.path.join(os.getcwd(), "raw_test"))]
        coord_test_cases = [f for f in os.listdir(os.path.join(os.getcwd(), "coord_test"))]
        test_cases = raw_test_cases + coord_test_cases
        print(test_cases)
        test_file_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.csv')
        with open(os.path.join("test_results", test_file_name), 'w', newline='') as result_file:
            csvwriter = csv.writer(result_file)
            csvwriter.writerow(['cooling_rate', 'initial_temperature', 'final_temperature'])
            csvwriter.writerow([cooling_rate, initial_temperature, final_temperature])
            csvwriter.writerow(['test_case', 'result', 'solution', 'overshoot'])
            for test_case in test_cases:
                print("Testing", test_case)
                if test_case in raw_test_cases:
                    self.rload(test_case)
                if test_case in coord_test_cases:
                    self.cload(test_case)
                self.full_simulated_annealing(cooling_rate=cooling_rate, initial_temperature=1000,
                                              final_temperature=0.1, test=True)
                print(test_case, round(self.total_distance), self.solution)
                overshoot = round(100 * (self.total_distance - self.solution) / self.solution)
                print('Overshoot', overshoot, '%')
                csvwriter.writerow([test_case, str(round(self.total_distance)),
                                    str(self.solution), str(overshoot)])

    def full_simulated_annealing(self, initial_temperature=1000, final_temperature=0.1,
                                 cooling_rate=0.9997, test=False):
        """Loops over sim annealing."""
        self.prepare_algorithm()
        if not test:
            plots.show_parcels(self)
            plots.show_drone_paths(self)
        prev_best = self.total_distance
        prev = self.total_distance
        temperature = initial_temperature
        while temperature > final_temperature:
            self.iteration(temperature, test=test)
            if not test:
                print('Now', round(self.total_distance), 'Before', round(prev), 'Best',
                      round(prev_best), 'Temp', temperature, '\n')
            temperature *= cooling_rate
            prev = self.total_distance
            if self.total_distance < prev_best:
                if not test:
                    plots.show_drone_paths(self)
                prev_best = self.total_distance
        if not test:
            plots.show_drone_paths(self, final=True)
            plots.show_distance_history(self)

    def iteration(self, temperature, test=False):
        """Performs one iteration of simulated annealing algorithm."""
        # XXX needs slight refactoring.
        previous_drones, previous_distance = self.save()
        choice([choice(self.drones).twoopt, self.reinsert_parcel])()
        self.calculate_cost()
        self.total_distances['attempted'].append(self.total_distance)
        if self.total_distance < self.best_total_distance:
            self.best_total_distance = self.total_distance
        improvement = previous_distance - self.total_distance
        acceptance = e ** min(100, improvement / (temperature * self.scale))
        if not test:
            print('Weird value:', acceptance)
        if acceptance > random():
            if not test:
                print('Passed.')
        else:
            if not test:
                print('Revert.')
            self.revert(previous_drones)
        self.total_distances['best'].append(self.best_total_distance)
        self.total_distances['accepted'].append(self.total_distance)

    def save(self):
        """Save drones' state."""
        return [deepcopy(drone) for drone in self.drones], self.total_distance

    def revert(self, previous_drones):
        """Reverts drones' state into previous state."""
        for i in range(len(self.drones)):
            self.drones[i] = previous_drones[i]
        self.calculate_cost()

    def reinsert_parcel(self):
        """Moves a random parcel between two random drones."""
        from_drone = choice(self.drones)
        if not from_drone.parcels:
            return
        to_drone = choice(self.drones)
        pop_index = randrange(0, len(from_drone.parcels))
        insert_index = randint(0, len(to_drone.parcels))
        to_drone.parcels.insert(insert_index, from_drone.parcels.pop(pop_index))
