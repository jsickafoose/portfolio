clear;
clear clc;
clf;

numSteps=200;

p=deg2rad(0);
q=deg2rad(0);
r=deg2rad(0);
gyroInput=[p;q;r];

biasTerms=[.1;.1;.1];
%biasTerms=[.0;.0;.0];
accelInertial=[0;0;-1];
accelReading=[0;0;-1];
magInertial=[1;0;0];
magReading=[1;0;0];

Kp_a=.2;
Ki_a=Kp_a/10;

Kp_m=.2;
Ki_m=Kp_m/10;

biasEstimate=[0;0;0];
nvector=[1;0;0];
evector=[0;-1;0];
dvector=[0;0;-1];



Ro=eye(3);
angleX = deg2rad(30);
angleY = deg2rad(30);
angleZ = deg2rad(30);
rotX=[1 0 0; 0 cos(angleX) -sin(angleX); 0 sin(angleX) cos(angleX)];
rotY=[cos(angleY) 0 sin(angleY); 0 1 0; -sin(angleY) 0 cos(angleY)];
rotZ=[cos(angleZ) -sin(angleZ) 0; sin(angleZ) cos(angleZ) 0; 0 0 1];
Ro=rotX*rotY*rotZ;

initNVector=Ro*nvector;
initEVector=Ro*evector;
initDVector=Ro*dvector;

R=Ro;



[sX,sY,sZ]=sphere(30);
surf(sX,sY,sZ,'FaceAlpha',.1,'EdgeColor','none');
axis equal;
xlabel('x')
ylabel('y')
zlabel('z')
hold on

quiver3([0,0,0],[0,0,0],[0,0,0],[initNVector(1),initEVector(1),initDVector(1)],[initNVector(2),initEVector(2),initDVector(2)],[initNVector(3),initEVector(3),initDVector(3)],0);
pause

for i=1:numSteps,              
    gyroInputWithBias=gyroInput+biasTerms;
    [R,biasEstimate] = IntegrateClosedLoop(R,biasEstimate,gyroInputWithBias,magReading,accelReading,magInertial,accelInertial,.1)
    newNVector=R'*nvector;
    newEVector=R'*evector;
    newDVector=R'*dvector;
    quiver3([0,0,0],[0,0,0],[0,0,0],[newNVector(1),newEVector(1),newDVector(1)],[newNVector(2),newEVector(2),newDVector(2)],[newNVector(3),newEVector(3),newDVector(3)],0);
 pause;
end

hold off