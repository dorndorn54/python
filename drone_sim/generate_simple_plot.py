import random
import math
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import numpy as np

# class imports
from polygon_class import Polygons as poly
from signal_simulation import generate_points_in_pentagon as generate_phones


# constants
DRONE_HEIGHT = 100
random.seed(0)
np.random.seed(0)


class Room:
    def __init__(self, width, length, height, outer_polygon, inner_polygon, phones):
        """a room for the drone to fly in 

        Args:
            width (int): = width of the room
            length (int): length of the room
            height (int): height of the room
            outer_polygon (class): the polygon class for the outermost polygon
            inner_polygon (class): the polygon class for the inner polygon
            phones (list): a list of phone classes 
        """
        self.width = width
        self.length = length
        self.height = height
        self.outer_polygon = outer_polygon
        self.inner_polygon = inner_polygon
        self.phones = phones

    def is_inside(self, x, y):
        """checks if the drone is inside the outer pentagon

        Args:
            x (float): x position of the drone
            y (float): y position of the drone

        Returns:
            BOOL: true or false
        """
        point = Point(x, y, 0)
        return self.outer_polygon.contains(point)

    def calculate_rssi_at_position(self):
        """calculates the rssi value at a given position
        needs to be updated to receive the values from the drones
        """
        def generate_random_point_in_polygon(polygon):
            min_x, min_y, max_x, max_y = polygon.bounds
            while True:
                point = Point(np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y))
                if polygon.contains(point):
                    return point

        point = generate_random_point_in_polygon(self.outer_polygon)
        rssi = list()
        for phone in self.phones:
            rssi.append(phone.calculate_rssi([point.x, point.y, DRONE_HEIGHT]))
        # print(point.x, point.y)
        # print(len(rssi))
        print(rssi)
        return np.mean(rssi)

    def plot_room(self):
        """plots the room in which the drone is flying in 
        """
        # Create figure and axis for 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Extract coordinates of the polygon vertices
        x, y = self.outer_polygon.exterior.xy
        # Fill the polygon in 3D
        ax.plot(x, y, zs=0, zdir='z', color='b', alpha=0.5)
        for pentagon in self.inner_polygon:
            ax.plot(*pentagon.exterior.xy, color='red', linewidth=1)
        # Fill in the phones in the inner polygons
        for phone in self.phones:
            ax.scatter(phone.x, phone.y, zs=0, zdir='z', color='g', marker='o', s=1)
        for point in self.points:
            ax.scatter(phone[0], phone[1], zs=0, zdir='z', color='r', marker='o', s=1)

        # Set plot labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Room')

        # set Z limit
        ax.set_zlim(0, None)

        # Show plot
        plt.show()


def generate_plot(x_limit, y_limit, z_limit, num_sides, num_clusters, max_people_cluster):
    """1 function provide vertices and plot the graph

    Args:
        x_limit (int): x limit
        y_limit (int): y limit
        z_limit (int): z limit
        num_sides (int): the number of points for the polygon
    """
    # generate the polygons to be built
    polygon_class = poly(x_limit, y_limit, num_sides)
    outer_polygon = polygon_class.generate_outer_polygon()
    inner_polygons = polygon_class.generate_random_pentagons(outer_polygon, num_clusters, x_limit)

    # generate the phones to be in the room
    phones = generate_phones(inner_polygons, max_people_cluster)

    # generate the room
    room = Room(x_limit, y_limit, z_limit, outer_polygon, inner_polygons, phones)

    # show the room plot
    room.plot_room()

    # show rssi value
    print(room.calculate_rssi_at_position())


generate_plot(100, 100, 100, 10, 4, 10)
