"""Module provides plotting functions, which take city as an argument."""

import csv
import os
import matplotlib.pyplot as plt

def show_parcels(city, test=False):
    """Shows parcels on a map (for now overlaps drone paths)."""
    if test:
        return
    x_positions = [parcel.position.x for parcel in city.parcels]
    y_positions = [parcel.position.y for parcel in city.parcels]
    plt.plot(x_positions, y_positions, 'ro')
    plt.plot(city.position.x, city.position.y, 'go')

def show_drone_paths(city, final=False, test=False):
    """Shows drones paths on a map."""
    if test:
        return
    plt.ion()
    if final:
        plt.ioff()
    plt.axis('equal')
    plt.clf()
    for drone in city.drones:
        if drone.path:
            plt.plot(*zip(*drone.path))
        else:
            print("Error: no path to be displayed.")
    if city.solution:
        percentage = int(100 * (city.total_distance - city.solution) / city.solution)
        plt.title('Total distance: ' + str(round(city.total_distance)) + ' Solution: ' +\
                  str(city.solution) + ' (+' + str(percentage) + '% overshoot)')
    else:
        plt.title('Total distance: ' + str(round(city.total_distance)))
    plt.show()
    show_parcels(city)
    plt.pause(0.05)

def show_distance_history(city, test=False):
    """Plots consecutive iterations of an angorithm."""
    if test:
        return
    plt.ioff()
    plt.clf()
    for key, value in city.total_distances.items():
        plt.plot(value, label=str(key), alpha=0.7)
    plt.legend()
    plt.show()

def show_test_results():
    """Plots all test results."""
    result_files = [f for f in os.listdir('test_results') if f.endswith('.csv')]
    for result_file in result_files:
        with open(os.path.join('test_results', result_file)) as test_result:
            reader = csv.reader(test_result)
            data = []
            legend = []
            for row in reader:
                if len(row) == 3:
                    legend.append(row)
                else:
                    data.append(row[3])
        data = [int(item) for item in data[1:]]
        label = ' '.join([str(v1) + '=' + str(v2) for v1, v2 in zip(legend[0], legend[1])])
        plt.plot(data, label=label)
    plt.legend()
    plt.show()
