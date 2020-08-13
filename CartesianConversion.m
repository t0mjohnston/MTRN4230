%Jordan Rockoff scripting centroid translation
%z5160388

%Interpret from centroids ( camera found ) the XYZ of the objects in the simulation
function [finalx,finaly,fiz]=CartesianConversion(x_im,y_im)
%modifiable Vals
s=0; %zero skew
f=174.4; %(mm) %focal length of Kinect Camera
sx=10; %pixel width (mm)
sy=10; %pixel heigh (mm)
Z=280; %(mm) depth to table objects are approx 0.04 to 0.05m    196
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

fix=(cameraX-X)/1000;
fiy=(cameraY-Y)/2800;
fiz=(cameraZ-Z)/1000; 
%final_in_metres
x_p=[-0.2,-0.075,0.05,.175];
y_p=[.225,.1,-0.025,-0.15];
x_i=[173,265,356,447];
y_i=[74,165,257,348];

kappa=22;
zappa=22;
index=1;
indeyy=1;
for k=1:1:4
    if kappa > abs(x_im-x_i(k))
        kappa=abs(x_im-x_i(k));
        index=k;
    end
    if zappa > abs(y_im-y_i(k))
        zappa= abs(y_im-y_i(k));
        indeyy=k;
    end
end


finalx=x_p(index);
finaly=y_p(indeyy);

end