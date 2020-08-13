%Jordan Rockoff scripting centroid translation
%z5160388

%Interpret from centroids ( camera found ) the XYZ of the objects in the simulation
function [fx,fy,fz]=CartesianConversion(x_im,y_im)
%modifiable Vals
s=0; %zero skew
f=176.9; %(mm) %focal length of Kinect Camera
sx=100; %pixel width (mm)
sy=3000; %pixel heigh (mm)
Z=196; %(mm) depth to table objects are approx 0.04 to 0.05m
cx=240; %in pixels
cy=320;

x_pxl=cx+x_im/sx;
y_pxl=cy+y_im/sy;

fx=f/sx;
fy=f/sy;
K=[fx,s,cx;
      0,fy,cy;
      0,0,1;];
Rt=[1,0,0,0;
       0,1,0,0;
       0,0,1,0;];
%characteristic equation
syms X Y;
Dest=[X;Y;Z;1];
Char_A=K*Rt*Dest;
%solve for x3
x3=double(Char_A(3));

x1=x_pxl*x3; %using the destination we wish to back project the location of 
x2=y_pxl*x3;
%solve for X and Y and produce XYZ of the object
Vec1=linsolve(K*Rt,[x1;x2;x3;]);
X=Vec1(1);
Y=Vec1(2);

%Zcheck=Vec1(3);

cameraX=0;
cameraY=0;
cameraZ=1000; %1 metre above ground

fx=(cameraX-X)/1000;
fy=(cameraY-Y)/2600;
fz=(cameraZ-Z)/1000; 
%final_in_metres

end