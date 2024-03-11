from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
import math
import random
import numpy as np

random.seed(0)
np.random.seed(0)


class Drone:
    def __init__(self, x, y, z, speed, angle, flytime, coverage_angle, coverage_zone):
        """the drone that is to fly in the room

        Args:
            x (float): x position
            y (float): y position
            z (float): z position
            speed (float): the speed of the drone
            angle (float): the orientation of the drone
            flytime (int): the flytime is represented by the maximum distance the drone can travel
            coverage_angle (int): the coverage angle of the drone antenna
            coverage_zone (class): the polygon class
        """

        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.angle = angle
        self.flytime = flytime
        self.coverage_angle = coverage_angle
        self.coverage_zone = coverage_zone

    def get_position(self):
        """obtains the position of the drone

        Returns:
            tuple: x y and z position
        """
        return (self.x, self.y, self.z)

    def coverage_fov(self):
        """plots the square coverage box for the drone

        Returns:
            numpy array: the coordingates of the coverage box
        """
        # coverage angle in radian
        cov_rad = np.radians(self.coverage_angle)

        # calculate the half side length of the square coverage area
        half_side_length = 2 * self.z * np.tan(cov_rad / 2)

        # coordinates for the box
        vertices = np.array([
            [self.x - half_side_length, self.y - half_side_length],  # Bottom-left
            [self.x - half_side_length, self.y + half_side_length],  # Top-left
            [self.x + half_side_length, self.y + half_side_length],  # Top-right
            [self.x + half_side_length, self.y - half_side_length]   # Bottom-right
        ])

        return vertices


def intersection_points(outer_polygon, perpendicular_distance):
    """returns a list of points along the outer polygon for the drone
    to travel to 

    Args:
        outer_polygon (class): polygon class
        perpendicular_distance (float): the distance separating the lines

    Returns:
        list: x and y coordinates
    """
    boundary_points = np.array(outer_polygon.exterior)
    intersection_points = list()
    
    for i in range(len(boundary_points) - 1):
        # definind the line segment points
        p1, p2 = boundary_points[i:i+2]

        # calculate the direction vector ux and uy
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = np.sqrt(dx**2 + dy**2)
        ux, uy = dx / length, dy / length
        
        # calculates the number of lines needed based on drone coverage
        num_lines = int(length / dl)
        increment_x, increment_y = dl * ux, dl * uy
        current_point = p1

        intersection_points.extend([current_point := (current_point[0] + increment_x, current_point[1] + increment_y) for _ in range(num_lines)])

    return intersection_points