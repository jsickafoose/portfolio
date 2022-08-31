close all;

%% AccelX Axis
Array=csvread('AccelX.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);

% Get coefficients of a line fit through the data.
coefficients = polyfit(col1, col2, 1);
% Create a new x axis with exactly 1000 points (or whatever you want).
xFit = linspace(min(col1), max(col1), 1000);
% Get the estimated yFit value for each of those 1000 new x locations.
yFit = polyval(coefficients , xFit);
% Plot everything.
AccelXCoefficients = polyfit(col1, col2 ,1)

figure('Name','AccelX Axis','NumberTitle','off');
plot(col1,col2, '.')
hold on;
plot(xFit, yFit, 'r-', 'LineWidth', 2);
title('Reading vs Expected')
legend('Real','Best Fit Line')
xlabel('Reading')
ylabel('Expected')
hold off;

%% AccelY Axis
Array=csvread('AccelY.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);

% Get coefficients of a line fit through the data.
coefficients = polyfit(col1, col2, 1);
% Create a new x axis with exactly 1000 points (or whatever you want).
xFit = linspace(min(col1), max(col1), 1000);
% Get the estimated yFit value for each of those 1000 new x locations.
yFit = polyval(coefficients , xFit);
% Plot everything.
AccelYCoefficients = polyfit(col1, col2 ,1)

figure('Name','AccelY Axis','NumberTitle','off');
plot(col1,col2, '.')
hold on;
plot(xFit, yFit, 'r-', 'LineWidth', 2);
title('Reading vs Expected')
legend('Real','Best Fit Line')
xlabel('Reading')
ylabel('Expected')
hold off;

%% AccelZ Axis
Array=csvread('AccelZ.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);

% Get coefficients of a line fit through the data.
coefficients = polyfit(col1, col2, 1);
% Create a new x axis with exactly 1000 points (or whatever you want).
xFit = linspace(min(col1), max(col1), 1000);
% Get the estimated yFit value for each of those 1000 new x locations.
yFit = polyval(coefficients , xFit);
% Plot everything.
AccelZCoefficients = polyfit(col1, col2 ,1)

figure('Name','AccelZ Axis','NumberTitle','off');
plot(col1,col2, '.')
hold on;
plot(xFit, yFit, 'r-', 'LineWidth', 2);
title('Reading vs Expected')
legend('Real','Best Fit Line')
xlabel('Reading')
ylabel('Expected')
hold off;