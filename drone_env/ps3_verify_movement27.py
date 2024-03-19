# 6.0002 Problem Set 3:
# Edited Fall 2016

import math
import random
import ps3_visualize
import pylab

OBSTACLES = 3

def test_robot_movement(robot_type, room_type):
    # check if room is obstacle room
    is_obstacle = str(room_type).find('obstacleRoom') > 0
    
    room = room_type(5, 5)
    if is_obstacle:
        room.add_obstacles_to_room(OBSTACLES)
    robots = [robot_type(room, 1, 1000)]
    coverage = 0
    time_steps = 0
    min_coverage = 1.0
    if is_obstacle:
        anim = ps3_visualize.RobotVisualization(1, 5, 5, room.obstacle_tiles) 
    else:
        anim = ps3_visualize.RobotVisualization(1, 5, 5, [])  
    while coverage < min_coverage:
        time_steps += 1 
        for robot in robots:
            robot.update_position_and_sweep()
            anim.update(room, robots)
            coverage = float(room.get_num_explored_tiles())/room.get_num_tiles()
    anim.done()