#!/usr/bin/env python

from std_msgs.msg import Int16
from std_msgs.msg import Empty
from std_msgs.msg import Header
from geometry_msgs.msg import Point
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

import numpy as np
import geometry_msgs.msg
import moveit_msgs.msg

from copy import deepcopy
import moveit_commander

from std_msgs.msg import Header
from std_msgs.msg import Bool
from std_srvs.srv import Empty

import rospy
import sys
import moverobot
import time

import moverobot_xyz 

matFlag = 0;
wp1 = 0;
wp2 = 0;
wp3 = 0;
wp4 = 0;
wp5 = 0;
wp6 = 0;
dumbBug = 0;

def callback(data):
    rospy.loginfo("Flag from Matlab: %d", data.data)
    global matFlag
    matFlag = data.data;

def hollaback(data):
    global wp1
    global wp2
    global wp3
    wp1 = data.x
    wp2 = data.y
    wp3 = data.z
    rospy.loginfo("Test: %f %f %f", wp1, wp2, wp3)

def hollaback2(data):
    global wp4
    global wp5
    global wp6
    wp4 = data.x
    wp5 = data.y
    wp6 = data.z
    rospy.loginfo("Test: %f %f %f %f %f %f", wp1, wp2, wp3, wp4, wp5, wp6)

def hook():
    global dumbBug # This means what you think it does
    dumbBug = 1;

def main():

    rospy.init_node('py_comm')
    pub2 = rospy.Publisher('py_comms',
                          Int16,
                          queue_size=10)

    pub = rospy.Publisher('/arm_controller/command',
                          JointTrajectory,
                          queue_size=10)

    pubgrip = rospy.Publisher('/gripper_on',
                          Bool,
                          queue_size=10)

    cnt = 0
    test = 0
    rate = rospy.Rate(1)
    
    rospy.on_shutdown(hook) # Dumb bug error handling

    while not rospy.is_shutdown():
        # Initialize flag that MATLAB will listen for
        test = 1
        # Update the local storage of the flag from MATLAB
        rospy.Subscriber("mat_comms",Int16,callback)
        
        # Wait until MATLAB flag that data has been updated before continuing
        while not bool(matFlag):
            rospy.Subscriber("mat_comms",Int16,callback)
            rospy.loginfo("Waiting on Flag...")
            time.sleep(2)
            if(dumbBug): # This is a dumb bug that makes your terminal go rogue 
                break    # unless you break the while loop. It wont let 
                         # you ctrl+C your program otherwise wtf
        time.sleep(6)
        # Read data in from MATLAB
        rospy.Subscriber("mat_out",Point,hollaback)
        #rospy.Subscriber("mat_out2",Point,hollaback2)
        time.sleep(5)
        # Move the robot through the three default and one variable waypoint

        #moverobot.cycle(wp1,wp2,wp3,wp4,wp5,wp6,pub,pubgrip)
        moverobot_xyz.moveto_xyz(wp1,wp2,0.234,pub,40)

        moverobot_xyz.moveto_xyz(wp1,wp2,0.028,pub,40)
        #moverobot_xyz.moveto_xyz(wp1,wp2,0.06,pub)

        time.sleep(0.1)
        pubgrip.publish(True)
        moverobot_xyz.moveto_xyz(wp1,wp2,0.05,pub,25)
        moverobot_xyz.moveto_xyz(-0.51,0.2,0.234,pub,40)
        moverobot_xyz.moveto_xyz(-0.51,0.2,0.07,pub,25)
        time.sleep(0.2)
        pubgrip.publish(False)
        moverobot_xyz.moveto_xyz(-0.51,0.2,0.234,pub,40)

        #time.sleep(5) # This is to simulate the robot moving delay for testing purposes

        # Send flag to topic that MATLAB can restart its loop
        rospy.loginfo(test)
        pub2.publish(test)
        rate.sleep()

        # Wait so MATLAB definitely notices the flag (probably should do a 2 way
        #                                             confirmation flag but ceebs)
        time.sleep(1)

        # Reset the flag
        test = 0
        
        # Publish the flag to topic
        rospy.loginfo(test)
        pub2.publish(test)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")
