from Drone import Drone
from Parcel import Parcel


class City(object):
    '''Class implements city creation, access to drones and parcels, and drone trajectories.'''


    def __init__(self, wind):
        '''Creates a city, initialized with wind and empty drone and parcels lists.'''

        self.drones = []
        self.parcels = []
        self.wind = wind


    def __add__(self, item):
        '''Appends a drone or parcel to iternal parcels or drones lists.'''

        if type(item) == Drone:
            #print('A drone added.')
            self.drones.append(item)
            return self

        if type(item) == Parcel:
            #print('A parcel added.')
            self.parcels.append(item)
            return self


    def __str__(self):
        '''Provides printing of a city'''

        string = '=' * 40 + ' City description ' + '=' * 40
        string += "\nWind's strength: {wind}\n".format(wind=self.wind)

        string += '\nThere are {amount} drones in the city:\n'.format(amount=len(self.drones))
        for drone in self.drones:
            string += str(drone)

        string += '\nThere are {amount} parcels in the city:\n'.format(amount=len(self.parcels))
        for parcel in self.parcels:
            string += str(parcel)

        return string



if __name__ == '__main__':

    city = City(wind=(1, 2))
    city += Drone(1, 4, 8)
    city += Drone(2, 13, 15)
    city += Parcel(1, 20, (1, 2))
    city += Parcel(2, 15, (0, 7))
    city += Parcel(3, 5, (-1, -5))

    print(city)
