"""Provides parcel implementation."""

class Parcel(object):
    """Provides parcel implementation."""

    def __init__(self, number, position, weight=0):
        self.number = number
        self.position = position
        self.weight = weight

    def __str__(self):
        string = '{:>20}'.format(self.number)
        string += '{:>20}'.format(str(self.position))
        string += '{:>20}\n'.format(self.weight)
        return string

    def __repr__(self):
        string = 'Number: {}, '.format(self.number)
        string += 'Position: {}, '.format(str(self.position))
        string += 'Weight: {}\n'.format(self.weight)
        return string
