#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf2_ros
import tf2_geometry_msgs
from math import radians, modf, pi

TURTLEBOT_ID = 'yellow' # might need to change this. If unsure or doesn't work, check rostopic list
# cur_linear_x = -999
# cur_linear_y = -999
# cur_linear_z = -999

# cur_angular_x = -999
# cur_angular_y = -999
# cur_angular_z = -999

# class EncoderListener():
# 	def __init__(self):

# 		rospy.init_node('closed_loop_control', anonymous=False)

# 		self.angle = 0
# 		self.distance = 0
# 		self.topic = "/" + TURTLEBOT_ID + "/odom/"

# 		self.tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
# 		self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

# 		self.cur_linear_x = -999
# 		self.cur_linear_y = -999
# 		self.cur_angular_z = -999

# 		print("ENCODER LISTENER STARTED")

# 		def callback(data): 
# 			#print(data.pose.pose.position)
# 			transform = self.tf_buffer.lookup_transform("base_link",
# 									   "odom", #source frame
# 									   rospy.Time(0), #get the tf at first available time
# 									   rospy.Duration(1.0)) #wait for 1 second
# 			# print("transform")
# 			# print(transform)
# 			# transform.transform.translation.x = 0
# 			# transform.transform.translation.y = 0
# 			# transform.transform.translation.z = 0

# 			# pose_transformed = tf2_geometry_msgs.do_transform_pose(data.pose, transform)
# 			# print("ORIGINAL")
# 			# print(data.pose.pose.position)
# 			# print(data.pose.pose.position.x)

# 			# # print(type(data.pose))
# 			# print("TRANSFORMED")
# 			# print(pose_transformed)
# 			# print()

# 			self.cur_linear_x = data.pose.pose.position.x
# 			# print(self.cur_linear_x)
# 			self.cur_linear_y = data.pose.pose.position.y
# 			self.cur_angular_z = data.pose.pose.orientation.z

# 		rospy.Subscriber("/" + TURTLEBOT_ID + "/odom/", Odometry, callback)


#Define the method which contains the node's main functionality
def listener():

	rospy.init_node('closed_loop_control', anonymous=False)

	angle = 0
	distance = 0
	topic = "/" + TURTLEBOT_ID + "/odom/"

	tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
	tf_listener = tf2_ros.TransformListener(tf_buffer)

	def callback(data):

		#print(data.pose.pose.position)
		transform = tf_buffer.lookup_transform("base_link",
								   "odom", #source frame
								   rospy.Time(0), #get the tf at first available time
								   rospy.Duration(1.0)) #wait for 1 second
		# print("transform")
		# print(transform)
		# transform.transform.translation.x = 0
		# transform.transform.translation.y = 0
		# transform.transform.translation.z = 0

		# pose_transformed = tf2_geometry_msgs.do_transform_pose(data.pose, transform)
		# print("ORIGINAL")
		# print(data.pose)
		# print(data.pose.pose.position.x)

		# # print(type(data.pose))
		# print("TRANSFORMED")
		# print(pose_transformed)
		# print()
		global cur_linear_x
		global cur_linear_y
		global cur_linear_z
		global cur_angular_x
		global cur_angular_y
		global cur_angular_z
		# print("previous x: ", cur_linear_x)
		cur_linear_x = data.pose.pose.position.x
		cur_linear_y = data.pose.pose.position.y
		cur_linear_x = data.pose.pose.position.x

		cur_angular_x = data.pose.pose.orientation.x
		cur_angular_y = data.pose.pose.orientation.y
		cur_angular_z = data.pose.pose.orientation.z

		# print(cur_angular_z)

	sub = rospy.Subscriber(topic, Odometry, callback)

	# only get message in 0.05s, then unsubscribe
	# rospy.sleep(0.5)
	# sub.unregister()
	# rospy.spin()



	#Wait for messages to arrive on the subscribed topics, and exit the node
	#when it is killed with Ctrl+C
	# rospy.spin()
	# rospy.sleep()

