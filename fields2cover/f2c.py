import fields2cover as f2c
import numpy as np

np.random(0)

def generate_obtuse_polygon_with_area(n, target_area):
    """generates a n sided polygon  of area target_area

    Args:
        n (int): number of sides of polygon
        target_area (float): the area of the polygon 

    Returns:
        list: x, y coordinates
    """
    # Ensure n is odd
    if n % 2 == 0:
        n += 1

    # Initialize variables
    current_area = 0
    size = 1.0  # Initial size
    vertices = []

    while current_area < target_area:
        # Generate convex and concave vertices alternately
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        vertices.clear()
        for i in range(n):
            angle = angles[i]
            if i % 2 == 0:
                vertices.append((size * np.cos(angle), size * np.sin(angle)))
            else:
                vertices.append((size * 0.5 * np.cos(angle), size * 0.5 * np.sin(angle)))

        # Calculate the area of the generated polygon
        current_area = 0.5 * np.abs(np.dot(np.array(vertices[:-1])[:, 0], np.array(vertices[1:])[:, 1]) -
                                    np.dot(np.array(vertices[:-1])[:, 1], np.array(vertices[1:])[:, 0]))

        # Adjust size for next iteration
        size += 0.1

    # Round coordinates to 1 decimal point
    rounded_vertices = [(round(x, 1), round(y, 1)) for x, y in vertices]

    return rounded_vertices


def generate_headland(ring, robot):
    """generates an inner zone for the drone to operate in

    Args:
        ring (class): the linear ring class
        robot (class): the robot class

    Returns:
        class: headland class a zone for the drone to fly in
    """
    # generate a cell from the given ring
    cell = f2c.Cell()
    cell.addRing(ring)
    
    # area of the cell
    #area = cell.getArea()

    # generate a multipolygon cells to pass to headland generator
    cells = f2c.Cells()
    cells.addGeometry(cell)
    
    # generate const border to allow drone to turn
    const_hl = f2c.HG_Const_gen()
    no_hl = const_hl.generateHeadlands(cells, 3.0 * robot.robot_width)

    return no_hl

def generate_linear_ring(coordinates):
    """generates the linear ring that the drone is meant to fly in

    Args:
        coordinates (list): x, y coordinates

    Returns:
        class: the ring class
    """
    # generating the ring
    ring = f2c.LinearRing()

    # passing the points to the ring
    for x, y in coordinates:
        # generate point
        p = f2c.Point(x, y)

        # add the point to the ring
        ring.addPoint(p)

    return ring


def generate_robot(fov_width, cruise_speed, max_icc):
    """generate the robot that is to operate in the field

    Args:
        fov_width (float): the width of the drone camera 
        cruise_speed (float): the speed of the drone
        max_icc (float): max turning speed of the drone
    """
    robot = f2c.Robot(1.0, fov_width, cruise_speed)
    robot.setMinRadius(max_icc)
    robot.linear_curv_change(0.1)

    return robot


def generate_length_swath(robot, no_hl):
    """generates the swath, maximise length of the swath

    Args:
        robot (class): the robot class
        no_hl (class): the area the drone travels in a straight line
    """
    # initalise the method to generate the swath length
    swath_length = f2c.OBJ_SwathLength()
    bf_sw_gen = f2c.SG_BruteForce();
    
    # generate the swaths in the headland
    swaths_bf_swathlength = bf_sw_gen.generateBestSwaths(swath_length, robot.op_width, no_hl.getGeometry(0));
    
    return swaths_bf_swathlength


def generate_swath_connections(swaths, type_path):
    """generates the swaths start and end

    Args:
        swaths (class): the lines for the drone to follow
        type_path (string): boustrophedon or snake

    Returns:
        class: the swath class
    """
    if type_path == 'boustrophedon':
        sorter = f2c.RP_Boustrophedon()
    if type_path == 'snake':
        sorter = f2c.RP_Snake()

    swaths = sorter.genSortedSwaths(swaths)

    return swaths


def generate_path(swaths, robot, curve_type):
    """generate the final path for the drone to follow

    Args:
        swaths (class): the lines for the drone to follow
        robot (clas): the robot 
        curve_type (string): a string of the type of curve to be used
    
    Returns:

    """
    # call the path planner
    path_planner = f2c.PP_PathPlanning()

    # set the curve type
    if curve_type == 'dubins':
        curve = f2c.PP_DubinsCurves()
    if curve_type == 'reeds':
        curve = f2c.PP_ReedsSheppCurves()
    
    # configure the path
    path = path_planner.searchBestPath(robot, swaths, curve)
    
    return path


def generate_output(fov_width, cruise_speed, max_icc, n_side, target_area, type_path, curve_type):
    # call the robot
    Robot = generate_robot(fov_width, cruise_speed, max_icc)
    
    # generate outermap
    polygon = generate_obtuse_polygon_with_area(n_side, target_area)
    # generate liner ring
    ring = generate_linear_ring(polygon)
    # generate headland
    no_hl = generate_headland(ring, Robot)
    
    # generate swaths(path)
    swaths = generate_length_swath(Robot, no_hl)
    # sort the swaths
    sorted_swaths = generate_swath_connections(swaths, type_path)
    # plan the path
    path = generate_path(sorted_swaths, Robot, curve_type)
    