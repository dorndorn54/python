import math
import random

import ps3_visualize
import pylab
import numpy

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement

from env2 import obstacleRoom as oR
from return_home import a_star
from drone import drone, Position


class bsd_drone(drone):
    """A drone that follows the Boustrophedon-cell-decomposition

    Args:
        drone (class): drone class from the main drone
    """
    def return_home(self):
        """generates a list of coordinates for the drone to return home

        Returns:
            _type_: _description_
        """
        pos = self.get_drone_position()
        curr_pos = (math.floor(pos.get_x()), math.floor(pos.get_y()))
        home = (0, 0)
        room = self.room
        path = a_star(curr_pos, home, room)  # the coordinates are in (y,x) format

        if path is None:
            self.set_drone_position(Position(0, 0))
        else:
            pos_path = []
            for coordinates in path:
                pos_path.append(Position(coordinates[1], coordinates[0]))
            
        return pos_path

class split_map(object):
    """this class serves to split up the given map into a few regions
    when it meets an obstacle it will split the area before as 1 unit

    Args:
        object (_type_): _description_
    """
    def __init__(self, room, drone_count):
        self.room = room
        self.drone_count = drone_count