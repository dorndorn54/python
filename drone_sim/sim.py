# this code is meant to create the environment to fly the drone and simulate the algorithm 

import matplotlib.pyplot as plt
import numpy as np
import random

X_VAL = 300
Y_VAL = 300
Z_VAL = 300

class object3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Drone(object3D):
    def __init__(self, x=0, y=0, z=0, signal_range=10, cone_angle=120):
        super().__init__(x, y, z)
        self.signal_range = signal_range
        self.cone_angle = cone_angle

    def within_signal_cone(self, human):
        """checks if the human on the ground is in the signal cone
        of the drone 

        Args:
            human (_class_): _a human class_
        """
        distance = np.sqrt((self.x - human.x)**2 + (self.y - human.y)**2 + (self.z - human.z)**2)
        # if dt fail just return false
        if distance <= self.signal_range:
            # else check the signal cone component 
            angle_to_human = np.arctan2(human.y - self.y, human.x - self.x)
            angle_difference = np.abs(angle_to_human - np.arctan2(self.y, self.x))
            if angle_difference <= self.cone_angle/2:
                return True
        return False

class Human(object3D):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)


class environment_3D:
    def __init__(self, width, length, height):
        """the environment that the drone and the human are to be placed in

        Args:
            width (int): x_value
            length (int): y_value
            height (int): z_value
        """
        self.width = width
        self.length = length
        self.height = height
        self.human = list()
        self.drone = list()
    
    def provide_dimensions(self):
        return (self.width, self.length, self.height)

    # adding item into free space to visualise
    def add_human(self, human):
        self.human.append(human)
    
    def add_drone(self, drone):
        self.drone.append(drone)

    def plot_space(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot drones
        for drone in self.drone:
            ax.scatter(drone.x, drone.y, drone.z, c='r', marker='^', label='Drone')
        for human in self.human:
            ax.scatter(human.x, human.y, human.z, c='b', marker='o', label='Human')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.length)
        ax.set_zlim(0, self.height)
        ax.legend()

        plt.show()
        
def generate_humans(count, environment):
    """randomly generate COUNT number of humans over a given area in the environment

    Args:
        count (_int_): the number of humans that need to be generated
        environment (class): the 3d space class to get the cords data and append the human to it later
    """
    max_x_value = environment.width
    max_y_value = environment.length
    
    for _ in range(count):
        x = random.uniform(0, max_x_value)
        y = random.uniform(0, max_y_value)
        
        # generate the human
        human = Human(x, y, 0)
        
        # appending the human to the environment
        environment.add_human(human)
        
def generate_drone(count, environment, signal_range, cone_angle):
    """randomly generate COUNT number of humans over a given space in the environment

    Args:
        count (int): the number of drones that need to be generated
        environment (class): the 3d space class to get the cords data and append the human to it later
        signal_range (int): the range of the signal that the drone can provide
        cone_angle (int): the cone angle of the drones
    """
    max_x_value, max_y_value, max_z_value = environment.provide_dimensions()
    
    for _ in range(count):
        x = random.uniform(0, max_x_value)
        y = random.uniform(0, max_y_value)
        z = random.uniform(0, max_z_value)
        
        # generate the drone
        drone = Drone(x, y, z, signal_range, cone_angle)
        
        # append the drone to the environment
        environment.add_drone(drone)

        
def generate_simulation(x, y, z, human_count, drone_count, signal_range, cone_angle):
    """one function to simulate everything

    Args:
        x (_int_): x_value
        y (int): y_value
        z (int): z_value
        human_count (int): number of human to deploy
        drone_count (int): number of drones to deploy
        signal_range (int): max range of the drone
        cone_angle (int): max angle from the drone to the humans
    """
    # configure the environment
    environment = environment_3D(X_VAL, Y_VAL, Z_VAL)
    
    # configure the humans in the environment
    generate_humans(human_count, environment)
    
    # configure the drone in the environment
    generate_drone(drone_count, environment, signal_range, cone_angle)
    
    # show the space
    environment.plot_space()

generate_simulation(X_VAL, Y_VAL, Z_VAL, 10, 1, 10, 60)