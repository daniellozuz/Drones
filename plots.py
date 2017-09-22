import matplotlib.pyplot as plt


def show_parcels(city):
    """Shows parcels on a map (for now overlaps drone paths)."""

    xcoord = [ele.position[0] for ele in city.parcels]
    ycoord = [ele.position[1] for ele in city.parcels]

    plt.plot(xcoord, ycoord, 'ro')
    plt.plot(city.position[0], city.position[1], 'go')


def show_drone_paths(city):
    """Shows drones paths on a map."""
    # TODO Legend.
    # TODO Just plot drone.path
    #plt.ion()
    plt.clf()
    for drone in city.drones:
        if drone.path:
            plt.plot(*zip(*drone.path))
        else:
            print("Error: no path to be displayed.")
    plt.title('Total distance: ' + str(round(city.total_distance, 2)))
    plt.show()
    show_parcels(city)
    plt.pause(0.05)


def show_distance_history(city):
    """Plots consecutive iterations of an angorithm."""

    plt.ioff()
    plt.clf()
    plt.plot(range(len(city.total_distances)), city.total_distances)
    plt.show()
