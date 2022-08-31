close all;

%% Uncalibrated 3D Magnetometer Data
Array=csvread('MagUncal.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);
col3 = Array(:, 3);

figure('Name','Uncalibrated 3D Magnetometer Data','NumberTitle','off');
plot3(col1,col2,col3, '.')
hold on;
title('Uncalibrated 3D Magnetometer Data')
xlabel('X Axis')
ylabel('Y Axis')
zlabel('Z Axis')
hold off;

MagnetometerArray=csvread('MagCal.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);
col3 = Array(:, 3);

figure('Name','Magnetometer 3D Accelerometer Data','NumberTitle','off');
plot3(col1,col2,col3, '.')
hold on;
title('Calibrated 3D Magnetometer Data')
xlabel('X Axis')
ylabel('Y Axis')
zlabel('Z Axis')
hold off;