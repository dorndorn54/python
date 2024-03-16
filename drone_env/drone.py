class Position(object):
    def __init__(self, x, y):
        """initalise a position with x and y coordinates

        Args:
            x (float): x coordinate
            y (float): y coordinate
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


class Drone(object):
    """
    Represents a drone sweeping a given zone
    
    At all times the Drone has a position and direction in the room
    It has also a fixed pov of the ground below it
    
    The subclasses are meant to provide movement stratergies
    simulating a single time step
    """
    def __init__(self, environment, speed, runtime):
        """initalises a Drone with a given speed and allocated runtime
        It is orignally setup at (0, 0) facing north 

        Args:
            environment (_type_): _description_
            speed (_type_): _description_
            runtime (_type_): _description_
        """
        self.room = room
        self.environment = environment
        self.speed = speed
        self.runtime = runtime
        # configured
        self.pos = Position(0, 0)
        self.direction = 0
        
    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.pos
    
    def get_robot_speed(self):
        """
        Returns: the speed of the robot which is a float s > 0.0
        """
        return self.speed

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.pos = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction
    
    def update_position_and_clean(self):
        """
        simulate the passage of time as a single timestep
        """
        # -- implement in subclass--