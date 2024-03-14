class x_algorithm:
    def __init__(self, polygon, drone):
        """the cellular decomp search algorithm

        Args:
            polygon (class): the polygon class (search area)
            drone (class): the drone class
        """
        self.polygon = polygon
        self.drone = drone

    def decompose_polygon_equal_areas(self, num_subpolygons):
        """decomposes the larger area into smaller areas for each drone to utilise

        Args:
            polygon (class): the larger polygon to convert into smaller polygons
            num_subpolygons (int): the number of smaller polygons to be generated

        Returns:
            list: a list of polygon classes
        """
        # Calculate the total area of the polygon
        total_area = self.polygon.area

        # Calculate the target area for each sub-polygon
        target_area = total_area / num_subpolygons

        # Convert the polygon into a MultiPolygon with one initial polygon
        multi_polygon = MultiPolygon([self.polygon])

        # Decompose the polygon into smaller sub-polygons
        subpolygons = []
        for _ in range(num_subpolygons):
            # Use a binary search to find a sub-polygon with approximately the target area
            min_area = 0
            max_area = total_area
            while max_area - min_area > 1e-6:
                # Calculate the mid-point of the search interval
                mid_area = (min_area + max_area) / 2

                # Extract a sub-polygon with the given area
                sub_polygon = multi_polygon.buffer(-mid_area)

                # Check if the area of the sub-polygon is close enough to the target area
                if np.isclose(sub_polygon.area, target_area, atol=1e-6):
                    break
                elif sub_polygon.area > target_area:
                    min_area = mid_area
                else:
                    max_area = mid_area

            # Add the sub-polygon to the list of decomposed sub-polygons
            subpolygons.append(sub_polygon)

            # Update the remaining area for the next iteration
            total_area -= sub_polygon.area

            # Update the MultiPolygon by removing the current sub-polygon
            multi_polygon = multi_polygon.difference(sub_polygon)

        return subpolygons

    def generate_liner_ring(self, subpolygon):
        """convert the subpolygon to linear ring

        Args:
            subpolygons (class): a polygon of the polygon class

        Returns:
            ring: the area for the robot to navigate in
        """
        vertices_coords = subpolygon.exterior.coords
        # generate the ring
        ring = f2c.LinearRing()

        # iterate through the coordinates
        for coords in vertices_coords:
            # generate the point
            point = f2c.Point(coords[0], coords[2])
            # append the point to the ring
            ring.addPoint(point)

        return ring