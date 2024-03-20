# 6.0002 Problem Set 3:
# Edited Fall 2016

import math
import random
import ps3_visualize
import pylab


def test_robot_movement(robot_type, room_type, room_width, room_length, obstacles):
    # check if room is obstacle room
    is_obstacle = str(room_type).find('obstacleRoom') > 0
    
    room = room_type(room_width, room_length)
    if is_obstacle:
        room.add_obstacles_to_room(obstacles)
    robots = [robot_type(room, 1)]
    coverage = 0
    time_steps = 0
    min_coverage = 1.0
    if is_obstacle:
        anim = ps3_visualize.RobotVisualization(1, room_width, room_length, room.obstacle_tiles) 
    else:
        anim = ps3_visualize.RobotVisualization(1, 5, 5, [])  
    while coverage < min_coverage:
        time_steps += 1 
        for robot in robots:
            robot.update_position_and_sweep()
            anim.update(room, robots)
            coverage = float(room.get_num_explored_tiles())/room.get_num_tiles()
    
    if robot.check_home():
        time_steps += 1
        anim.done()
    else:
        pos_path = robot.return_home()
        for position in pos_path:
            time_steps += 1
            robot.set_drone_position(position)
            anim.update(room, robots)

        anim.done()
