#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the rospy package. For an import to work, it must be specified
#in both the package manifest AND the Python file in which it is used.
import rospy

#Import the String message type from the /msg directory of
#the std_msgs package.
from my_chatter.msg import TimestampString

#Define the method which contains the main functionality of the node.
def talker():

  #Run this program as a new node in the ROS computation graph 
  #called /talker.
  rospy.init_node('my_chatter_talker', anonymous=True)

  #Create an instance of the rospy.Publisher object which we can 
  #use to publish messages to a topic. This publisher publishes 
  #messages of type std_msgs/String to the topic /chatter_talk
  pub = rospy.Publisher('my_chatter_talk', TimestampString, queue_size=10)

  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():
    print('Please enter a line of text and press <Enter>: ')
    uinput = raw_input()

    # Construct a string that we want to publish
    # (In Python, the "%" operator functions similarly
    #  to sprintf in C or MATLAB)
    pub_string = TimestampString()
    pub_string.user_input = uinput
    pub_string.timestamp = rospy.get_time()
    
    # Publish our string to the 'chatter_talk' topic
    pub.publish(pub_string)
      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method
  try:
    talker()
  except rospy.ROSInterruptException: pass
