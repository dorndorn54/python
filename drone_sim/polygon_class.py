from shapely.geometry import Polygon, Point
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

    def generate_random_pentagons(self, outer_polygon, num_pentagons):
        """generates random smaller pentagons inside the outer polygon

        Args:
            outer_polygon (class): the polygon class
            num_pentagons (int): the number of smaller pentagons to be plotted

        Returns:
            list: a list of smaller pentagon class to be plotted later
        """
        pentagons = list()
        min_x, min_y, max_x, max_y = outer_polygon.bounds
        # Calculate maximum pentagon size based on the outer polygon
        pentagon_radius = min(outer_polygon.bounds[2] - outer_polygon.bounds[0], outer_polygon.bounds[3] - outer_polygon.bounds[1]) / 20

        for _ in range(num_pentagons):
            # Generate a random position within the outer polygon with enough distance from the boundary
            while True:
                random_point = (np.random.uniform(min_x + pentagon_radius, max_x*0.8 - pentagon_radius),
                                np.random.uniform(min_y + pentagon_radius, max_y*0.8 - pentagon_radius))
                if outer_polygon.contains(Point(random_point)):
                    break

            # Generate vertices for the pentagon
            vertices = []
            for i in range(5):
                angle = 2 * math.pi * i / 5
                vertex_x = random_point[0] + pentagon_radius * math.cos(angle)
                vertex_y = random_point[1] + pentagon_radius * math.sin(angle)
                vertices.append((vertex_x, vertex_y))

            # Create polygon from generated vertices
            pentagons.append(Polygon(vertices))
        return pentagons