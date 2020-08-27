#!/usr/bin/python
#
# Send joint values to UR5 using messages
#

from std_msgs.msg import Header
from geometry_msgs.msg import Pose
from copy import deepcopy

import rospy
import sys

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

wp1 = float(sys.argv[1])
wp2 = float(sys.argv[2])
wp3 = float(sys.argv[3])
wp4 = float(sys.argv[4])
wp5 = float(sys.argv[5])
wp6 = float(sys.argv[6])

def main():

    rospy.init_node('send_joints')

    waypoints = [[0.0, 0, 0, 0, 0, 0], [wp1,wp2,wp3,wp4,wp5,wp6]]
    pub = rospy.Publisher('/arm_controller/command',
                          JointTrajectory,
                          queue_size=10)

    # Create the topic message
    traj = JointTrajectory()
    traj.header = Header()
    # Joint names for UR5
    traj.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                        'wrist_3_joint']

    rate = rospy.Rate(1)
    cnt = 0
    pts = JointTrajectoryPoint()
    traj.header.stamp = rospy.Time.now()

    while not rospy.is_shutdown():
        cnt += 1
        
        pts.positions = waypoints[1]

        pts.time_from_start = rospy.Duration(1.0)

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        pub.publish(traj)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")
