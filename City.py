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

    def __init__(self, position=Pos(0, 0), wind=(0, 0), metric='total_time'):
        self.metric = metric
        self.scale = None
        self.solution = None
        self.position = position
        self.wind = wind
        self.drones = []
        self.parcels = []
        self.total_cost = 0
        self.best_total_cost = inf
        self.total_costs = {'accepted' : [], 'attempted' : [], 'best' : []}

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
        string += '{:>20}'.format('Position')
        string += '{:>20}\n'.format('Weight')
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
            self += Parcel(parcel['number'], Pos(parcel['x'], parcel['y']), parcel['weight'])
        for drone in data['drones']:
            self += Drone(drone['number'], drone['max_capacity'], drone['max_speed'])

    def rload(self, raw_file_name):
        """Loads performance testing data from .txt file in raw format (used in test_tsp only)."""
        with open(os.path.join("test_TSP", "raw_test", raw_file_name)) as raw_file:
            data = raw_file.read().strip('\n')
        self.solution = int(data.split('\n')[0])
        self.parcels = []
        for line in data.split('\n')[1:]:
            parcel_number, pos_x, pos_y = line.split(' ')
            self += Parcel(int(parcel_number), Pos(float(pos_x), float(pos_y)))
            self.position = Pos(float(pos_x), float(pos_y)) # Base overlaps with last point.

    def cload(self, coord_file_name):
        """Loads data from GPS coordinates. The solutions are approximate due to conversion to
            xy coordinates (used in test_tsp only)."""
        with open(os.path.join("test_TSP", "coord_test", coord_file_name)) as coord_file:
            data = coord_file.read().strip('\n')
        self.solution = int(data.split('\n')[0])
        self.parcels = []
        th0 = mean(float(line.split(' ')[1]) for line in data.split('\n')[1:])
        for line in data.split('\n')[1:]:
            parcel_number, pos_x, pos_y = self.convert(line, th0)
            self += Parcel(parcel_number, Pos(pos_x, pos_y))
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
            self.total_cost = sum(drone.path_length for drone in self.drones)
        if self.metric == 'total_time':
            self.total_cost = max(drone.total_time for drone in self.drones)

    def calculate_scale(self):
        """Calculates scale according to data range."""
        max_x = max([parcel.position.x for parcel in self.parcels])
        max_y = max([parcel.position.y for parcel in self.parcels])
        min_x = min([parcel.position.x for parcel in self.parcels])
        min_y = min([parcel.position.y for parcel in self.parcels])
        self.scale = max(max_x - min_x, max_y - min_y)

    def test_everything(self, iterations=1000, initial_temperature=10, final_temperature=0.001):
        """Performs simulated annealing for all test cases and creates .txt file with summary."""
        # XXX not used so far.
        raw_test_cases = [f for f in os.listdir(os.path.join(os.getcwd(), "raw_test"))]
        coord_test_cases = [f for f in os.listdir(os.path.join(os.getcwd(), "coord_test"))]
        test_cases = raw_test_cases + coord_test_cases
        print(test_cases)
        test_file_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.csv')
        with open(os.path.join("test_results", test_file_name), 'w', newline='') as result_file:
            csvwriter = csv.writer(result_file)
            csvwriter.writerow(['iterations', 'initial_temperature', 'final_temperature'])
            csvwriter.writerow([iterations, initial_temperature, final_temperature])
            csvwriter.writerow(['test_case', 'result', 'solution', 'overshoot'])
            for test_case in test_cases:
                print("Testing", test_case)
                if test_case in raw_test_cases:
                    self.rload(test_case)
                if test_case in coord_test_cases:
                    self.cload(test_case)
                self.full_simulated_annealing(iterations=iterations,
                                              initial_temperature=initial_temperature,
                                              final_temperature=final_temperature,
                                              test=True)
                print(test_case, round(self.total_cost), self.solution)
                overshoot = round(100 * (self.total_cost - self.solution) / self.solution)
                print('Overshoot', overshoot, '%')
                csvwriter.writerow([test_case, str(round(self.total_cost)),
                                    str(self.solution), str(overshoot)])

    def test_tsp(self, iterations=1000, initial_temperature=10, final_temperature=0.001):
        """Classic TSP with no drone spec or parcel weight considered (known solutions)."""
        self.metric = 'simple'
        raw_test_cases = [f for f in os.listdir(os.path.join("test_TSP", "raw_test"))]
        coord_test_cases = [f for f in os.listdir(os.path.join("test_TSP", "coord_test"))]
        test_cases = raw_test_cases + coord_test_cases
        print(test_cases)
        test_file_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.csv')
        with open(os.path.join("test_TSP", "test_results", test_file_name), 'w', newline='') as result_file:
            csvwriter = csv.writer(result_file)
            csvwriter.writerow(['iterations', 'initial_temperature', 'final_temperature'])
            csvwriter.writerow([iterations, initial_temperature, final_temperature])
            csvwriter.writerow(['test_case', 'result', 'solution', 'overshoot'])
            for test_case in test_cases:
                print("Testing", test_case)
                if test_case in raw_test_cases:
                    self.rload(test_case)
                if test_case in coord_test_cases:
                    self.cload(test_case)
                self.full_simulated_annealing(iterations=iterations,
                                              initial_temperature=initial_temperature,
                                              final_temperature=final_temperature,
                                              test=True)
                print(test_case, round(self.total_cost), self.solution)
                overshoot = round(100 * (self.total_cost - self.solution) / self.solution)
                print('Overshoot', overshoot, '%')
                csvwriter.writerow([test_case, str(round(self.total_cost)),
                                    str(self.solution), str(overshoot)])

    def full_simulated_annealing(self, initial_temperature=10, final_temperature=0.001,
                                 iterations=10_000, test=False):
        """Loops over sim annealing."""
        cooling_rate = pow(final_temperature / initial_temperature, 1 / iterations)
        self.prepare_algorithm()
        plots.show_parcels(self, test=test)
        plots.show_drone_paths(self, test=test)
        prev_best = self.total_cost
        prev = self.total_cost
        temperature = initial_temperature
        while temperature > final_temperature:
            self.iteration(temperature, test=test)
            if not test:
                print('Now', round(self.total_cost), 'Before', round(prev), 'Best',
                      round(prev_best), 'Temp', temperature, '\n')
            temperature *= cooling_rate
            prev = self.total_cost
            if self.total_cost < prev_best:
                plots.show_drone_paths(self, test=test)
                prev_best = self.total_cost
        plots.show_drone_paths(self, final=True, test=test)
        plots.show_distance_history(self, test=test)

    def iteration(self, temperature, test=False):
        """Performs one iteration of simulated annealing algorithm."""
        # XXX needs slight refactoring.
        previous_drones, previous_distance = self.save()
        choice([choice(self.drones).twoopt, self.reinsert_parcel])()
        self.calculate_cost()
        self.total_costs['attempted'].append(self.total_cost)
        if self.total_cost < self.best_total_cost:
            self.best_total_cost = self.total_cost
        improvement = previous_distance - self.total_cost
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
        self.total_costs['best'].append(self.best_total_cost)
        self.total_costs['accepted'].append(self.total_cost)

    def save(self):
        """Save drones' state."""
        return [deepcopy(drone) for drone in self.drones], self.total_cost

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
