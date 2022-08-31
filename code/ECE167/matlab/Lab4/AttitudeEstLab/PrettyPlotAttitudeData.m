function PrettyPlotAttitudeData(dT,Acc,Mag,wGyro,Eul)
% function PrettyPlotAttitudeData(dT,Acc,Mag,wGyro,Eul)
%
% This is a plotting function that goes through the data and reconstructs
% the data and plots out graphs of relevant data

He = [22770;5329;41510.2]/1000;     % Earth's magnetic field in uT (NED)
Hu = He/norm(He);                   % magnetic field unit vector
Ge = [0;0;1];                       % Earth's gravitational field in g (NED)

npts = length(Eul);
H = zeros(npts,3);
A = zeros(npts,3);

for i = 1:npts,
    R = eul2dcm(Eul(i,:)*pi/180);   % generate a rotation matrix from Euler
    H(i,:) = (R'*Hu)';
    A(i,:) = (R'*Ge)';
end

Tvec = dT*[0:npts-1]';
figure(5), clf;
plot(Tvec,Eul);
legend('yaw, \psi (^\circ)','pitch, \theta (^\circ)','roll, \phi (^\circ)');
xlabel('Time, sec'), ylabel('Angle (^\circ)')
title('Euler angles vs Time for synthetic data (noise free)');

figure(6), clf;
sphere(50),hold on
colormap('gray');
plot3(H(:,1),H(:,2),H(:,3),'r.');
plot3(Mag(:,1),Mag(:,2),Mag(:,3),'m.');
plot3(A(:,1),A(:,2),A(:,3),'b.');
plot3(Acc(:,1),Acc(:,2),Acc(:,3),'c.');
axis('equal'); legend('','Mags (perfect)','Mags + noise','Accels (perfect)','Accels + noise');
title('Noise free projection of body-fixed mags and accels');  

figure(7), clf
plot(Tvec,wGyro);
xlabel('Time, sec'), ylabel('angular rate (counts)')
legend('p (counts)','q (counts)','r (counts)');
title('Raw angular rates (in Counts)');
end

function C=eul2dcm(eul)
%----------------------------------------------------------------
% function C=eul2dcm(eul)
%
%   This functions determines the direction cosine matrix C
%   that transforms a vector in a reference axis system at time k
%   to one the same axis sytem at time k+1.  The input argument to
%   this function is a vector of the Euler angles in the following
%   order: eul = [yaw,pitch,roll]. (i.e., 3-2-1 rotation convention).  
%
%-----------------------------------------------------------------  

ps=eul(1); th=eul(2); ph=eul(3);

C1=[1 0 0; 0 cos(ph) sin(ph); 0 -sin(ph) cos(ph)];
C2=[cos(th) 0 -sin(th); 0 1 0; sin(th) 0 cos(th)];
C3=[cos(ps) sin(ps) 0; -sin(ps) cos(ps) 0; 0 0 1];

C=C1*C2*C3;
end
