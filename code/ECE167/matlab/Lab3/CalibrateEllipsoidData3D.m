function [Atilde,Btilde] = CalibrateEllipsoidData3D(x,y,z,kstep,plotFlag)
% function [Atilde,Btilde] = CalibrateEllipsoidData3D(x,y,z,kstep,plotFlag)
%
% Calibrates 3D elliptical data from sensors using the iterated least
% squares matrix method outlines in "Iterative calibration method for 
% inertial and magnetic sensors" by Eric Dorveaux
%
% Input data is the (noisy) x and y of the sensor.
% k is the number of iterations for the process to take
% plotFlag is 1 will show the points change as the iteration steps continue
%
Atilde = eye(3);
Btilde = -[mean(x);mean(y);mean(z)];

xi = x;
yi = y;
zi = z;

xyzplus = (Atilde*[xi';yi';zi'])'; % update the xi,yi,zi tuples
xi = xyzplus(:,1)+Btilde(1);
yi = xyzplus(:,2)+Btilde(2);
zi = xyzplus(:,3)+Btilde(3);



M = zeros(length(xi)*3,12);
Y = zeros(length(xi)*3,1);

if plotFlag,
    figure(1), clf
    [xx,yy,zz] = sphere(30);
    surf(xx,yy,zz,'FaceAlpha',0.1);
    xlabel('x');
    ylabel('y');
    zlabel('z');
    title('Visualization of Walk In for Each Step of Calibration')
    axis('equal');
    hold on
    plot3(xi,yi,zi,'.');
end

Atracking = Atilde(:)';
Btracking = Btilde(:)';

% Iterate through estimation process
% kstep should be somewhere between 2-20
%
for k = 1:kstep, 
    for i = 1:length(xi)
        M(i*3-2,:) = [xi(i) yi(i) zi(i) 0 0 0 0 0 0 1 0 0];
        M(i*3-1,:) = [0 0 0 xi(i) yi(i) zi(i) 0 0 0 0 1 0];
        M(i*3,:)   = [0 0 0 0 0 0 xi(i) yi(i) zi(i) 0 0 1];
        Y(i*3-2:i*3) = (1/sqrt(xi(i)^2+yi(i)^2+zi(i)^2))*[xi(i);yi(i);zi(i)];
    end

    p = M\Y;    % do the least squares for A and B elements
    Akplus = [p(1) p(2) p(3);p(4) p(5) p(6);p(7) p(8) p(9)];
    Bkplus = [p(10); p(11); p(12)];
    
    xyzplus = (Akplus*[xi';yi';zi'])'; % update the xi,yi,zi tuples
    xi = xyzplus(:,1)+Bkplus(1);
    yi = xyzplus(:,2)+Bkplus(2);
    zi = xyzplus(:,3)+Bkplus(3);
    
    Btilde = Akplus*Btilde + Bkplus;
    Atilde = Akplus*Atilde;
    
    Atracking(k+1,:) = Atilde(:)';
    Btracking(k+1,:) = Btilde(:)';
    
    if plotFlag,
        plot3(xi,yi,zi,'.');
    end
end


if plotFlag,
    hold off
    figure(2), clf
    plot([sqrt(x.^2+y.^2+z.^2) sqrt(xi.^2+yi.^2+zi.^2)],'.');
    legend('Pre-Calibration','Post-Calibration');
    title('Norm of data pre- and post-Calibration');
    
    mmm = mean(sqrt(x.^2+y.^2+z.^2));
    
    figure(3), clf
    plot([Atracking Btracking]/mmm)
    xlabel('Step')
    ylabel('Parameter Value')
    title('Plot of Walk In of Parameters')
    
    figure(4), clf
    histfit(sqrt(x.^2+y.^2+z.^2)), hold on
    histfit(sqrt(xi.^2+yi.^2+zi.^2)), hold off
end


