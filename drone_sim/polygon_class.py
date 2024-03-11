from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
import math
import random
import numpy as np

random.seed(0)

class Polygons:
    def __init__(self, outer_x_limit, outer_y_limit, outer_num_sides):
        self.outer_x_limit = outer_x_limit
        self.outer_y_limit = outer_y_limit
        self.outer_num_sides = outer_num_sides

    def generate_outer_polygon(self):
        """generate the polygon to get a good guage of what it would look like
        the range must have a range of about maybe 10% to 20% so polygon not so oddly shaped

        Returns:
            a polygon class of the outer polygon to be plotted
        """
        coordinates = []
        angle_increment = 2 * math.pi / self.outer_num_sides

        def generate_displacement(displacement):
            limiter = 0.2
            angle = random.uniform(0, 360)
            displacement = (displacement * limiter) * math.cos(angle)

            return displacement

        for i in range(self.outer_num_sides):
            x = self.outer_x_limit * math.cos(i * angle_increment) + generate_displacement(self.outer_x_limit)
            y = self.outer_y_limit * math.sin(i * angle_increment) + generate_displacement(self.outer_y_limit)
            coordinates.append((x, y))

        return Polygon(coordinates)

    def generate_random_pentagons(self, outer_polygon, num_pentagons, rad):
        """generates smaller circles inside the bigger polygon

        Args:
            outer_polygon (class): polygon class
            num_pentagons (class): polygon class
            radius (float): radius of the circle

        Returns:
            list: a list of inner polygons
        """
        def generate_random_point_in_polygon(polygon):
            min_x, min_y, max_x, max_y = polygon.bounds
            while True:
                point = Point(np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y))
                if polygon.contains(point):
                    return point
        
        inner_polygons = []
        for _ in range(num_pentagons):
            random_point = generate_random_point_in_polygon(outer_polygon)
            radius = rad / 10 # Adjust this value as needed
            circle = random_point.buffer(radius)
            inner_polygon = circle.intersection(outer_polygon)
            if inner_polygon.area > 0:
                inner_polygons.append(inner_polygon)

        return inner_polygons