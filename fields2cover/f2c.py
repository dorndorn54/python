import fields2cover as f2c
import numpy as np

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


def generate_linear_ring(coordinates):
    """generates the linear ring that the drone is meant to fly in

    Args:
        coordinates (_type_): _description_

    Returns:
        _type_: _description_
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
