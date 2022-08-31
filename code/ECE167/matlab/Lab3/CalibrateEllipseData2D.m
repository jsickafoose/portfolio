function [Atilde,Btilde] = CalibrateEllipseData2D(x,y,kstep,plotFlag)
% function [Atilde,Btilde] = CalibrateEllipseData2D(x,y,kstep,plotFlag)
%
% Calibrates 2D elliptical data from sensors using the iterated least
% squares matrix method outlines in "Iterative calibration method for 
% inertial and magnetic sensors" by Eric Dorveaux
%
% Input data is the (noisy) x and y of the sensor.
% k is the number of iterations for the process to take
% plotFlag is 1 will show the points change as the iteration steps continue
%
Atilde = eye(2);
Btilde = [0;0];

xi = x;
yi = y;

M = zeros(length(xi)*2,6);
Y = zeros(length(xi)*2,1);

if plotFlag,
    figure(1), clf
    r = 1.0;
    th = [0:2:360]';
    plot(r*cos(th*pi/180),r*sin(th*pi/180),'k-',xi,yi,'.');
    axis('equal');
    hold on
end

% Iterate through estimation process
% kstep should be somewhere between 2-20
%
for k = 1:kstep, 
    for i = 1:length(xi)
        M(i*2-1,:) = [xi(i) yi(i) 0 0 1 0];
        M(i*2,:)   = [0 0 xi(i) yi(i) 0 1];
        Y(i*2-1:i*2) = (1/sqrt(xi(i)^2+yi(i)^2))*[xi(i);yi(i)];
    end
    p = M\Y;    % do the least squares for A and B elements
    Akplus = [p(1) p(2);p(3) p(4)];
    Bkplus = [p(5); p(6)];
    
    xyplus = (Akplus*[xi';yi'])'; % update the xi,yi pairs
    xi = xyplus(:,1)+Bkplus(1);
    yi = xyplus(:,2)+Bkplus(2);
    
    Btilde = Akplus*Btilde + Bkplus;
    Atilde = Akplus*Atilde;
    
    if plotFlag,
        plot(xi,yi,'.');
    end
end

if plotFlag,
    figure(2), clf
    plot([sqrt(x.^2+y.^2) sqrt(xi.^2+yi.^2)],'.');
    legend('Pre-Calibration','Post-Calibration');
    title('Norm of data pre- and post-Calibration');
end


