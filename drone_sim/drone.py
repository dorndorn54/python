from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
import math
import random
import numpy as np

random.seed(0)
np.random.seed(0)

class Drone:
    def __init__(self, x, y, z, speed, angle, flytime):
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.angle = angle
        self.flytime = flytime
    
    def get_position(self):
        """obtains the position of the drone

        Returns:
            tuple: x y and z position
        """
        return (self.x, self.y, self.z)
    
    def get_new_position(self, speed)