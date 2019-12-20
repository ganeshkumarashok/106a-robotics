#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf2_ros
import tf2_geometry_msgs
from math import radians, modf, pi
import math
import numpy as np

TURTLEBOT_ID = 'yellow' # might need to change this. If unsure or doesn't work, check rostopic list
moving_cmd_topic = '/' + TURTLEBOT_ID + '/cmd_vel_mux/input/navi'
odom_reading_topic = '/' + TURTLEBOT_ID + '/odom/'

# if the above topic is not found, use this instead
# moving_cmd_topic = '/cmd_vel_mux/input/navi'
# odom_reading_topic = '/odom'

def quaternion_to_euler(x, y, z, w):

	t0 = +2.0 * (w * x + y * z)
	t1 = +1.0 - 2.0 * (x * x + y * y)
	roll = math.atan2(t0, t1)
	t2 = +2.0 * (w * y - z * x)
	t2 = +1.0 if t2 > +1.0 else t2
	t2 = -1.0 if t2 < -1.0 else t2
	pitch = math.asin(t2)
	t3 = +2.0 * (w * z + x * y)
	t4 = +1.0 - 2.0 * (y * y + z * z)
	yaw = math.atan2(t3, t4)
	return yaw, pitch, roll

def euler_to_quaternion(roll, pitch, yaw):

		qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
		qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
		qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
		qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

		return qx, qy, qz, qw

# define global function that constantly read odom reading
def listener():

	rospy.init_node('closed_loop_control', anonymous=False)

	angle = 0
	distance = 0
	# topic = "/" + TURTLEBOT_ID + "/odom/"

	tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
	tf_listener = tf2_ros.TransformListener(tf_buffer)

	def callback(data):

		#print(data.pose.pose.position)
        # transform here
		transform = tf_buffer.lookup_transform("base_link",
								   "odom", #source frame
								   rospy.Time(0), #get the tf at first available time
								   rospy.Duration(1.0)) #wait for 1 second
		global cur_linear_x
		global cur_linear_y
		global cur_linear_z
		global cur_angular_x
		global cur_angular_y
		global cur_angular_z
		global cur_angular_w
		global cur_yaw
		global cur_pitch
		global cur_roll

		cur_linear_x = data.pose.pose.position.x
		cur_linear_y = data.pose.pose.position.y
		cur_linear_z = data.pose.pose.position.z

		cur_angular_x = data.pose.pose.orientation.x
		cur_angular_y = data.pose.pose.orientation.y
		cur_angular_z = data.pose.pose.orientation.z
		cur_angular_w = data.pose.pose.orientation.w

		# each yaw, pitch, roll is between -pi to pi
		cur_yaw, cur_pitch, cur_roll = quaternion_to_euler(cur_angular_x, cur_angular_y, cur_angular_z, cur_angular_w)
	sub = rospy.Subscriber(odom_reading_topic, Odometry, callback)

	# only get message in 0.05s, then unsubscribe
	# rospy.sleep(0.5)
	# sub.unregister()
	# rospy.spin()

