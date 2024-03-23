import math
import random

import ps3_visualize
import pylab
import numpy

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement

from env2 import obstacleRoom as oR
from env2 import circularRoom as cR
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

    def update_angle(self, curr_angle, direction):
        """changes the angle for the drone
        ensuring that the angle is in line

        Args:
            curr_angle (int): current direction of the drone
            direction (str): right / left

        Returns:
            int: the angle to be pointed to
        """
        # if turning right exceed 360
        if direction == 'right':
            if (curr_angle + 90) > 360:
                return 0
            else:
                return curr_angle + 90
        # if turning left go below 0
        if direction == 'left':
            if (curr_angle - 90) < 0:
                return 270
            else:
                return curr_angle - 90
    
    def check_if_adjacent_visited(self, curr_pos):
        """checks if the adjacent tiles have been visited

        Args:
            curr_pos (class): the current position of the drone

        Returns:
            BOOL: True if not visited, False if visited
        """
        curr_x = curr_pos.get_x()
        curr_y = curr_pos.get_y()
        adjcent_pos = [Position(curr_x - 1, curr_y), Position(curr_x + 1, curr_y),
                       Position(curr_x, curr_y - 1), Position(curr_x, curr_y + 1) ]

        # check if in the room if so then check if explored
        for pos in adjcent_pos:
            x = math.floor(pos.get_x())
            y = math.floor(pos.get_y())
            if self.room.is_position_valid(pos):
                if not self.room.is_tile_explored(x, y):
                    return False

        return True
                
    def move_drone_and_mark_pos(self, new_pos):
        """if position is valid move and then mark as cleaned

        Args:
            new_pos (class): the new position the drone is meant to move to
        """
        self.set_drone_position(new_pos)
        # clean the position that it is at
        self.room.mark_tile_as_scanned(new_pos)

    def update_position_and_sweep(self):
        drone_speed = self.get_drone_speed()
        drone_direction = self.get_drone_direction()
        new_pos = self.pos.get_new_position(drone_direction, drone_speed)
        
        # check if next step forward is valid
            # move to the next step forwards 
        # obstacle met
            # turn right
            # one step forward
            # look back to the front
            
            # if boundary has been met turn to the right
        # if surrounding has been explored
            # move inwards and then point back to where it was pointing before moving in
test_robot_movement(circular_drone, cR, 10, 10, None)
