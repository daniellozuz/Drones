"""Module provides plotting functions, which take city as an argument."""


import matplotlib.pyplot as plt
import csv
import os


def show_parcels(city):
    """Shows parcels on a map (for now overlaps drone paths)."""
    x_positions = [parcel.position.x for parcel in city.parcels]
    y_positions = [parcel.position.y for parcel in city.parcels]
    plt.plot(x_positions, y_positions, 'ro')
    plt.plot(city.position.x, city.position.y, 'go')


def show_drone_paths(city, final=False):
    """Shows drones paths on a map."""
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


def show_distance_and_modification_history(city):
    """Plots consecutive iterations of an angorithm."""
    plt.ioff()
    plt.clf()
    plt.subplot(211)
    handles = []
    for key, value in city.total_distances.items():
        handles.extend(plt.plot(value, label=str(key), alpha=0.7))
    plt.legend(handles=handles)
    plt.subplot(212)
    handles = []
    for key, value in city.stats.items():
        if str(key) != 'neighbour_chain_lengths':
            handles.extend(plt.plot(value, label=str(key)))
    plt.legend(handles=handles, loc=1)
    plt.show()


def show_test_results():
    """Plots all test results."""
    result_files = [f for f in os.listdir(os.path.join(os.getcwd(), 'test_results'))]
    handles = []
    for result_file in result_files:
        if result_file.endswith('.csv'):
            with open(os.path.join('test_results', result_file)) as a_file:
                reader = csv.reader(a_file)
                data = []
                legend = []
                for row in reader:
                    if len(row) == 3:
                        legend.append(row)
                    else:
                        data.append(row[3])
            data = [int(item) for item in data[1:]]
            label = [str(v1) + '=' + str(v2) for v1, v2 in zip(legend[0], legend[1])]
            label = ' '.join(label)
            handles.extend(plt.plot(data, label=label))
    plt.legend(handles=handles, loc=1)
    plt.show()
