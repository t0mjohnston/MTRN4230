%Given XYZ (cartesian) coordinates, convert these to joint angles 
close all; clear variables; clc;

%Cartesian coordinates
goalPos = [-0.25,0.5,0.7]; %X,Y,Z

robot = loadrobot('universalUR5');
showdetails(robot);
%randPos = randomConfiguration(robot); %This is in angles, need to put in xyz! Is it even needed?

%Forward kinematics
wp1 = trvec2tform(goalPos); %Converts XYZ to a transform, produces similar result to fkine matrix
disp('XYZ to T matrix');
disp(wp1);

%Inverse kinematics
ik = inverseKinematics('RigidBodyTree',robot);
weights = [0.25 0.25 0.25 1 1 1];
initialguess = robot.homeConfiguration;
[configSol,solInfo] = ik('tool0',wp1,weights,initialguess); %Feed i current joint state read from ROS instead of the initialguess

%The end effector points upwards, multiply by -1 to flip it
configSol(5).JointPosition = configSol(5).JointPosition*-1;

figure(1);
show(robot,configSol);
title('From wp1 (trvec2tform)');

%IS THIS LITERALLY JUST THE KINEMATICS THAT AGGY WROTE UP?!