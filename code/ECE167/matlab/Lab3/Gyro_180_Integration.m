close all;

%% X Axis
Array=csvread('Gyro_180_X.csv');
GyroX = Array(:, 1);
TimeInMilliX = Array(:, 4);

GyroX = cumsum(GyroX*.02);

%% Y Axis
Array=csvread('Gyro_180_Y.csv');
GyroY = Array(:, 2);
TimeInMilliY = Array(:, 4);
TimeInMilliY = TimeInMilliY - 330000;

GyroY = cumsum(GyroY*.02);

%% Z Axis
Array=csvread('Gyro_180_Z.csv');
GyroZ = Array(:, 3)
TimeInMilliZ = Array(:, 4);
TimeInMilliZ = TimeInMilliZ + 81790;

GyroZ = cumsum(GyroZ*.02);

%% Plotting
figure('Name','Angle Vs. Time','NumberTitle','off');
plot(TimeInMilliX,GyroX, '.')
hold on;
plot(TimeInMilliY,GyroY, '.')
plot(TimeInMilliZ,GyroZ, '.')

title('Angle vs. Time')
legend('X Axis','Y Axis','Z Axis')
xlabel('Time In Milli')
ylabel('Gyro Angle')
hold off;