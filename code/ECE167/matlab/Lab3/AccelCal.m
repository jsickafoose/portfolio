close all;

%% Uncalibrated 3D Accelerometer Data
Array=csvread('AccelUncal.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);
col3 = Array(:, 3);

figure('Name','Uncalibrated 3D Accelerometer Data','NumberTitle','off');
plot3(col1,col2,col3, '.')
hold on;
title('Uncalibrated 3D Accelerometer Data')
xlabel('X Axis')
ylabel('Y Axis')
zlabel('Z Axis')
hold off;

%% Uncalibrated 3D Accelerometer Data
Array=csvread('AccelCal.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);
col3 = Array(:, 3);

figure('Name','Calibrated 3D Accelerometer Data','NumberTitle','off');
plot3(col1,col2,col3, '.')
hold on;
title('Calibrated 3D Accelerometer Data')
xlabel('X Axis')
ylabel('Y Axis')
zlabel('Z Axis')
hold off;