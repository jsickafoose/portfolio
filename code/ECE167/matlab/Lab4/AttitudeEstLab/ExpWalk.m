
clear all;
clc;


R=eye(3);
dt=.1;
gyro=[0;0;0]
numsteps=2000;

RTracking = R(:)';
Thetas= [0];
RChangedTemp = (R'*R);
RChanged = RChangedTemp(:)';
for i=1:numsteps
    R=IntegrateOpenLoop(R,gyro,dt)
    Thetas(i+1)=asin(-R(1,3));
    Rtracking(i+1,:) = R(:)';
    RChangedTemp = (R'*R);
    RChanged(i+1,:) = RChangedTemp(:)';
    %plot(R)
end
figure(1);
subplot(1,2,1)
plot(Rtracking)
title("R over Time")
subplot(1,2,2)
plot(RChanged)
title("R'*R")
figure(2);
plot(Thetas, '.')
title("Theta over Time")