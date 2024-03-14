from shapely.geometry import Polygon, Point,  MultiPolygon
from shapely.ops import cascaded_union
import math
import random
import numpy as np

from polygon_class import Polygons as poly


# randomly move around the given space till all the nodes are hit
class polygon_area:
    """this represents the odd shaped room that the drone will have to explore in
    the room oringates from the polygon that was previously generated from the polygon_class.py
    file
    """
    def __init__(self, polygon):
        self.polygon = polygon
        self.points_per_polygon = list()

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

    def generate_points(self, polygon, grid_size, distance):
        """generates the points that the drone must hit

        Args:
            polygon (class): the polygon class
            grid_size (float): the size of the grid to determine the resolution of the plot points
            distance (float): the distance between the points

        Return:
            list: a list of x and y coordinates of the points
        """

        def generate_equidistant_points(distance):
            equidistant_points = []
            # Iterate through the exterior coordinates of the polygon
            for i in range(len(polygon.exterior.coords) - 1):
                # Get the start and end points of the line segment
                start_point = polygon.exterior.coords[i]
                end_point = polygon.exterior.coords[i + 1]

                # Create a LineString from the start and end points
                line = LineString([start_point, end_point])

                # Calculate the length of the line segment
                segment_length = line.length

                # Calculate the number of points to distribute along the line segment
                num_points = int(segment_length / distance)

                # Calculate the step size along the line segment
                step_size = segment_length / num_points

                # Iterate along the line segment and add equidistant points
                for j in range(num_points):
                    # Interpolate a point along the line segment
                    point = line.interpolate(j * step_size)
                    equidistant_points.append(point.coords[0])

            # Add the last point of the polygon
            equidistant_points.append(polygon.exterior.coords[-1])

            return equidistant_points

        def generate_points_on_perimeter_and_inside(polygon, grid_size, distance):
            # Generate equidistant points along the perimeter
            equidistant_points = generate_equidistant_points(distance)

            # Generate points inside the polygon using a grid-based approach
            min_x, min_y, max_x, max_y = polygon.bounds
            grid_points = []
            for x in np.arange(min_x, max_x, grid_size):
                for y in np.arange(min_y, max_y, grid_size):
                    point = Point(x, y)
                    if polygon.contains(point):
                        grid_points.append((x, y))

            # Combine the lists of equidistant points and grid points
            points = equidistant_points + grid_points

            # convert all points to int
            int_coords = [(int(x), int(y)) for x, y in points]

            return int_coords
        
        return generate_points_on_perimeter_and_inside(polygon, grid_size, distance)

    def generate_dict_points(self, points):
        """given the points of each broken down polygon
        build a dictionary of each polygon points

        Args:
            points (list): contains the points marked throughout one polygon
        """
        point_dict = dict()
        
        for point in points:
            point_dict[point] = False

        self.points_per_polygon.append(point_dict)
        
class individual_polygon_drone:
    def __init__(self, polygon):
        self.polygon = polygon
        
    def mark_visited(self, drone_coverage):
        """marks the coordinates that have been visited by the drone that
        is designated to survey that area 

        Args:
            drone_coverage (_type_): _description_
        """
        points_within_squares = []
        for sq in drone_coverage:
            min_x, min_y = np.min(sq, axis=0)
            max_x, max_y = np.max(sq, axis=0)
            points_within_square = [(x, y) for x in range(int(min_x), int(max_x) + 1) for y in range(int(min_y), int(max_y) + 1)]
            points_within_squares.append(points_within_square)

        for point in points_within_square:
            if point in self.polygon:
                self.polygon[point] = True
    
    def is_tile_cleaned(self, position):
        """determines if the area has been sweeped by the dron

        Args:
            position (tuple): x, y coordinates

        Returns:
            BOOL: True if the area has been cleaned
        """
        return self.polygon[position]

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        tiles = list(self.tiles.values())
        return tiles.count(False)
    
    def is_position_in_room(self, position):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        x_cord = math.floor(position.x)
        y_cord = math.floor(position.y)
        if (x_cord, y_cord) in self.polygon:
            return True
        return False

class Drone:
    def __init__(self, x, y, z, speed, angle, flytime, coverage_angle):
        """the drone that is to fly in the room

        Args:
            x (float): x position
            y (float): y position
            z (float): z position
            speed (float): the speed of the drone
            angle (float): the orientation of the drone
            flytime (int): the flytime is represented by the maximum distance the drone can travel
            coverage_angle (int): the coverage angle of the drone antenna
        """

        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.angle = angle
        self.flytime = flytime
        self.coverage_angle = coverage_angle

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
    
    def coverage_width(self):
        """calculates the width of the fov of the drone

        Returns:
            float: the width
        """
        # coverage angle in radian
        cov_rad = np.radians(self.coverage_angle)
        
        # calculate the length of the fov
        side_length = self.z * np.tan(cov_rad / 2)
        
        return side_length

    def coverage_fov(self):
        """plots the square coverage box for the drone

        Returns:
            numpy array: the coordingates of the coverage box
        """
        # coverage angle in radian
        cov_rad = np.radians(self.coverage_angle)

        # calculate the half side length of the square coverage area
        half_side_length = self.z * np.tan(cov_rad / 2) / 2 

        # coordinates for the box
        vertices = np.array([
            [self.x - half_side_length, self.y - half_side_length],  # Bottom-left
            [self.x - half_side_length, self.y + half_side_length],  # Top-left
            [self.x + half_side_length, self.y + half_side_length],  # Top-right
            [self.x + half_side_length, self.y - half_side_length]   # Bottom-right
        ])

        return vertices


def run_simulation(polygon, num_robots):
    timesteps = list()
    
    # initalise the search area the drones are to fly in

    # generating the polygon
    polygon_class = poly(x_limit, y_limit, num_sides)
    outer_polygon = polygon_class.generate_outer_polygon()
    
    # generating a drone
    drone = Drone(x, y, z, speed, angle, flytime, coverage_angle)
    drone_fov = drone.coverage_width()
    
    # calling the decomposition class
    polygon_decomposition = polygon_area(outer_polygon)
    # decomposing the bigger polygon into smaller polygons a list
    decomposed_polygons = polygon_decomposition.decompose_polygon_equal_areas(num_robots)
    # iterate through the decomposed polygons and obtain a list containg a list for each decomposed polygon
    dict_per_decomposed_polygon = list()
    for polygon in decomposed_polygons:
        # generate the points for each polygon
        points = polygon_decomposition.generate_points(polygon, 1.0, drone_fov)
        # generate the dictionary used by the drone
        dict_per_decomposed_polygon.append(polygon_decomposition.generate_dict_points(points))
    
    robot_list = list()
    for i in range(num_robots):
        given_area = individual_polygon_drone