class open_loop_move():
	def __init__(self):
		# initiliaze
		# rospy.init_node('drawasquare', anonymous=False)

		# What to do you ctrl + c
		# self.encoder = EncoderListener()    
		rospy.on_shutdown(self.shutdown)
		
		self.cmd_vel = rospy.Publisher('/' + TURTLEBOT_ID + '/cmd_vel_mux/input/navi', Twist, queue_size=10)
		# self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
	 
	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ = 1/10 s = 0.1s
		self.update_rate = 10
		self.r = rospy.Rate(self.update_rate);

		
	def shutdown(self):
		# stop turtlebot
		rospy.loginfo("Stop Moving")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)

	def go_forward(self, time, speed=0.2):
		# default speed is moving at 0.2 m/s
		# time in seconds
		rospy.loginfo("go forward for {0} s at speed {1} m/s".format(time, speed))
		go_forward_cmd = Twist()
		go_forward_cmd.linear.x = speed
		go_forward_cmd.angular.z = 0

		# print('forward')
		# cur_x = self.encoder.cur_linear_x
		# cur_y = self.encoder.cur_linear_y
		# cur_z = self.encoder.cur_angular_z

		# print("x: ", cur_x)        

		for x in range(0,time*self.update_rate): 
			self.cmd_vel.publish(go_forward_cmd)
			self.r.sleep()

			# listener()
			print()
			print("current linear_x while moving forward: ", cur_linear_x)
			print("current linear_y while moving forward: ", cur_linear_y)
			print("current linear_z while moving forward: ", cur_linear_z)
			print("current angular_x while moving forward: ", cur_angular_x)
			print("current angular_y while moving forward: ", cur_angular_y)
			print("current angular_z while moving forward: ", cur_angular_z)
	
	def go_backward(self, time=None, speed=0.2, distance=None):
		# default speed is moving at 0.2 m/s
		if not distance: # when we don't move by distance
			rospy.loginfo("go backward for {0} s at speed {1} m/s".format(time, speed))
			go_backward_cmd = Twist()
			go_backward_cmd.linear.x = -speed
			go_backward_cmd.angular.z = 0

			for x in range(0,time*self.update_rate): 
				self.cmd_vel.publish(go_backward_cmd)
				self.r.sleep()

				# listener()
				print("current x while moving backward: ", cur_linear_x)
		elif distance:
			rospy.loginfo("go backward for {0} at speed {1} m/s".format(distance, speed))
			starting_x = cur_linear_x
			# while cur_linear_x

	def turn_right(self, time, speed=45):
		# default speed is turning at 45 deg/s
		turn_right_cmd = Twist()
		turn_right_cmd.linear.x = 0
		turn_right_cmd.angular.z = radians(speed); # convert 45 deg/s to radians/s
		rospy.loginfo("turn_right for {0} s at speed {1} deg/s".format(time, speed))
		for x in range(0,time*self.update_rate):
			self.cmd_vel.publish(turn_right_cmd)
			self.r.sleep()            

			print()
			print("current linear_x while moving forward: ", cur_linear_x)
			print("current linear_y while moving forward: ", cur_linear_y)
			print("current linear_z while moving forward: ", cur_linear_z)
			print("current angular_x while moving forward: ", cur_angular_x)
			print("current angular_y while moving forward: ", cur_angular_y)
			print("current angular_z while moving forward: ", cur_angular_z)

	def turn_left(self, time, speed=45):
		# default speed is turning at 45 deg/s
		turn_left_cmd = Twist()
		turn_left_cmd.linear.x = 0
		turn_left_cmd.angular.z = -radians(speed); # convert 45 deg/s to radians/s
		rospy.loginfo("turn left for {0} s at speed {1} def/s".format(time, speed))
		for x in range(0,time*self.update_rate):
			self.cmd_vel.publish(turn_left_cmd)
			self.r.sleep()

			print()
			print("current linear_x while moving forward: ", cur_linear_x)
			print("current linear_y while moving forward: ", cur_linear_y)
			print("current linear_z while moving forward: ", cur_linear_z)
			print("current angular_x while moving forward: ", cur_angular_x)
			print("current angular_y while moving forward: ", cur_angular_y)
			print("current angular_z while moving forward: ", cur_angular_z)

	def turn(self, time=None, speed=45, angle=None, z_coor=None):
		# counterclockwise is always increasing, and clockwise is always decreasing
		# starting z orientation angle is always 0, and the reverse (pi or 180 degree) z is 1/-1 depends on which direction it moves
		# if move counterclockwise, then 0 -> 1 -> -1 -> 0 complete one loop
		# if move clockwise, then 0 -> -1 -> 1 -> 0 complete one loop
		
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
			starting_z = cur_angular_z
			# print("start: ", starting_z)

			ending_z = radians(angle)/pi + starting_z

			# handle the case where from positive to negative or from negative to positive
			# Therefore, defined the ending_z as the float after decimal
			if ending_z > 1:
				ending_z = -1+round(modf(ending_z)[0], 5)
			elif ending_z < -1:
				ending_z = 1+round(modf(ending_z)[0], 5)
			z_coor = ending_z
		# because z_coor could be 1 or 0			
		if z_coor is not None:
			turn_cmd = Twist()
			rospy.loginfo("turn left for {0} degree at speed {1} def/s".format(angle, speed))
			rospy.sleep(1)
			starting_z = cur_angular_z
			print("start: ", starting_z)

			ending_z = z_coor
			print("end: ", ending_z)
			
			# handle the case where from positive to negative 
			# Therefore, defined the error as the float after decimal
			error = ending_z - starting_z
			if error >= 1:
				error = -1+round(modf(error)[0], 5)
			elif error <= -1:
				error = 1+round(modf(error)[0], 5)
			print(error)

			# need to tuen this thread
			while abs(error) > 0.01:
				turn_cmd.linear.x = 0
				turn_cmd.linear.y = 0
				turn_cmd.linear.z = 0
				turn_cmd.angular.z = min(max(error*p1, 0.3), 2)
				self.cmd_vel.publish(turn_cmd)
				self.r.sleep()
				error = ending_z - cur_angular_z
				if error > 1:
					error = -1+round(modf(error)[0], 5)
				elif error < -1:
					error = 1+round(modf(error)[0], 5)

				# print("current angular_z while moving forward: ", cur_angular_z)
		# print("current angular_z while turning: ", cur_angular_z)



	def curve_left(self, time, lin_speed=0.2, ang_speed=20):
		curve_left_cmd = Twist()
		curve_left_cmd.linear.x = lin_speed
		curve_left_cmd.linear.y = 0
		curve_left_cmd.linear.z = 0
		curve_left_cmd.angular.z = radians(ang_speed); # convert 45 deg/s to radians/s
		curve_left_cmd.angular.x = 0
		curve_left_cmd.angular.y = 0
		rospy.loginfo("turn left for {0} s at linear speed {1} m/s and angular speed {2} def/s".format(time, lin_speed, ang_speed))
		for x in range(0,time*self.update_rate):
			self.cmd_vel.publish(curve_left_cmd)
			self.r.sleep()

	def curve_right(self, time, lin_speed=0.2, ang_speed=20):
		curve_right_cmd = Twist()
		curve_right_cmd.linear.x = lin_speed
		curve_right_cmd.linear.y = 0
		curve_right_cmd.linear.z = 0
		curve_right_cmd.angular.z = -radians(ang_speed); # convert 45 deg/s to radians/s
		curve_right_cmd.angular.x = 0
		curve_right_cmd.angular.y = 0
		rospy.loginfo("turn left for {0} s at linear speed {1} m/s and angular speed {2} def/s".format(time, lin_speed, ang_speed))
		for x in range(0,time*self.update_rate):
			self.cmd_vel.publish(curve_right_cmd)
			self.r.sleep()

	def turn_left_angle(self, angle, speed=20):
		turn_left_angle_cmd = Twist()
		turn_left_angle_cmd.linear.x = 0
		print('sdfjk')
		cur_x = self.encoder.cur_linear_x
		cur_y = self.encoder.cur_linear_y
		cur_z = self.encoder.cur_angular_z

		print("x: ", cur_x)


		# while 
 

