"""Provides parcel implementation."""


class Parcel(object):
    """Provides parcel implementation."""


    def __init__(self, number, weight, position):
        self.number = number
        self.weight = weight
        self.position = position


    def __str__(self):
        string = '{:>20}'.format(self.number)
        string += '{:>20}'.format(self.weight)
        string += '{:>20}\n'.format(str(self.position))
        return string


    def __repr__(self):
        string = 'Number: {}, '.format(self.number)
        string += 'Weight: {}, '.format(self.weight)
        string += 'Position: {}\n'.format(str(self.position))
        return string
