from shapely.geometry import Polygon, Point,  MultiPolygon
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
    
    def get_range(self):
        """obtains the fly time of the drone

        Returns:
            int: the remaing flytime of the drone
        """
        return self.flytime

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

class cellular_decomposition:
    def __init__(self, polygon, drone):
        """the cellular decomp search algorithm

        Args:
            polygon (class): the polygon class (search area)
            drone (class): the drone class
        """
        self.polygon = polygon
        self.drone = drone

    def boustrophedon_sweep(self, step_size):
        """marks the points along the polygon for the sweeping program

        Args:
            polygon (class): polygon clas
            step_size (float): the minimum distance between the points

        Returns:
            list: x and y coordinates
        """
        coverage_path = []

        # Extract the exterior coordinates of the polygon
        exterior_coords = self.polygon.exterior.coords[:]

        # Iterate through the exterior coordinates
        for i in range(len(exterior_coords) - 1):
            v1 = exterior_coords[i]
            v2 = exterior_coords[i + 1]

            # Create a LineString segment between consecutive vertices
            segment = LineString([v1, v2])

            # Calculate the length of the segment
            segment_length = segment.length

            # Calculate the number of steps needed to cover the segment
            num_steps = int(segment_length / step_size)

            # Calculate the step size along the segment
            dx = (v2[0] - v1[0]) / num_steps
            dy = (v2[1] - v1[1]) / num_steps

            # Iterate along the segment and add waypoints to the coverage path
            for j in range(num_steps):
                x = v1[0] + j * dx
                y = v1[1] + j * dy

                # Add waypoint to the coverage path
                coverage_path.append(Point(x, y))

            # Add the end vertex of the segment to the coverage path
            coverage_path.append(Point(v2))

        return coverage_path

    def decompose_polygon_equal_areas(self, num_subpolygons):
        """decomposes the larger area into smaller areas for each drone to utilise

        Args:
            polygon (class): the larger polygon to convert into smaller polygons
            num_subpolygons (int): the number of smaller polygons to be generated

        Returns:
            list: a list of polygon classes
        """
        # Calculate the total area of the polygon
        total_area = self.polygon.area
        
        # Calculate the target area for each sub-polygon
        target_area = total_area / num_subpolygons
        
        # Convert the polygon into a MultiPolygon with one initial polygon
        multi_polygon = MultiPolygon([self.polygon])
        
        # Decompose the polygon into smaller sub-polygons
        subpolygons = []
        for _ in range(num_subpolygons):
            # Use a binary search to find a sub-polygon with approximately the target area
            min_area = 0
            max_area = total_area
            while max_area - min_area > 1e-6:
                # Calculate the mid-point of the search interval
                mid_area = (min_area + max_area) / 2
                
                # Extract a sub-polygon with the given area
                sub_polygon = multi_polygon.buffer(-mid_area)
                
                # Check if the area of the sub-polygon is close enough to the target area
                if np.isclose(sub_polygon.area, target_area, atol=1e-6):
                    break
                elif sub_polygon.area > target_area:
                    min_area = mid_area
                else:
                    max_area = mid_area
                    
            # Add the sub-polygon to the list of decomposed sub-polygons
            subpolygons.append(sub_polygon)
            
            # Update the remaining area for the next iteration
            total_area -= sub_polygon.area
            
            # Update the MultiPolygon by removing the current sub-polygon
            multi_polygon = multi_polygon.difference(sub_polygon)
            
        return subpolygons


