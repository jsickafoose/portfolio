clear;
clear clc;
close all;

dT = 1;

numSteps=30;

p=deg2rad(10);
q=deg2rad(0);
r=deg2rad(0);
gyroInput=[p;q;r];



nvector=[1;0;0];
evector=[0;-1;0];
dvector=[0;0;-1];



Ro=eye(3);

R=Ro;



[sX,sY,sZ]=sphere(30);
surf(sX,sY,sZ,'FaceAlpha',.1,'EdgeColor','none');
axis equal;
xlabel('x')
ylabel('y')
zlabel('z')
hold on

quiver3([0,0,0],[0,0,0],[0,0,0],[nvector(1),evector(1),dvector(1)],[nvector(2),evector(2),dvector(2)],[nvector(3),evector(3),dvector(3)]);
pause

for i=1:numSteps,
    gyroInputWithBias=gyroInput+[deg2rad(rand);deg2rad(rand);deg2rad(rand)]
    R= Rexp(gyroInputWithBias, dT) * R
    newNVector=R'*nvector;
    newEVector=R'*evector;
    newDVector=R'*dvector;
    quiver3([0,0,0],[0,0,0],[0,0,0],[newNVector(1),newEVector(1),newDVector(1)],[newNVector(2),newEVector(2),newDVector(2)],[newNVector(3),newEVector(3),newDVector(3)]);
    pause;
end

hold off
 