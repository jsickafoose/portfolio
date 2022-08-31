close all;

%% GyroX Axis
Array=csvread('GyroX.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);

X = mean(col1)

%% AccelY Axis
Array=csvread('GyroY.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);

Y = mean(col1)

%% AccelZ Axis
Array=csvread('GyroZ.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);

Z = mean(col1)

%% Bias Drift Over 30Minutes
Array=csvread('Gyro_Bias1.csv');
GyroX = Array(:, 1);
GyroY = Array(:, 2);
GyroZ = Array(:, 3);
TimeInMilli = Array(:, 4);

% Get coefficients of a line fit through the data.
coefficients_X = polyfit(TimeInMilli, GyroX, 1);
coefficients_Y = polyfit(TimeInMilli, GyroY, 1);
coefficients_Z = polyfit(TimeInMilli, GyroZ, 1);
% Create a new x axis with exactly 1000 points (or whatever you want).
xFit = linspace(min(TimeInMilli), max(TimeInMilli), 10000);
% Get the estimated yFit value for each of those 1000 new x locations.
yFit_X = polyval(coefficients_X , xFit);
yFit_Y = polyval(coefficients_Y , xFit);
yFit_Z = polyval(coefficients_Z , xFit);
% Plot everything.
Gyro1XCoefficients = polyfit(TimeInMilli, GyroX ,1)
Gyro1YCoefficients = polyfit(TimeInMilli, GyroY ,1)
Gyro1ZCoefficients = polyfit(TimeInMilli, GyroZ ,1)

figure('Name','Bias Drift Over 30Minutes','NumberTitle','off');
plot(TimeInMilli,GyroX, '.')
hold on;
plot(TimeInMilli,GyroY, '.')
plot(TimeInMilli,GyroZ, '.')
plot(xFit, yFit_X, 'r-', 'LineWidth', 2);
plot(xFit, yFit_Y, 'r-', 'LineWidth', 2);
plot(xFit, yFit_Z, 'r-', 'LineWidth', 2);
title('Reading vs Expected')
legend('X_Axis','Y_Axis','Z_Axis','BestFit_X','BestFit_Y','BestFit_Z')
xlabel('Time In Milli')
ylabel('Gyro Output')
hold off;

%% Bias Drift Over 1Hour
Array=csvread('Gyro_Bias2.csv');
GyroX = Array(:, 1);
GyroY = Array(:, 2);
GyroZ = Array(:, 3);
TimeInMilli = Array(:, 4);

% Get coefficients of a line fit through the data.
coefficients_X = polyfit(TimeInMilli, GyroX, 1);
coefficients_Y = polyfit(TimeInMilli, GyroY, 1);
coefficients_Z = polyfit(TimeInMilli, GyroZ, 1);
% Create a new x axis with exactly 1000 points (or whatever you want).
xFit = linspace(min(TimeInMilli), max(TimeInMilli), 10000);
% Get the estimated yFit value for each of those 1000 new x locations.
yFit_X = polyval(coefficients_X, xFit);
yFit_Y = polyval(coefficients_Y, xFit);
yFit_Z = polyval(coefficients_Z, xFit);
% Plot everything.
Gyro2XCoefficients = polyfit(TimeInMilli, GyroX ,1)
Gyro2YCoefficients = polyfit(TimeInMilli, GyroY ,1)
Gyro2ZCoefficients = polyfit(TimeInMilli, GyroZ ,1)

figure('Name','Bias Drift Over 1 Hour','NumberTitle','off');
plot(TimeInMilli,GyroX, '.')
hold on;
plot(TimeInMilli,GyroY, '.')
plot(TimeInMilli,GyroZ, '.')
plot(xFit, yFit_X, 'r-', 'LineWidth', 2);
plot(xFit, yFit_Y, 'r-', 'LineWidth', 2);
plot(xFit, yFit_Z, 'r-', 'LineWidth', 2);
title('Reading vs Expected')
legend('X_Axis','Y_Axis','Z_Axis','BestFit_X','BestFit_Y','BestFit_Z')
xlabel('Time in Milliseconds')
ylabel('Recorded Value')
hold off;