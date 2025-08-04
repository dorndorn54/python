import random
import math

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a length and contains (width * length) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, length):
        """
        Initializes a rectangular room with the specified width, length, and 
        dirt_amount on each tile.

        width: an integer > 0
        length: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = width
        self.length = length
        self.tiles = dict()

        # creating the dictionary for the floorplan
        for w in range(int(width)):
            for h in range(int(length)):
                self.tiles[(w, h)] = False
        
    def mark_tile_as_scanned(self, pos):
        """
        Mark the tile under the position pos as explored by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be explored in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        # determine which area the robot is at
        x_coord = math.floor(pos.get_x())
        y_coord = math.floor(pos.get_y())

        # set that tile as explored as True once explored
        self.tiles[(x_coord, y_coord)] = True

    def is_tile_explored(self, m, n):
        """
        Return True if the tile (m, n) has been explored.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is explored, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        return self.tiles[(m, n)]

    def get_num_explored_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        tiles = list(self.tiles.values())
        return tiles.count(True)
    
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        if pos.get_x() >= self.width or pos.get_y() >= self.length:
            return False
        elif pos.get_x() < 0 or pos.get_y() < 0:
            return False
        else:
            return True
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of obstacleRoom) 
                 if position is unobstacle, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


class obstacleRoom(RectangularRoom):
    """
    A obstacleRoom represents a RectangularRoom with a rectangular piece of 
    obstacle. The robot should not be able to land on these obstacle tiles.
    """
    def __init__(self, width, length):
        """ 
        Initializes a obstacleRoom, a subclass of RectangularRoom. obstacleRoom
        also has a list of tiles which are obstacle (obstacle_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, length)
        # Adds the data structure to contain the list of obstacle tiles
        self.obstacle_tiles = []
    
    def get_dimensions(self):
        """provides the dimensions of the given space

        Returns:
            tuple: (width, length)
        """
        return (self.width, self.length)

    def get_obstacles(self):
        """provides the obstacles of the given space

        Returns:
            list: list of obstacles as a tuple (x,y)
        """
        return self.obstacle_tiles
    
    def add_obstacles_to_room(self, num_obstacles):
        """generates num_obstacles number of obstacles that would
        be generated and appended to the self.obstacles_tiles list

        Args:
            num_obstacles (int): the number of obstacles to be generated
        """
        obstacles = []
        min_gap = math.floor(self.width * 0.2)
        while len(obstacles) < num_obstacles:
            # Generate random width, length, and position for each obstacle
            width = random.randint(1, math.floor(self.width * 0.3))
            length = random.randint(1, math.floor(self.length * 0.3))
            x = random.randint(1, self.width - width)
            y = random.randint(1, self.length - length)
            
            # Check if the obstacle overlaps with existing obstacles
            overlaps = False
            for obstacle in obstacles:
                if (x < obstacle[0] + obstacle[2] + min_gap and x + width + min_gap> obstacle[0] and
                    y < obstacle[1] + obstacle[3] + min_gap and y + length + min_gap > obstacle[1]):
                    overlaps = True
                    break
            
            # If no overlap, add the obstacle to the list
            if not overlaps:
                obstacles.append((x, y, width, length))
                
        for obstacle in obstacles:
            for x in range(obstacle[0], obstacle[0] + obstacle[2]):
                for y in range(obstacle[1], obstacle[1] + obstacle[2]):
                    self.obstacle_tiles.append((x, y))

    def is_tile_obstacle(self, m, n):
        """
        Return True if tile (m, n) is obstacle.
        """
        if (m, n) in self.obstacle_tiles:
            return True
        return False
        
    def is_position_obstacle(self, pos):
        """
        pos: a Position object.

        Returns True if pos is obstacle and False otherwise
        """
        x_cord = math.floor(pos.get_x())
        y_cord = math.floor(pos.get_y())
        if (x_cord, y_cord) in self.obstacle_tiles:
            return True
        return False

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        returns: True if pos is in the room Fand is unobstacle, False otherwise.
        """

        if (self.is_position_obstacle(pos) is False) and self.is_position_in_room(pos):
            return True
        return False

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        the number of obstacle tiles must be deducted
        """
        return len(self.tiles) - len(self.obstacle_tiles)
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position
        (inside the room and not in a obstacle area).
        """
        possible_pos = list()
        for keys in self.tiles:
            if keys not in self.obstacle_tiles:
                possible_pos.append(keys)
        return random.choice(possible_pos)


class circularRoom(RectangularRoom):
    """
    A obstacleRoom represents a RectangularRoom with a rectangular piece of 
    obstacle. The robot should not be able to land on these obstacle tiles.
    """
    def __init__(self, width, length):
        """ 
        Initializes a obstacleRoom, a subclass of RectangularRoom. obstacleRoom
        also has a list of tiles which are obstacle (obstacle_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, length)
        # Adds the data structure to contain the list of obstacle tiles
        self.obstacle_tiles = []
    
    def get_dimensions(self):
        """provides the dimensions of the given space

        Returns:
            tuple: (width, length)
        """
        return (self.width, self.length)

    def get_obstacles(self):
        """provides the obstacles of the given space

        Returns:
            list: list of obstacles as a tuple (x,y)
        """
        return self.obstacle_tiles
    
    def add_obstacles_to_room(self):
        """generates num_obstacles number of obstacles that would
        be generated and appended to the self.obstacles_tiles list

        Args:
            num_obstacles (int): the number of obstacles to be generated
        """
        center_x = self.width / 2
        center_y = self.length / 2
        
        # axes
        axes = list()
        for _ in range(3):
            x_axe = random.randint(1, math.floor(center_x * 0.5))
            y_axe = random.randint(1, math.floor(center_y * 0.5))
            axes.append((x_axe, y_axe))

        # Define the corners to add obstacles
        corners = [(0, self.length-1), (self.width-1, self.length-1), (self.width-1, 0)]

        for corner, (semi_major, semi_minor) in zip(corners, axes):
            corner_x, corner_y = corner
            for x in range(self.width):
                for y in range(self.length):
                    if ((x - corner_x) / semi_major)**2 + ((y - corner_y) / semi_minor)**2 <= 1:
                        self.obstacle_tiles.append((x, y))

    def is_tile_obstacle(self, m, n):
        """
        Return True if tile (m, n) is obstacle.
        """
        if (m, n) in self.obstacle_tiles:
            return True
        return False
        
    def is_position_obstacle(self, pos):
        """
        pos: a Position object.

        Returns True if pos is obstacle and False otherwise
        """
        x_cord = math.floor(pos.get_x())
        y_cord = math.floor(pos.get_y())
        if (x_cord, y_cord) in self.obstacle_tiles:
            return True
        return False

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        returns: True if pos is in the room Fand is unobstacle, False otherwise.
        """

        if (self.is_position_obstacle(pos) is False) and self.is_position_in_room(pos):
            return True
        return False

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        the number of obstacle tiles must be deducted
        """
        return len(self.tiles) - len(self.obstacle_tiles)
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position
        (inside the room and not in a obstacle area).
        """
        possible_pos = list()
        for keys in self.tiles:
            if keys not in self.obstacle_tiles:
                possible_pos.append(keys)
        return random.choice(possible_pos)