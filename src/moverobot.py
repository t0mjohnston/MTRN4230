#!/usr/bin/python
#
# Send joint values to UR5 using messages
#

from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectory

from trajectory_msgs.msg import JointTrajectoryPoint
import rospy
import sys


def cycle(wp1,wp2,wp3,wp4,wp5,wp6,pub,pubgrip):

    waypoints = [[1.79258668703901,-1.71664182898895,-1.57683370118371,-1.67722132469095,-1.57056759784320,0],[wp1+1,wp2+1,wp3+1,wp4+1,wp5+1,wp6+1],[wp1,wp2,wp3,wp4,wp5,wp6],[wp1+1,wp2+1,wp3+1,wp4+1,wp5+1,wp6+1],[0,0,0,0,0,0]]                   
    
    # Create the topic message
    traj = JointTrajectory()
    traj.header = Header()
    # Joint names for UR5
    traj.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                        'wrist_3_joint']

    rate = rospy.Rate(1)
    cnt = -1
    pts = JointTrajectoryPoint()
    traj.header.stamp = rospy.Time.now()

    while not (rospy.is_shutdown() or cnt>3):
        cnt += 1

        traj.header.stamp = rospy.Time.now()
        rospy.loginfo("count num %d", cnt)
        pts.positions = waypoints[cnt%4]

        pts.time_from_start = rospy.Duration(1.0)

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        pub.publish(traj)
        rate.sleep()

        if cnt == 2:
            pubgrip.publish(True)
            pause(2)
        elif cnt == 4:
            pubgrip.publish(False)
            pause(2)


if __name__ == '__cycle__':
    try:
        cycle()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")
