class Drone(object):
    '''Class implements drone creation and specification.'''


    drone_list = []


    def __init__(self, _id, max_capacity, max_speed):
        '''Creates a drone and appends it to internal drone_list.'''

        self._id = _id
        self.max_capacity = max_capacity
        self.max_speed = max_speed
        Drone.drone_list.append(self)


    def __str__(self):
        '''Provides printing of a single drone.'''

        string = 'Drone ID: {:>6}\n'.format(self._id)
        string += 'Max capacity: {:>4}\n'.format(self.max_capacity)
        string += 'Max speed: {:>7}\n'.format(self.max_speed)
        return string


    def __repr__(self):
        '''Provides printing of all drones in internal drone_list.'''

        string = 'Drone ID: {:>6}\n'.format(self._id)
        string += 'Max capacity: {:>4}\n'.format(self.max_capacity)
        string += 'Max speed: {:>7}\n'.format(self.max_speed)
        return string


if __name__ == '__main__':
    d1 = Drone(1, 10, 20)
    d2 = Drone(2, 13, 15)
    print(d1)
    print(d1._id)
    #print(d2)
    print(Drone.drone_list)
