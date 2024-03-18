import math
import random

import ps3_visualize
import pylab
import numpy

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement

from env2 import obstacleRoom as oR

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
    def __init__(self, room, speed, runtime):
        """Initalises a drone with a given speed in a room, it also has a specified
        runtime to indicate how long it can run for

        Args:
            room (class): the room class
            speed (int): speed of the drone
            runtime (int): how long the drone can operate in meters
        """
        self.room = room
        self.speed = speed
        self.runtime = runtime
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


test_robot_movement(Standarddrone, oR)
