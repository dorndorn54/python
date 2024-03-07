import random
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


class Room:
    def __init__(self, width, length, height, shape_vertices):
        """a room class for the drone to navigate in 

        Args:
            width (int): the width of the room
            length (int): the length of the room
            shape_vertices (class): a polygon class that provides the shape of the random area
        """
        self.width = width
        self.length = length
        self.height = height
        self.shape = Polygon(shape_vertices)
        
    def is_inside(self, x, y):
        point = Point(x, y, 0)
        return self.shape.contains(point)

    def plot_room(self):
        # Create figure and axis for 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Extract coordinates of the polygon vertices
        x, y = self.shape.exterior.xy

        # Fill the polygon in 3D
        ax.plot(x, y, zs=0, zdir='z', color='b', alpha=0.5)

        # Set plot labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Room')

        # set Z limit
        ax.set_zlim(0, None)
        
        # Show plot
        plt.show()
        
# width = 20
# length = 20
# height = 20
# shape_vertices = [(2, 2), (8, 5), (15, 10), (10, 17), (5, 15)]  # Example shape vertices

# room = Room(width, length, height, shape_vertices)
# room.plot_room()

def generate_points(x_limit, y_limit, num_points):
    """generate the points for the polygon to get a good guage of what it would look like
    the range must have a range of about maybe 10% to 20% so polygon not so oddly shaped
    Args:
        x_limit (int): x limit
        y_limit (int): y limit
        num_points (int): the number of points for the polygon
    """
    points = list()
    
    # generate the points to build up the polygon
    percentage = 0.9
    x_value_to_pick = list(range(-x_limit, round(percentage*-x_limit))) + list(range(round(percentage*x_limit), x_limit)
    y_value_to_pick = list(range(-y_limit, round(percentage*-y_limit))) + list(range(round(percentage*y_limit), y_limit)
    
    # iterate through the num of points needed                                                                                             
    for _ in range(num_points):
        x_value = random.choice(x_value_to_pick)
        y_value = random.choice(y_value_to_pick)

            
