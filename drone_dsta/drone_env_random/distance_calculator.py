import math


def distance_travelled_drone(drone):
    """finds the total distance travelled by the drone

    Args:
        drone (class): the drone class
    """
    def cal_distance(pos1, pos2):
        """calculate distance between two points

        Args:
            pos1 (class): the first position
            pos2 (class): the second position

        Returns:
            float: distance between the two positions
        """
        x1, y1 = pos1.get_x(), pos1.get_y()
        x2, y2 = pos2.get_x(), pos2.get_y()
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance

    drone_positions = drone.get_drone_all_position()

    distance = 0
    for i in range(len(drone_positions) - 1):
        distance += cal_distance(drone_positions[i], drone_positions[i + 1])

    return distance
