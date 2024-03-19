import math
import heapq
 
# Define the Cell class
class Cell:
    """the cell class for for the a* algorithm
    """
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination
 

def is_valid(row, col, COL, ROW):
    """checks if the cell is within the grid

    Args:
        row (int): y coordinate
        col (int): x coordinate
        COL (int): the number of columns in the grid
        ROW (int): the number of rows in the grid

    Returns:
        BOOL: True if valid, False if invalid
    """
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)


def is_unblocked(grid, row, col):
    """check if the cell is blocked

    Args:
        grid (dictionary): the grid used in the algorithm
        row (int): y coordinate
        col (int): x coordinate

    Returns:
        BOOL: True if no obstacle, False if there is an obstacle
    """
    return grid[row][col] == 1
 

def is_destination(row, col, dest):
    """checks if the cell is the destination

    Args:
        row (int): y coordinate
        col (int): x coordinate
        dest (tuple): y, x coordinate

    Returns:
        BOOL: True if destination reached, False if destination not reached
    """
    return row == dest[0] and col == dest[1]
 

def calculate_h_value(row, col, dest):
    """calculates the h value for the a* algorithm

    Args:
        row (int): y coordinate
        col (int): x coordinate
        dest (tuple): y, x coordiante

    Returns:
        float: the heuristic value
    """
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5


def trace_path(cell_details, dest):
    """traces the path from the src to the destination

    Args:
        cell_details (class): the cell class
        dest (tuple): y, x coordinate
    """
    path = []
    row = dest[0]
    col = dest[1]
 
    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col
 
    # Add the source cell to the path
    path.append((col, row))
    # Reverse the path to get the path from source to destination
    path.reverse()
  
    return path
    # # Print the path
    # for i in path:
    #     print("->", i, end=" ")
    # print()


def a_star_search(grid, src, dest, COL, ROW):
    """the engine for the a* algorithm

    Args:
        grid (dictionary): the grid of the map
        src (tuple): y, x coordinate
        dest (tuple): y, x coordinate
        COL (int): max width of the grid
        ROW (int): max length of the grid
    """
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1], COL, ROW) or not is_valid(dest[0], dest[1], COL, ROW):
        print("Source or destination is invalid")
        return
 
    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return
 
    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return
 
    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]
 
    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j
 
    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))
 
    # Initialize the flag for whether destination is found
    found_dest = False
 
    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)
 
        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True
 
        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]
 
            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j, COL, ROW) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    found_dest = True
                    return path
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new
 
                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")


def a_star(curr_pos, home, room):
    """generates the a* algorithm to retur home

    Args:
        curr_pos (tuple): x, y coordinate
        home (tuple): x, y coordinate
        room (class): the room class
    """
    # Define the grid (1 for unblocked, 0 for blocked)
    COL, ROW = room.get_dimensions()
    obstacles = room.get_obstacles()

    # initalise the positions
    src = (curr_pos[1], curr_pos[0])
    dest = (home[1], home[0])

    # generate grid
    grid = list()
    for _ in range(ROW):
        grid.append([1 for _ in range(COL)])

    # add the obstacles into the area
    for x, y in obstacles:
        grid[y][x] = 0

    # Run the A* search algorithm
    return a_star_search(grid, src, dest, COL, ROW)
    