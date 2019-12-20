#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the dependencies as described in example_pub.py
import rospy
from geometry_msgs.msg import PoseStamped
import time

#Define the callback method which is called whenever this node receives a 
#message on its subscribed topic. The received message is passed as the 
#first argument to callback().
def callback(message):

    #Print the contents of the message to the console
    # print('Message: ' + message.user_input + ', Sent at: ' + str(message.timestamp) + \
    #       ', Received at: ' + str(rospy.get_time()))


    """
    sample message 
    header: 
      seq: 144
      stamp: 
        secs: 1574728710
        nsecs: 416430552
      frame_id: "world"
    pose: 
      position: 
        x: -1.58865058422
        y: 2.75253391266
        z: 1.18586134911
      orientation: 
        x: -0.0389922335744
        y: 0.00612592697144
        z: 0.710290193558
        w: -0.702801465988
    """


    print('all message\n {0}'.format(message))
    print("")
    print('position\n {0}'.format(message.pose.position))
    print("")
    # time.sleep(100)

#Define the method which contains the node's main functionality
def listener(obj):

    #Run this program as a new node in the ROS computation graph
    #called /listener_<id>, where <id> is a randomly generated numeric
    #string. This randomly generated name means we can start multiple
    #copies of this node without having multiple nodes with the same
    #name, which ROS doesn't allow.
    rospy.init_node('listener', anonymous=True)

    # 50 HZ = 0.2s Around 0.2s will receive one message of the location
    r = rospy.Rate(50)

    #Create a new instance of the rospy.Subscriber object which we can 
    #use to receive messages of type std_msgs/String from the topic /chatter_talk.
    #Whenever a new message is received, the method callback() will be called
    #with the received message as its first argument.
    # rospy.Subscriber("my_chatter_talk", TimestampString, callback)
    rospy.Subscriber("mocap_node/pose/" + obj, PoseStamped, callback)


    #Wait for messages to arrive on the subscribed topics, and exit the node
    #when it is killed with Ctrl+C
    # rospy.spin()
    r.sleep()


#Python's syntax for a main() method
if __name__ == '__main__':
    listener("cap1")