class simple_move():
	def __init__(self):
		# initiliaze
		# rospy.init_node('drawasquare', anonymous=False)

		# What to do you ctrl + c
		# self.encoder = EncoderListener()
		rospy.on_shutdown(self.shutdown)

		self.cmd_vel = rospy.Publisher(moving_cmd_topic, Twist, queue_size=10)
		# self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

		#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ = 1/10 s = 0.1s
		self.update_rate = 10
		self.r = rospy.Rate(self.update_rate);


	def shutdown(self):
		# stop turtlebot
		rospy.loginfo("Stop Moving")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)

	def go_straight(self, time=None, speed=0.2, distance=None):
		# proportional control term
		p1 = 3

		if distance:
			desired_x = cur_linear_x + math.cos(cur_yaw) * distance
			desired_y = cur_linear_y + math.sin(cur_yaw) * distance

			print("desired_x: {0} desired_y: {1}".format(desired_x, desired_y))

			go_straight_cmd = Twist()
			go_straight_cmd.linear.x = speed
			go_straight_cmd.angular.z = 0

			rospy.loginfo("go to {0} at speed {1} def/s".format(distance, speed))
			rospy.sleep(1)

			while abs(desired_x - cur_linear_x) > 0.03 or abs(desired_y - cur_linear_y) > 0.03:
				if abs(desired_x - cur_linear_x) < 0.3 and abs(desired_y - cur_linear_y) < 0.3:
					if speed > 0:
						go_straight_cmd.linear.x = max(speed * abs(desired_x - cur_linear_x) * p1, 0.2)
					else:
						go_straight_cmd.linear.x = min(speed * abs(desired_x - cur_linear_x) * p1, -0.2)
				self.cmd_vel.publish(go_straight_cmd)
				self.r.sleep()
				print("current: x:{0} y:{1}".format(cur_linear_x, cur_linear_y))
				print("x error: ", abs(desired_x - cur_linear_x))
		elif time:
			rospy.loginfo("go for {0} s at speed {1} m/s".format(time, speed))
			go_straight_cmd = Twist()
			go_straight_cmd.linear.x = speed
			go_straight_cmd.angular.z = 0

			for x in range(0,time*self.update_rate):
				self.cmd_vel.publish(go_forward_cmd)
				self.r.sleep()


	def turn(self, time=None, speed=0.4, angle=None, yaw_coor=None):
		# counterclockwise is always increasing, and clockwise is always decreasing
		# starting z orientation angle is always 0,
		# and the reverse (pi or 180 degree) z is 1/-1 depends on which direction it moves
		# if move counterclockwise, then 0 -> pi -> -pi -> 0 complete one circle
		# if move clockwise, then 0 -> -pi -> pi -> 0 complete one circle

		# proportional control term
		p1 = 3

		if time:
			turn_cmd = Twist()
			turn_cmd.linear.x = 0
			turn_cmd.angular.z = radians(speed) # convert 45 deg/s to radians/s
			rospy.loginfo("turn left for {0} s at speed {1} def/s".format(time, speed))
			for x in range(0,time*self.update_rate):
				self.cmd_vel.publish(turn_left_cmd)
				self.r.sleep()
		elif angle:
			if angle > 180 or angle < -180:
				raise Exception("angle must be smaller than 180 or greater than -180")

			starting_yaw = cur_yaw
			ending_yaw = radians(angle) + starting_yaw

			# handle the case where from positive to negative or from negative to positive
			if ending_yaw > pi:
				ending_yaw = pi-ending_yaw
			elif ending_yaw < -pi:
				ending_yaw = 2*pi+ending_yaw
			yaw_coor = ending_yaw
			rospy.loginfo("turn for {0} degree at speed {1} rad/s".format(angle, speed))

		# because z_coor could be 0
		if yaw_coor is not None:
			if yaw_coor > pi or yaw_coor < -pi:
				raise Exception("yaw_coor must be smaller than pi or greater than -pi")

			# convert euler to quaternion
			desired_x, desired_y, desired_z, desired_w = euler_to_quaternion(0, 0, yaw_coor)

			print("desired: z:{0} w:{1}".format(desired_z, desired_w))

			if cur_yaw * yaw_coor > 0:
				if cur_yaw - yaw_coor > 0:
					speed = -speed
			elif cur_yaw * yaw_coor < 0:
				if abs(cur_yaw - yaw_coor) > pi:
					speed = -speed

			turn_cmd = Twist()
			turn_cmd.linear.x = 0
			turn_cmd.angular.z = speed

			rospy.loginfo("turn to {0} yaw coordinate at speed {1} def/s".format(yaw_coor, speed))
			rospy.sleep(1)

            # turn to some desired angle, stop when the angle is less than some threshold
			while abs(desired_z - cur_angular_z) > 0.006 or abs(desired_w - cur_angular_w) > 0.006:
				if abs(desired_z - cur_angular_z) < 0.2 and abs(desired_w - cur_angular_w) < 0.2:
					if speed > 0:
						turn_cmd.angular.z = max(speed * abs(desired_z - cur_angular_z) * p1, 0.2)
					else:
						turn_cmd.angular.z = min(speed * abs(desired_z - cur_angular_z) * p1, -0.2)
				self.cmd_vel.publish(turn_cmd)
				self.r.sleep()
				print("current: z:{0} w:{1}".format(cur_angular_z, cur_angular_w))
				print("z error: ", abs(desired_z - cur_angular_z))


	def curve_left(self, time, lin_speed=0.2, ang_speed=20):
		curve_left_cmd = Twist()
		curve_left_cmd.linear.x = lin_speed
		curve_left_cmd.angular.z = radians(ang_speed); # convert 45 deg/s to radians/s
		rospy.loginfo("turn left for {0} s at linear speed {1} m/s and angular speed {2} def/s".format(time, lin_speed, ang_speed))
		for x in range(0,time*self.update_rate):
			self.cmd_vel.publish(curve_left_cmd)
			self.r.sleep()


	def curve_right(self, time, lin_speed=0.2, ang_speed=20):
		curve_right_cmd = Twist()
		curve_right_cmd.linear.x = lin_speed
		curve_right_cmd.angular.z = -radians(ang_speed); # convert 45 deg/s to radians/s
		rospy.loginfo("turn left for {0} s at linear speed {1} m/s and angular speed {2} def/s".format(time, lin_speed, ang_speed))
		for x in range(0,time*self.update_rate):
			self.cmd_vel.publish(curve_right_cmd)
			self.r.sleep()

if __name__ == '__main__':
	listener()
	simple_bot = simple_move()
	rospy.sleep(0.5)
	print("no moving: x: {0} y: {1}".format(cur_linear_x, cur_linear_y))
	simple_bot.go_straight(distance=1, speed=0.4)
	print("after moving: x: {0} y: {1}".format(cur_linear_x, cur_linear_y))

	# simple_bot.curve_left(5)
    # simple_bot.curve_right(time=3, lin_speed=0.4, ang_speed=30)
    # simple_bot.go_straight(time=3, speed=0.4)

	# simple_bot.turn(angle=60, speed=0.8)
	# simple_bot.turn(yaw_coor=-pi/2)
	# print("after moving: ", cur_yaw)

	simple_bot.shutdown()
