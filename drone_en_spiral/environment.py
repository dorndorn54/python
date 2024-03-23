import os
import csv
import math


class map_generator(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
    def gen_corner_obstacle(self, percentage_width, percentage_height, corner_side):
        """generate obstacles at chosen corner position

        Args:
            percentage_width (float): percentage of the width
            percentage_height (float): percentage of the length
            corner_side (float): , (2, top.right), (3, bottom.right), (4 is bottom.left)
        """
        # need to check if the obstacle to be given will hit other osbtacles
        # if so reject
        y_position, x_position = corner_side.split(".")
         
        x_dimension = math.floor(percentage_width * self.width)
        y_dimension = math.floor(percentage_height * self.height)

        if x_position == 'left':
            start_x = 0
        elif x_position == 'right':
            start_x = self.width - x_dimension
        
        if y_position == 'top':
            start_y == 0
        elif y_position == 'bottom':
            start_y = self.height - y_dimension
        
        for x in range(start_x, start_x + x_dimension):
            for y in range(start_y, start_y + y_dimension):
                self.map[y][x] = 1
        
    def save_map(self, file_name, subfolder):
        """save the map to a csv file

        Args:
            file_name (string): name of map to be saved
        """
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        
        file_path = os.path.join(subfolder, file_name)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in self.map:
                writer.writerow(row)


map = map_generator(10, 10)
map.save_map("map_1", "map_data")