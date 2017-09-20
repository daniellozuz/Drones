import math
import random


def alg_random(drones, parcels, base):
    '''Distributes parcels to drones at random and returns total distance.'''

    for drone in drones:
        drone.parcels = []
    for parcel in parcels:
        ind = random.randint(0, len(drones) - 1)
        drones[ind] += parcel
    return calculate_total_distance(drones, base)


def calculate_total_distance(drones, base):
    '''Returns total distance covered by drones.'''

    distance = 0
    for drone in drones:
        distance += calculate_distance(drone, base)
    return distance


def calculate_distance(drone, base):
    '''Returns distance covered by a single drone.'''

    if not drone.parcels:
        return 0
    distance = 0
    occupied_capacity = 0
    drone_pos = base
    for ind in range(len(drone.parcels) - 1):
        distance += dist(drone_pos, drone.parcels[ind].position)
        occupied_capacity += drone.parcels[ind].weight
        drone_pos = drone.parcels[ind].position
        if ind < len(drone.parcels) - 1 and occupied_capacity + drone.parcels[ind + 1].weight > drone.max_capacity:
            distance += dist(drone_pos, base)
            occupied_capacity = 0
            drone_pos = base
    distance += dist(drone_pos, base)
    return distance


def dist(p1, p2):
    '''Returns distance between two points.'''

    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


if __name__ == '__main__':
    from Drone import Drone
    from Parcel import Parcel

    drones = [Drone(1, 40, 8), Drone(2, 30, 7)]
    parcels = [Parcel(1, 2, (3, 4)), Parcel(2, 5, (7, 12))]
    base = (0, 0)
    alg_random(drones, parcels, base)
