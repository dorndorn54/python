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

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


class drone(object):

    """Represents a drone sweeping a given area
    At all times the drone has a given position and direction in the room
    
    Subclasses would provide movement stratergies via update_position_and_sweep
    providing a single time step
    """
    def __init__(self, room, speed,):
        """Initalises a drone with a given speed in a room, it also has a specified
        runtime to indicate how long it can run for

        Args:
            room (class): the room class
            speed (int): speed of the drone
            runtime (int): how long the drone can operate in meters
        """
        self.room = room
        self.speed = speed
        # configure the drone position and direction
        self.pos = Position(0, 0)
        self.direction = 0

    def get_drone_position(self):
        """
        Returns: a Position object giving the drone's position in the room.
        """
        return self.pos
    
    def get_drone_speed(self):
        """
        Returns: the speed of the drone which is a float s > 0.0
        """
        return self.speed

    def get_drone_direction(self):
        """
        Returns: a float d giving the direction of the drone as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_drone_position(self, position):
        """
        Set the position of the drone to position.

        position: a Position object.
        """
        self.pos = position

    def set_drone_direction(self, direction):
        """
        Set the direction of the drone to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction
    
    def check_home(self):
        """check if the drone is home

        Returns:
            BOOL: True if home, False if not home
        """
        home = Position(0, 0)
        
        if home == self.get_drone_position():
            return True

    def update_position_and_sweep(self):
        """
        Simulate the raise passage of a single time-step.

        Move the drone to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


class Standarddrone(drone):
    """
    A Standarddrone is a drone with the standard movement strategy.

    At each time-step, a Standarddrone attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
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
        """
        Simulate the raise passage of a single time-step.

        Move the drone to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean 
        the dirt on the tile by its given capacity. 
        """
        # given the current speed of the drone cal where the drone will go
        drone_speed = self.get_drone_speed()
        drone_angle = self.get_drone_direction()
        new_pos = self.pos.get_new_position(drone_angle, drone_speed)

        if self.room.is_position_valid(new_pos):
            # it will move to that new position
            self.set_drone_position(new_pos)
            # clean the position that it is at
            self.room.mark_tile_as_scanned(new_pos)
        # if position not valid it will just rotate at position
        else:
            self.set_drone_direction(random.randrange(360))


#test_robot_movement(Standarddrone, oR, 5, 5, 3)
test_robot_movement(Standarddrone, cR, 10, 10, None)
""" to visualise the movement of the drone

Args:
    Standarddrone (class): drone type
    oR (class): room type
    10 (int): room width
    10 (int): room length
    5 (int): the number of obstacles in the room
"""




def run_simulation(speed, width, length, min_coverage, num_trials):
    """run num_trials of the simulation and return the mean number of
    timesteps needed to cover the entire area 

    Args:
        speed (int): speed of the robot
        width (int): width of the room
        length (int): length of the room
        min_coverage (float): the coverage goal for the room
        num_trials (int): the number of trials to be executed

    Returns:
        int: average of all the timesteps
    """
    timesteps = list()

    for _ in range(num_trials):
        # initalise the empty room
        Room = oR(width, length)
        tile_count = Room.get_num_tiles()
        explored_tiles = Room.get_num_explored_tiles

        drone = Standarddrone(Room, speed)

        # loop through and check if clean else continue
        count = 0
        while (explored_tiles / tile_count) < min_coverage:
            drone.update_position_and_sweep()
            explored_tiles = Room.get_num_explored_tiles()
            count += 1
        pos_path = drone.return_home()
        for position in pos_path:
            timesteps += 1
            drone.set_drone_position(position)
            count += 1
        # repeat and append the score to the list
        timesteps.append(count)

    return round(numpy.average(timesteps))