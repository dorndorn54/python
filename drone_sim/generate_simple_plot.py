import random
import math
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt

# class imports
from polygon_class import Polygons as poly
from signal_simulation import generate_points_in_pentagon as generate


class Room:
    def __init__(self, width, length, height, outer_polygon, inner_polygon):
        """a room class for the drone to navigate in 

        Args:
            width (int): the width of the room
            length (int): the length of the room
            shape_vertices (class): a polygon class that provides the shape of the random area
        """
        self.width = width
        self.length = length
        self.height = height
        self.outer_polygon = outer_polygon
        self.inner_polygon = inner_polygon
        
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

        # Set plot labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Room')

        # set Z limit
        ax.set_zlim(0, None)

        # Show plot
        plt.show()


def generate_plot(x_limit, y_limit, z_limit, num_sides, num_clusters):
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
    inner_polygons = polygon_class.generate_random_pentagons(outer_polygon, num_clusters)
    
    # generate the room
    room = Room(x_limit, y_limit, z_limit, outer_polygon, inner_polygons)
    
    # generate phones in the 
    # show the room plot
    room.plot_room()


generate_plot(1000, 1000, 1000, 8, 5)
