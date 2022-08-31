close all;
clc;

%% Initializations
deltaT = 0.02; % dT = 0.02sec = 20ms or 50Hz
noiseFlag = 1; % 0 = No noise, 1 = Random noise

[Acc,Mag,wGyro,Eul] = CreateTrajectoryData(deltaT,noiseFlag);

% Inits Yaw, Pitch, Roll from the first Euler angle row which are the raw
% true angles
yaw = Eul(1, 1)
pitch = Eul(1, 2)
roll = Eul(1, 3)

% Euler to DCM from the known true Euler values
r_yaw = [cosd(yaw),  sind(yaw), 0;
         -sind(yaw), cosd(yaw), 0;
         0,         0,        1];

r_pitch = [cosd(pitch), 0, -sind(pitch);
           0,          1,  0;
           sind(pitch), 0,  cosd(pitch)];~

r_roll = [1,  0,         0;
          0,  cosd(roll), sind(roll);
          0, -sind(roll), cosd(roll)];

Rminus = (r_roll * r_pitch) * r_yaw; % Inits Rminus as the first DCM attitude

% DCM to Euler
    % Yaw
    yaw_temp = rad2deg(atan2(Rminus(1,2), Rminus(1,1)))
    
    % Pitch
    if Rminus(1,3) < -1
        pitch_temp = rad2deg(-asin(-1))

    elseif Rminus(1,3) > 1
        pitch_temp = rad2deg(-asin(1))

    else
        pitch_temp = rad2deg(-asin(Rminus(1,3)))
    end
    
    % Roll
    roll_temp = rad2deg(atan2(Rminus(2,3), Rminus(3,3)))

% R = Rminus;
%% Forward integration
for i = 1:3330
    % Fetching Gyro at i
    gyros = [deg2rad((wGyro(i, 1))/131);
             (deg2rad(wGyro(i, 2))/131);
             (deg2rad(wGyro(i, 3))/131)];
    
    % Updating DCM
    Rminus = Rminus - rcross(gyros) * Rminus * deltaT; % I think sometime around i = 202, Rminus starts to = NaN

    % % DCM to Euler
    % Yaw
    y_angleYaw(i) = rad2deg(atan2(Rminus(1,2), Rminus(1,1)));
    
    % Pitch
    if Rminus(1,3) < -1
        y_anglePitch(i) = rad2deg(-asin(-1));

    elseif Rminus(1,3) > 1
        y_anglePitch(i) = rad2deg(-asin(1));

    else
        y_anglePitch(i) = rad2deg(-asin(Rminus(1,3)));
    end
    
    % Roll
    y_angleRoll(i) = rad2deg(atan2(Rminus(2,3), Rminus(3,3)));

    % Storing current time for plotting
    x_time(i) = deltaT*i;
    % Saving Actual Euler value
    yaw_Actual(i) = Eul(i, 1);
    pitch_Actual(i) = Eul(i, 2);
    roll_Actual(i) = Eul(i, 3);
end

figure('Name','Forward Integration Angle vs. Time','NumberTitle','off');
subplot(3,1,1);
plot(x_time,y_angleYaw, '-')
hold on;
plot(x_time,yaw_Actual, '-')
title('Forward Integration Angle vs. Time')
ylabel('Yaw (degrees)')
legend('Calculated','Actual')
hold off;

subplot(3,1,2)
plot(x_time,y_anglePitch, '-')
hold on;
plot(x_time,pitch_Actual, '-')
ylabel('Pitch (degrees)')
legend('Calculated','Actual')
hold off;

subplot(3,1,3)
plot(x_time,y_angleRoll, '-')
hold on;
plot(x_time,roll_Actual, '-')
legend('Calculated','Actual')
xlabel('Time (sec)')
ylabel('Roll (degrees)')
hold off;

%% Matrix Exponential Form Integration
Rminus = (r_roll * r_pitch) * r_yaw;
for i = 1:3330
    % Fetching Gyro at i
    gyros = [(deg2rad(wGyro(i, 1))/131);
             (deg2rad(wGyro(i, 2))/131);
             (deg2rad(wGyro(i, 3))/131)];
    
    % Updating DCM
    Rminus = Rexp(gyros, deltaT) * Rminus;

    % % DCM to Euler
    % Yaw
    y_angleYaw(i) = rad2deg(atan2(Rminus(1,2), Rminus(1,1)));
    
    % Pitch
    if Rminus(1,3) < -1
        y_anglePitch(i) = rad2deg(-asin(-1));

    elseif Rminus(1,3) > 1
        y_anglePitch(i) = rad2deg(-asin(1));

    else
        y_anglePitch(i) = rad2deg(-asin(Rminus(1,3)));
    end
    
    % Roll
    y_angleRoll(i) = rad2deg(atan2(Rminus(2,3), Rminus(3,3)));

    % Storing current time for plotting
    x_time(i) = deltaT*i;
end

figure('Name','Matrix Exponential Integration vs. Time','NumberTitle','off');
subplot(3,1,1);
plot(x_time,y_angleYaw, '-')
hold on;
plot(x_time,yaw_Actual, '-')
title('Matrix Exponential Integration Angle vs. Time')
ylabel('Yaw (degrees)')
legend('Calculated','Actual')
hold off;


subplot(3,1,2)
plot(x_time,y_anglePitch, '-')
hold on;
plot(x_time,pitch_Actual, '-')
ylabel('Pitch (degrees)')
legend('Calculated','Actual')
hold off;


subplot(3,1,3)
plot(x_time,y_angleRoll, '-')
hold on;
plot(x_time,roll_Actual, '-')
legend('Calculated','Actual')
xlabel('Time (sec)')
ylabel('Roll (degrees)')
hold off;