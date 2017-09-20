import matplotlib.pyplot as plt


def show_parcels(city):
    '''Shows parcels on a map.'''

    xcoord = [ele.position[0] for ele in city.parcels]
    ycoord = [ele.position[1] for ele in city.parcels]

    plt.plot(xcoord, ycoord, 'ro')
    plt.plot(city.position[0], city.position[1], 'go')
    plt.title('City map')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


def show_drone_paths(city):
    '''Shows drones paths on a map.'''

    for drone in city.drones:
        occupied_capacity = 0
        path = [city.position]
        for parcel in drone.parcels:
            occupied_capacity += parcel.weight
            if occupied_capacity > drone.max_capacity:
                path.append(city.position)
                occupied_capacity = 0
            path.append(parcel.position)
        path.append(city.position)
        if path:
            plt.plot(*zip(*path))
    plt.show()
