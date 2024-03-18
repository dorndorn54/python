import math
import heapq

from env2 import obstacleRoom as oR

COL = 8
ROW = 10


class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination


def generate_grid(room):
    """generates the grid for the A* algorithm

    Args:
        room (class): the room that the drone is to navigate in

    Returns:
        list of list: 1 is free space, 0 is obstacle
    """
    width, length = room.get_dimensions()
    obstacles = room.get_obstacles()
    
    grid = [[1 for _ in range(width)] for _ in range(length)]
    
    for x, y in obstacles:
        grid[x][y] = 0
    
    return grid


def is_valid(row, col):
    """checks if the cell is valid

    Args:
        row (int): y value
        col (int): x value

    Returns:
        BOOL: True if the cell is valid, False if cell is not valid
    """
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)