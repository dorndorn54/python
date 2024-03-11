from shapely.geometry import Polygon, Point
import numpy as np
import matplotlib.pyplot as plt
import random

random.seed(0)

FREQUENCY = 2.4*(10**9)
TRANSMITTED_POWER = 20

class Phone:
    def __init__(self,x, y, frequency = FREQUENCY, transmitted_power = TRANSMITTED_POWER):
        """the phone class that would represent a phone emitting an RF signal

        Args:
            frequency (hz): the frequency of the phone signal (configured in the subfile)
            transmitted_power (dbm): the signal strength of the phone at 1m (connfigured in the subfile)
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
    def generate_random_point_in_polygon(polygon):
        min_x, min_y, max_x, max_y = polygon.bounds
        while True:
            point = Point(np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y))
            if polygon.contains(point):
                return point
    
    def generate_point(pentagons, num_people):
        all_points = []
        for inner_polygon in pentagons:
            points = []
            while len(points) < num_people:
                random_point = generate_random_point_in_polygon(inner_polygon)
                points.append(random_point)
            all_points.extend(points)
        return all_points

    phones = list()
    points = generate_point(pentagons, num_people)
    # generate the phones at each points
    for point in points:
        phone = Phone(point.x, point.y, FREQUENCY, TRANSMITTED_POWER)
        phones.append(phone)

    return phones