from collections import namedtuple


Position = namedtuple('Position', ['x', 'y'])


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





if __name__ == '__main__':
    p1 = Parcel(1, 5, Position(1, 1))
    p2 = Parcel(2, 9, Position(3, 5))
    print(p1)
    print(p1.number)
