% m-file to estimate attitude (full closed loop) given synthetic data.
%
%
dT = (1/50);                        % 50Hz update rate


% Kp_a=1;
% Ki_a=Kp_a/5;
% 
% Kp_m=1;
% Ki_m=Kp_m/5;

[Acc,Mag,wGyro,Eul] = CreateTrajectoryData(dT,true);

npts = length(Eul);
Tvec = dT*[0:npts-1]';

He = [22770;5329;41510.2]/1000;     % Earth's magnetic field in uT (NED)
Hu = He/norm(He);                   % magnetic field unit vector
Ge = [0;0;1];                       % Earth's gravitational field in g (NED)

D2R = pi/180;
Ro = eul2dcm(Eul(1,:)*D2R);         % initial attitude from Euler
Ro = eye(3);                        % set to pointing north, wings level
Bhat = zeros(3,1);                  % gyro biases

GscaleFactor = (1/250)*(2^15-1);    % conversion from deg/s to counts
Eul_hat = zeros(npts,3);
Bhat_vec = zeros(npts,3);
R = Ro;

for i=1:npts,
    [Rplus,Bplus] = IntegrateClosedLoop(R,Bhat, (1/GscaleFactor)*wGyro(i,:)'*D2R, Mag(i,:)', Acc(i,:)', He, Ge, dT);
    Eul_hat(i,:) = [atan2(R(1,2),R(1,1)) ...
                   -asin(R(1,3)) ...
                    atan2(R(2,3),R(3,3))]*180/pi;   % yaw pitch roll (deg)
    Bhat_vec(i,:) = Bhat';
    R = Rplus;
    Bhat = Bplus;
end



figure(1), clf
plot(Tvec,Eul,'-',Tvec,Eul_hat,'--')
xlabel('Time [s]'), ylabel('Euler Angles [deg]')
legend('\psi_{true}','\theta_{true}','\phi_{true}','\psi_{est}','\theta_{est}','\phi_{est}');
title('Euler Angles (true) and Estimated in [deg]');

cvg = find(Tvec > 15);
Yaw_error = Eul(cvg,1)-Eul_hat(cvg,1);
idx = find(abs(Yaw_error) < 340);
Yaw_error = Yaw_error(idx);
Tyaw = Tvec(cvg);
Tyaw = Tyaw(idx);
Pitch_error = Eul(cvg,2)-Eul_hat(cvg,2);
idx = find(abs(Pitch_error) < 340);
Pitch_error = Pitch_error(idx);
Tpitch = Tvec(cvg);
Tpitch = Tpitch(idx);
Roll_error = Eul(cvg,3)-Eul_hat(cvg,3);
idx = find(abs(Roll_error) < 340);
Roll_error = Roll_error(idx);
Troll = Tvec(cvg);
Troll = Troll(idx);
    figure(2), clf
    subplot(311), plot(Tyaw,Yaw_error,'b');
    ax=axis; hold on
    plot(Tvec(1:cvg-1),Eul(1:cvg-1,1)-Eul_hat(1:cvg-1,1),'r');
    axis([0 ax(2:4)]);
    ylabel('\psi error ^\circ')
    title('Errors between Estimated and True Euler Angles');
    
    subplot(312), plot(Tpitch,Pitch_error,'b');
    ax=axis; hold on
    plot(Tvec(1:cvg-1),Eul(1:cvg-1,2)-Eul_hat(1:cvg-1,2),'r');
    axis([0 ax(2:4)]);
    ylabel('\theta error ^\circ')
    
    subplot(313), plot(Troll,Roll_error);
    ax=axis; hold on
    plot(Tvec(1:cvg-1),Eul(1:cvg-1,3)-Eul_hat(1:cvg-1,3),'r');
    axis([0 ax(2:4)]);
    ylabel('\phi error ^\circ'), xlabel('Time [sec]')

figure(3), clf
subplot(221), histfit(Pitch_error);
ylabel('Frequency'), title(['Yaw: \mu = ',num2str(mean(Yaw_error)),' \sigma =',num2str(std(Yaw_error)),' [deg]']);
subplot(222), histfit(Pitch_error);
title(['Pitch: \mu = ',num2str(mean(Pitch_error)),' \sigma =',num2str(std(Pitch_error)),' [deg]']);
subplot(223), histfit(Roll_error);
ylabel('Frequency'), xlabel('Error [deg]'), title(['Roll: \mu = ',num2str(mean(Roll_error)),' \sigma =',num2str(std(Roll_error)),' [deg]']);
subplot(224), histfit(Yaw_error); hold on
histfit(Pitch_error);
xlabel('Error [deg]');
histfit(Roll_error);

figure(4), clf
plot(Tvec,Bhat_vec*180/pi);
ylabel('Gyro biases [deg/s]'), xlabel('Time [sec]');
title('Gyro bias estimates vs time');

PrettyPlotAttitudeData(dT,Acc,Mag,wGyro,Eul);

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
