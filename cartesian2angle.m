%Given XYZ (cartesian) coordinates, convert these to joint angles 
close all; clear variables; clc;
%% Cartesian coordinates
goalPos = [-0.25,0.5,0.7+0.09465]; %X,Y,Z

%% SETUP/CONNECT TO GAZEBO/ROS
ipaddress = '192.168.0.18';
robotType = 'Gazebo';
rosshutdown;
rosinit(ipaddress);
blockposes = rossubscriber('/gazebo/link_states');
pause(2);
posdata = receive(blockposes,10);
imSub = rossubscriber('/camera/color/image_raw');
pcSub = rossubscriber('/camera/depth/points');
testIm  = readImage(imSub.LatestMessage);
imshow(testIm);
rostopic list;

%% Load robot and read joint states from Gazebo/ROS
robot = loadrobot('universalUR5');
showdetails(robot);

%% Read Joint states
jointSub = rossubscriber('joint_states'); %Needs to connect to ROS/Gazebo?
JointStateGazebo = receive(jointSub);
JointPositionGazebo = exampleHelperJointMsgToStruct(robot,JointStateGazebo);

%% Forward kinematics
wp1 = trvec2tform(goalPos); %Converts XYZ to a transform, produces similar result to fkine matrix
disp('XYZ to T matrix');
disp(wp1);

%% Inverse kinematics
ik = inverseKinematics('RigidBodyTree',robot);
weights = [0.25 0.25 0.25 1 1 1];
%initialguess = robot.homeConfiguration;
[configSol,solInfo] = ik('tool0',wp1,weights,JointPositionGazebo); %Feed in current joint state read from ROS
%The end effector points upwards, multiply by -1 to flip it
configSol(5).JointPosition = configSol(5).JointPosition*-1;

%% Display
figure(1);
show(robot,configSol);
title('From wp1 (trvec2tform)');

for i = 1:1:numel(configSol)
    disp(configSol(i).JointPosition);
end

%IS THIS LITERALLY JUST THE KINEMATICS THAT AGGY WROTE UP?!