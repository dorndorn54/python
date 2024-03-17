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
        # work needs to be done 
        # need to keep track of previous postion and where it is now and if 
        # got enought battery to retrun back hpme
        # determine which area the robot is at
        x_cord = math.floor(pos.get_x())
        y_cord = math.floor(pos.get_y())
        # access the tile at certain position and clean it
        if self.tiles[(x_cord, y_cord)] > capacity:
            # if dirt smaller than capacity then just remove
            self.tiles[(x_cord, y_cord)] -= capacity
        else:
            # set dirt to 0 if exceed
            self.tiles[(x_cord, y_cord)] = 0
            
    def is_tile_explored(self, w, l):
        """checks if the tiles have been explored

        Args:
            w (int): x coordinate
            l (int): y coordinate

        Returns:
            _type_: _description_
        """
        return self.tiles[(w, l)]
    
    def get_num_explored_tiles(self):
        """returns the number of tiles that have been explored

        Returns:
            int: number of tiles explored
        """
        tiles = list(self.tiles.values())
        return tiles.count(True)