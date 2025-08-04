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


class snaking_drone(drone):
    """A drone that follows the wall of the area

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
        home = (0.0, 0.0)
        room = self.room
        path = a_star(curr_pos, home, room)  # the coordinates are in (y,x) format

        if path is None:
            self.set_drone_position(Position(0, 0))
        else:
            pos_path = []
            for coordinates in path:
                pos_path.append(Position(coordinates[1], coordinates[0]))
            
        return pos_path

    def check_angle(self, curr_angle, add_angle):
        """ensures that the robot receives a proper input

        Args:
            curr_angle (float): current angle
            add_angle (float): change in angle

        Returns:
            float: the new angle for the drone to rotate to
        """
        total_angle = curr_angle + add_angle
        
        if total_angle == 360:
            return 0
        else:
            return total_angle

    def check_adjacent(self):
        curr_pos = self.get_drone_position()
        # get back and forth positions

    def update_position_and_sweep(self):
        # get the next position to the right
        # only 4 angles can be provided 0, 90, 180, 360
        drone_angle = self.get_drone_direction()
        drone_speed = self.get_drone_speed()
        new_pos = self.pos.get_new_position(drone_angle, drone_speed)
        
        if self.room.is_position_valid(new_pos):
            # move to the next cell
            self.set_drone_position(new_pos)
            # mark tile as scanned
            self.room.mark_tile_as_scanned(new_pos)
        else:
            # iterate turning 90 and moving one forward till
            # stop when there is nothing on the left
            # let the above command run by ending this
        # check if all adjacent cells have been cleaned if so move inwards one step
        # then continue

test_robot_movement(snaking_drone, oR, 10, 10, 3)
