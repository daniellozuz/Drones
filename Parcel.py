class Parcel(object):
    '''Class implements parcel creation and specification.
    
    Normally Parcels would be assigned to a City, then within that city, assigned to drones.
    '''

    # I would probably get rid of it in the future (redundancy - City has it).
    parcel_list = []


    def __init__(self, _id, weight, position):
        '''Creates a parcel and appends it to internal parcel_list.'''

        self._id = _id
        self.weight = weight
        self.position = position
        Parcel.parcel_list.append(self)


    def __str__(self):
        '''Provides printing of a single parcel.'''

        string = 'Parcel ID: {:>5}\n'.format(self._id)
        string += 'Weight: {:>10}\n'.format(self.weight)
        string += 'Position: {:>15}\n'.format(str(self.position))
        return string


    def __repr__(self):
        '''Provides printing of all parcel in internal parcel_list.'''

        string = 'Parcel ID: {:>5}\n'.format(self._id)
        string += 'Weight: {:>10}\n'.format(self.weight)
        string += 'Position: {:>15}\n'.format(str(self.position))
        return string


if __name__ == '__main__':
    p1 = Parcel(1, 5, (1, 1))
    p2 = Parcel(2, 9, (3, 5))
    print(p1)
    print(p1._id)
    #print(p2)
    print(Parcel.parcel_list)
