#!/usr/bin/python
#
# Send joint values to UR5 using messages
#

from std_msgs.msg import Header
from geometry_msgs.msg import Pose
from copy import deepcopy

import rospy
import sys
import moveit_commander

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

# wp1 = float(sys.argv[1])
# wp2 = float(sys.argv[2])
# wp3 = float(sys.argv[3])
# wp4 = float(sys.argv[4])
# wp5 = float(sys.argv[5])
# wp6 = float(sys.argv[6])

# Target positions for the arm
# Currently hard-coded, get these from input/rostopic when ready
arm_tx1 = 0.175
arm_ty1 = -0.150
arm_tz1 = 0.200

arm = None

def moveit_cleanup():
    rospy.loginfo("Stopping the robot")
    # Stop any current arm movement
    if arm: 
        arm.stop()

    #Shut down MoveIt! cleanly
    rospy.loginfo("Shutting down Moveit!")
    moveit_commander.roscpp_shutdown()
    moveit_commander.os._exit(0)

def moveto_xyz(arm_tx, arm_ty, arm_tz, pub):

    #rospy.init_node('send_joints')
    rospy.on_shutdown(moveit_cleanup)
    # Initialize the move_group API
    moveit_commander.roscpp_initialize(sys.argv)
    arm = moveit_commander.MoveGroupCommander('manipulator')

    # Get the name of the end-effector link
    end_effector_link = arm.get_end_effector_link()
    # Set the reference frame for pose targets
    reference_frame = "/base_link"

    # Set the ur5_arm reference frame accordingly
    arm.set_pose_reference_frame(reference_frame)
    # Allow replanning to increase the odds of a solution
    arm.allow_replanning(True)
    # Allow some leeway in position (meters) and orientation (radians)
    arm.set_goal_position_tolerance(0.01)
    arm.set_goal_orientation_tolerance(0.1)

    # Get the current pose so we can add it as a waypoint
    start_pose = arm.get_current_pose(end_effector_link).pose

    # Initial waypoints
    waypoints = []

    waypoints.append(start_pose) 
    wpose = deepcopy(start_pose)
    
    # Get rid of these when you know what path you want to assign
    # arm_tx = wpose.position.x + 0.20
    # arm_ty = wpose.position.y + 0.10
    # arm_tz = wpose.position.z - 0.20

    wpose.position.x = arm_tx
    wpose.position.y = arm_ty - 0.700
    wpose.position.z = arm_tz
    waypoints.append(deepcopy(wpose))

    fraction = 0.0
    maxtries = 100
    attempts = 0 
    # Set the internal state to the current state
    arm.set_start_state_to_current_state()

    # Plan the Cartesian path connecting the waypoints
    while fraction < 1.0 and attempts < maxtries:
        (plan, fraction) = arm.compute_cartesian_path (waypoints, 0.01, 0.0, True)
        # Increment the number of attempts
        attempts += 1
        # Print out a progress message
        if attempts % 10 == 0:
            rospy.loginfo("Still trying after " + str(attempts) + " attempts...")

    # If we have a complete plan, execute the trajectory
    if fraction == 1.0:
        rospy.loginfo("Path computed successfully. Moving the arm.")
        num_pts = len(plan.joint_trajectory.points)

        rospy.loginfo("\n# waypoints: "+str(num_pts))
        waypoints = []
        for i in range(num_pts):
            waypoints.append(plan.joint_trajectory.points[i].positions)
    else:
        rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")
        return



    # Create the topic message
    traj = JointTrajectory()
    traj.header = Header()
    # Joint names for UR5
    traj.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                        'wrist_3_joint']

    rate = rospy.Rate(20)
    cnt = 0
    pts = JointTrajectoryPoint()
    

    # while not rospy.is_shutdown():
    while cnt < len(waypoints): 
        traj.header.stamp = rospy.Time.now()
        
        pts.positions = waypoints[cnt % num_pts]
        pts.time_from_start = rospy.Duration(0.001*cnt) #previously 1

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        pub.publish(traj)
        cnt += 1 # put this at start of loop to return to home/original position 
        # or leave here to compute new path to home
        rate.sleep()

if __name__ == '__main__':
    try:
        pub = rospy.Publisher('/arm_controller/command',
                              JointTrajectory,
                              queue_size=10)
        move_xyz(arm_tx1, arm_ty1, arm_tz1, pub)
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")
