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


class circular_drone(drone):
    """A drone that follows the circular pattern

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

    def update_position_and_sweep(self):

class circular_path(object):
    def __init__(self, drone):
        self.drone = drone
        self.room = self.drone.room
