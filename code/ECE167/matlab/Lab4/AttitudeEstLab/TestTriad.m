Ro=eye(3);
angleX = deg2rad(randn(1));
angleY = deg2rad(randn(1));
angleZ = deg2rad(randn(1));
rotX=[1 0 0; 0 cos(angleX) -sin(angleX); 0 sin(angleX) cos(angleX)];
rotY=[cos(angleY) 0 sin(angleY); 0 1 0; -sin(angleY) 0 cos(angleY)];
rotZ=[cos(angleZ) -sin(angleZ) 0; sin(angleZ) cos(angleZ) 0; 0 0 1];
Ro=rotX*rotY*rotZ;

accelInertial=[0;0;-1];
accelReading=Ro*[0;0;-1];
magInertial=[1;0;0];
magReading=Ro*[1;0;0];

R = DCMfromTriad(magReading,accelReading,magInertial,accelInertial);

R-Ro