close all;

%% MagX Axis
Array=csvread('MagX.csv');
col1 = Array(:, 1);

X = mean(col1)

%% MagY Axis
Array=csvread('MagY.csv');
col2 = Array(:, 2);

Y = mean(col2)

%% MagZ Axis
Array=csvread('MagZ.csv');
col3 = Array(:, 3);

Z = mean(col3)