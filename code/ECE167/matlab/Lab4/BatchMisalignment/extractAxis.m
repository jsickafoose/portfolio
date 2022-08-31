function [lambda,phi] = extractAxis(R)
% function lambda = extractAxis(R)
%
% this function extracts the axis and angle from a rotation matrix
% uses the property that lambda-x = (R - R')
%                                   --------
%                                   2 sin Phi
phi = acos((trace(R)-1)/2);
lx = (R-R')/(2*sin(phi));
lambda = [lx(3,2);
          lx(1,3);
          lx(2,1)];