class PathPlanner():

	def __init__(self):
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel = rospy.Publisher('/' + TURTLEBOT_ID + '/cmd_vel_mux/input/navi', Twist, queue_size=10)
		self.lin_speed = 0.2
		self.linear_error_bound = 0.1
		self.controller = open_loop_move()

	def move_forward_by(self, distance = 1.0):
		time = distance/(self.lin_speed)
		self.controller.go_forward(time, speed= self.lin_speed)

	def move_back_by(self, distance = 1.0):
		time = distance/(self.lin_speed)
		self.controller.go_backward(time, self.lin_speed)
 
if __name__ == '__main__':
	# encoder_listener = EncoderListener()
	listener()
	draw_tri = open_loop_move()
	rospy.sleep(0.5)
	print("no moving: ", cur_angular_z)
	# draw_tri.curve_left(5)
	# draw_tri.go_forward(3, speed=0.9)
	# draw_tri.go_backward(3, speed = 0.3)
	# draw_tri.go_backward(time=2)
	# draw_tri.go_forward(time=2)
	# draw_tri.go_backward(2)
	# draw_tri.go_forward(2)
	# draw_tri.go_backward(2)
	# draw_tri.go_forward(2)
	# draw_tri.go_backward(2)
	# draw_tri.turn_right(20, speed=20)
	# draw_tri.turn_left(20, speed=20)

	draw_tri.turn(angle=90)
	# draw_tri.turn(z_coor=0)
	print("after moving: ", cur_angular_z)
	
	# draw_tri.curve_left(2)
	# draw_tri.go_forward(2)
	# draw_tri.turn_right(4, speed=90)
	# draw_tri.go_forward(2)
	
	# draw_tri.shutdown()
	# except:
		# rospy.loginfo("node terminated.")

"""
Important: it looks like the yellow turtlebot has some offet in the positive z and negative z. 
Run the above code for several times, you will realize this issue. The positive z cover less 
area than negative z. What is the reason?
"""