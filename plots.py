"""Module provides plotting functions, which take city as an argument."""


import matplotlib.pyplot as plt


def show_parcels(city):
    """Shows parcels on a map (for now overlaps drone paths)."""
    x_positions = [parcel.position.x for parcel in city.parcels]
    y_positions = [parcel.position.y for parcel in city.parcels]
    plt.plot(x_positions, y_positions, 'ro')
    plt.plot(city.position.x, city.position.y, 'go')


def show_drone_paths(city, final=False):
    """Shows drones paths on a map."""
    # TODO Legend.
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
        plt.title('Total distance: ' + str(round(city.total_distance)) + ' Solution: ' + str(city.solution) + ' (+' + str(percentage) + '% overshoot)')
    else:
        plt.title('Total distance: ' + str(round(city.total_distance)))
    plt.show()
    show_parcels(city)
    plt.pause(0.05)


def show_distance_history(city):
    """Plots consecutive iterations of an angorithm."""
    plt.ioff()
    plt.clf()
    plt.plot(range(len(city.stats['attempted_total_distances'])), city.stats['attempted_total_distances'])
    plt.plot(range(len(city.stats['accepted_total_distances'])), city.stats['accepted_total_distances'])
    plt.plot(range(len(city.stats['best_total_distances'])), city.stats['best_total_distances'], 'g')
    plt.show()
