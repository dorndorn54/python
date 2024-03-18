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
    
    def get_tile_scanned(self, m, n):
        """checks if the tile has been scanned

        Args:
            m (int): x_coord
            n (int): y_coord

        Returns:
            BOOL: True if scanned, False if not scanned
        """
        return self.tiles[(m, n)]
        
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
    
    def add_obstacles_to_room(self, obstacles):
        """
        Add a rectangular piece of obstacle to the room. obstacle tiles are stored 
        as (x, y) tuples in the list obstacle_tiles 
        
        obstacle location and size is randomly selected. Width and length are selected
        so that the piece of obstacle fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of obstacle so that the entire piece of 
        obstacle lies in the room.
        """
        count = 0
        # This addobstacleToRoom method is implemented for you. Do not change it.
        while count < obstacles:
            obstacle_width = random.randint(1, self.width - 1)
            obstacle_length = random.randint(1, self.length - 1)

            # Randomly choose bottom left corner of the obstacle item.    
            o_bottom_left_x = random.randint(0, self.width - obstacle_width)
            o_bottom_left_y = random.randint(0, self.length - obstacle_length)

            # Fill list with tuples of obstacle tiles.
            for i in range(o_bottom_left_x, o_bottom_left_x + obstacle_width):
                for j in range(o_bottom_left_y, o_bottom_left_y + obstacle_length):
                    if (i, j) not in self.obstacle_tiles:
                        self.obstacle_tiles.append((i, j))
                        count += 1

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