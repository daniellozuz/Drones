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
