from shapely.geometry import Polygon, Point
import numpy as np
import matplotlib.pyplot as plt
import math
import random

random.seed(0)

FREQUENCY = 2.4*(10**9)
TRANSMITTED_POWER = 20

class Phone:
    def __init__(self, x, y, frequency, transmitted_power):
        """the phone class that would represent a phone emitting an RF signal

        Args:
            x (float): =x position
            y (float): y position
            frequency (hz): the frequency of the phone signal
            transmitted_power (dbm): the signal strength of the phone at 1m
        """
        self.x = x
        self.y = y
        self.frequency = frequency
        self.transmitted_power = transmitted_power
    
    def calculate_distance(self, drone_pos):
        """calculates the distance between the drone and the phone

        Args:
            drone_pos (a list of float): x y and z values of the drone position

        Returns:
            float: the distance between the drone and the phone 
        """
        drone_pos = np.array(drone_pos)
        phone_pos = np.array([self.x, self.y, 0])

        distance = np.linalg.norm(drone_pos - phone_pos)

        return distance

    def calculate_rssi(self, drone_pos, path_loss_exponent=2.0, noise_std_dev=2.0):
        """calculate the rssi received by the drone from the phone 
        
        Args:
            drone_pos (list): x y z value of the drone
            path_loss_exponent (float, optional): Free space is generally 2, dense environment is 4. Defaults to 2.0.
            noise_std_dev (float, optional): provides the gaussian random variable. Defaults to 2.0.

        Returns:
           float: the value of the rssi signal in DBm
        """
        # distance from drone to the phone
        distance = self.calculate_distance(drone_pos)
        # calculate the path loss using the log-dt path loss model
        path_loss = self.transmitted_power - 10 * path_loss_exponent * np.log10(distance)
        # add random noise to simulate environmental effects
        noise = np.random.normal(loc=0, scale=noise_std_dev, size=len(distance))
        # simulate RSSI with natural variation
        rssi = path_loss + noise

        return rssi


def generate_points_in_pentagon(pentagons, num_people):
    """generates points in the pentagon and at each point is 
    a phone emitting RF signal at 2.4ghz and at 20dbm

    Args:
        pentagons (class): pentagon class of the smaller pentagons
        num_people (int): the max number of poeple that can be spwaned in the pentagon

    Returns:
        list: a list of phone classes
    """
    points = list()
    for pentagon in pentagons:
        min_x, min_y, max_x, max_y = pentagon.bounds
        # random num_people per given area of the pentagon
        num_points = random.random.randint(0, num_people)
        while len(points) < num_points:
            random_x = np.random.uniform(min_x, max_x)
            random_y = np.random.uniform(min_y, max_y)
            if pentagon.contains(Point(random_x, random_y)):
                points.append(Point(random_x, random_y))

    phones = list()
    # generate the phones at each points
    for point in points:
        phone = Phone(point.x, point.y, FREQUENCY, TRANSMITTED_POWER)
        phones.append(phone)

    return phones