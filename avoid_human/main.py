# This file execute the whole process. 

# step 1: read data from optitrack
import motion_analytics
from simple_controller import simple_move, listener
import simple_controller
# import scipy as sp
import scipy.spatial

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf2_ros
import tf2_geometry_msgs
from math import radians, modf, pi
import math
import numpy as np
#Example
data = motion_analytics.load_mocap_csv('human_data/pose1a.csv')
# print(motion_analytics.get_min_distance(data))
# listener()
# rospy.sleep(0.5)
# turtlebot = simple_move()
# print("no moving: x: {0} y: {1}".format(cur_linear_x, cur_linear_y))
# turtlebot.go_straight(distance=1, speed=0.4)
# print("after moving: x: {0} y: {1}".format(cur_linear_x, cur_linear_y))
pedestrain = motion_analytics.get_xz_one_agent(data)
print(pedestrain)

# time, pedestrain_x, pedestrain_y = pedestrain[0]


# step 2: move the turtlebot in initial setting

# step 3: avoid human

# step 4: reach the goal