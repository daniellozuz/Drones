class Drone(object):
    '''Class implements drone creation and specification.'''


    def __init__(self, _id, max_capacity, max_speed, parcels=[]):
        '''Creates a drone and appends it to internal drone_list.'''

        self._id = _id
        self.max_capacity = max_capacity
        self.max_speed = max_speed
        self.parcels = parcels
        self.path = []
        self.path_length = 0


    def __add__(self, parcel):
        '''Assigns a parcel to a drone.'''

        self.parcels.append(parcel)
        return self


    def __str__(self):
        '''Provides printing of a single drone.'''

        string = 'Drone ID: {:>6}\n'.format(self._id)
        string += 'Max capacity: {:>4}\n'.format(self.max_capacity)
        string += 'Max speed: {:>7}\n'.format(self.max_speed)
        string += 'Parcels assigned: {:>4}\n'.format(len(self.parcels))
        return string


    def __repr__(self):
        '''Provides printing of all drones in internal drone_list.'''

        string = 'Drone ID: {:>6}\n'.format(self._id)
        string += 'Max capacity: {:>4}\n'.format(self.max_capacity)
        string += 'Max speed: {:>7}\n'.format(self.max_speed)
        string += 'Parcels assigned: {:>4}\n'.format(len(self.parcels))
        return string
    

    def update(self, base=(0, 0)):
        """Recalculates drone's parameters after modifications/alterations."""

        occupied_capacity = 0
        self.path = [base]
        for parcel in self.parcels:
            occupied_capacity += parcel.weight
            if occupied_capacity > self.max_capacity:
                self.path.append(base)
                occupied_capacity = 0
            self.path.append(parcel.position)
        self.path.append(base)

        self.recalculate_path_length()


    def recalculate_path_length(self):
        """Recalculates path length."""

        dist = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5

        self.path_length = 0
        for point1, point2 in zip(self.path[:-1], self.path[1:]):
            self.path_length += dist(point1, point2)



if __name__ == '__main__':
    d1 = Drone(1, 10, 20)
    d2 = Drone(2, 13, 15)
    print(d1)
    print(d1._id)
    #print(d2)
    print(Drone.drone_list)
