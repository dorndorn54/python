import math
import random

class RectangularRoom(object):
    def __init__(self, width, length):
        """initalises a room with width and length
        As the drone travels over the tile it is marked as 

        Args:
            width (int): width of the space
            length (int): Length of the space 
        """
        self.width = width
        self.length = length
        self.tiles = dict()
        self.obstacles = list()
        
        # generating the floorplan
        # false marked as havent explored yet
        for w in range(width):
            for l in range(length):
                self.tiles[(w, l)] = False

    def add_obstacles_to_room(self, obstacles):
        """generates a number of obstacles in the given field

        Args:
            obstacles (int): the number of obstacles in the space
        """
        for _ in range(obstacles):
            o_width = random.randint(0, self.width - 1)
            o_length = random.randint(0, self.length - 1)

            # randomly choose the bottom left corner of where the item is
            o_botttom_x = random.randint(0, self.width - o_width)
            o_bootom_y = random.randint(0, self.length - o_length)

            # Fill list with tuples of furniture tiles.
            for i in range(o_botttom_x, o_botttom_x + o_width):
                for j in range(o_bootom_y, o_bootom_y + o_length):
                    if (i, j) not in self.obstacles:
                        self.obstacles.append((i, j))

    def mark_tile_as_scanned(self, pos):
        """mark the tile under the position pos as explored
        
        Assumes that the pos represents a valid position inside the room

        Args:
            pos (class): a position object
        """
        x_coord = math.floor(pos.get_x())
        y_coord = math.floor(pos.get_y())
        
        # set that tile as explored as True once explored
        self.tiles[(x_coord, y_coord)] = True
            
    def is_tile_explored(self, w, l):
        """checks if the tiles have been explored

        Args:
            w (int): x coordinate
            l (int): y coordinate

        Returns:
            _type_: _description_
        """
        return self.tiles[(w, l)]
    
    def get_num_tiles(self):
        """returns the number of tiles that need to be explored

        Returns:
            int: number of tiles that can be explored
        """
        return len(self.tiles) - len(self.obstacles)

    def get_num_explored_tiles(self):
        """returns the number of tiles that have been explored

        Returns:
            int: number of tiles explored
        """
        tiles = list(self.tiles.values())
        return tiles.count(True)

    def is_position_obstacle(self, pos):
        """checks if the position ahead is an obstacle

        Args:
            pos (class): position class

        Returns:
            BOOL: False if there is obstacle, True if there is obstacle
        """
        x_coord = math.floor(pos.get_x())
        y_coord = math.floor(pos.get_y())
        
        if (x_coord, y_coord) in self.obstacles:
            return False
        else:
            return True
    
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

    def is_position_valid(self, pos):
        """checks if the position to be accessed is valid

        Args:
            pos (class): position class of the object

        Returns:
            BOOL: True if position is valid, False if position is not valid
        """
        if (self.is_position_obstacle(pos)) and (self.is_position_in_room(pos)):
            return True
        return False
    
    def get_random_position(self):
        """returns a position object a valid random position inside the space

        Returns:
            tuple: (x_coord, y_coord)
        """
        possible_pos = list()

        for key in self.tiles:
            if key not in self.obstacles:
                possible_pos.append(key)
        
        return random.choice(possible_pos)