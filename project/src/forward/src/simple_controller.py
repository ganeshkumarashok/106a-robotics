#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf2_ros
import tf2_geometry_msgs
from math import radians

TURTLEBOT_ID = 'yellow' # might need to change this. If unsure or doesn't work, check rostopic list

class EncoderListener():
    def __init__(self):

        rospy.init_node('closed_loop_control', anonymous=False)

        self.angle = 0
        self.distance = 0
        self.topic = "/" + TURTLEBOT_ID + "/odom/"

        self.tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        self.cur_linear_x = -999
        self.cur_linear_y = -999
        self.cur_angular_z = -999

        print("ENCODER LISTENER STARTED")

        def callback(data): 
            #print(data.pose.pose.position)
            transform = self.tf_buffer.lookup_transform("base_link",
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

            self.cur_linear_x = data.pose.pose.position.x
            print(self.cur_linear_x)
            self.cur_linear_y = data.pose.pose.position.y
            self.cur_angular_z = data.pose.pose.orientation.z

        rospy.Subscriber("/" + TURTLEBOT_ID + "/odom/", Odometry, callback)

# def callback(data):


#     #print(data.pose.pose.position)
#     transform = tf_buffer.lookup_transform("base_link",
#                                "odom", #source frame
#                                rospy.Time(0), #get the tf at first available time
#                                rospy.Duration(1.0)) #wait for 1 second
#     # print("transform")
#     # print(transform)
#     # transform.transform.translation.x = 0
#     # transform.transform.translation.y = 0
#     # transform.transform.translation.z = 0

#     # pose_transformed = tf2_geometry_msgs.do_transform_pose(data.pose, transform)
#     # print("ORIGINAL")
#     # print(data.pose)
#     # print(data.pose.pose.position.x)

#     # # print(type(data.pose))
#     # print("TRANSFORMED")
#     # print(pose_transformed)
#     # print()

#     self.cur_linear_x = data.pose.pose.position.x
#     print(self.cur_linear_x )
#     self.cur_linear_y = data.pose.pose.position.y
#     self.cur_angular_z = data.pose.pose.orientation.z

# #Define the method which contains the node's main functionality
# def listener(obj):

#     rospy.init_node('closed_loop_control', anonymous=False)

#     angle = 0
#     distance = 0
#     topic = "/" + TURTLEBOT_ID + "/odom/"

#     tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
#     tf_listener = tf2_ros.TransformListener(self.tf_buffer)

#     cur_linear_x = -999
#     cur_linear_y = -999
#     cur_angular_z = -999

#     print("ENCODER LISTENER STARTED")

#     #Create a new instance of the rospy.Subscriber object which we can 
#     #use to receive messages of type std_msgs/String from the topic /chatter_talk.
#     #Whenever a new message is received, the method callback() will be called
#     #with the received message as its first argument.
#     # rospy.Subscriber("my_chatter_talk", TimestampString, callback)
#     rospy.Subscriber("/" + TURTLEBOT_ID + "/odom/", Odometry, callback)


#     #Wait for messages to arrive on the subscribed topics, and exit the node
#     #when it is killed with Ctrl+C
#     # rospy.spin()
#     r.sleep()

class open_loop_move():
    def __init__(self):
        # initiliaze
        # rospy.init_node('drawasquare', anonymous=False)

        # What to do you ctrl + c
        self.encoder = EncoderListener()    
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
        for x in range(0,time*self.update_rate): 
            self.cmd_vel.publish(go_forward_cmd)
            self.r.sleep()
    
    def go_backward(self, time, speed=0.2):
        # default speed is moving at 0.2 m/s
        rospy.loginfo("go backward for {0} s at speed {1} m/s".format(time, speed))
        go_backward_cmd = Twist()
        go_backward_cmd.linear.x = -speed
        go_backward_cmd.angular.z = 0
        for x in range(0,time*self.update_rate): 
            self.cmd_vel.publish(go_backward_cmd)
            self.r.sleep()

    def turn_right(self, time, speed=45):
        # default speed is turning at 45 deg/s
        turn_right_cmd = Twist()
        turn_right_cmd.linear.x = 0
        turn_right_cmd.angular.z = radians(speed); # convert 45 deg/s to radians/s
        rospy.loginfo("turn_right for {0} s at speed {1} deg/s".format(time, speed))
        for x in range(0,time*self.update_rate):
            self.cmd_vel.publish(turn_right_cmd)
            self.r.sleep()            

    def turn_left(self, time, speed=45):
        # default speed is turning at 45 deg/s
        turn_left_cmd = Twist()
        turn_left_cmd.linear.x = 0
        turn_left_cmd.angular.z = -radians(speed); # convert 45 deg/s to radians/s
        rospy.loginfo("turn left for {0} s at speed {1} def/s".format(time, speed))
        for x in range(0,time*self.update_rate):
            self.cmd_vel.publish(turn_left_cmd)
            self.r.sleep()
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
    encoder_listener = EncoderListener()
    draw_tri = open_loop_move()
    # draw_tri.curve_left(5)
    # draw_tri.go_forward(3, speed=0.9)
    # draw_tri.go_backward(3, speed = 0.3)
    # draw_tri.go_forward(2)
    # draw_tri.go_backward(2)
    # draw_tri.go_forward(2)
    # draw_tri.go_backward(2)
    # draw_tri.go_forward(2)
    # draw_tri.go_backward(2)
    # draw_tri.turn_right(2, speed=90)
    # draw_tri.curve_left(3)
    # draw_tri.go_forward(2)
    # draw_tri.turn_right(4, speed=90)
    # draw_tri.go_forward(2)
    draw_tri.turn_left_angle(200)
    # draw_tri.shutdown()
    # except:
        # rospy.loginfo("node terminated.")


