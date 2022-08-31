function [Acc,Mag,wGyro,Eul] = CreateTrajectoryData(dT,noiseFlag)
% function [Acc,Mag,wGyro,Eul] = CreateTrajectoryData(dT,noiseFlag)
%
% m-file to create trajectory paths that can be used to verify that your
% algorithms are working and that you are recreating good attitude data. Trajctory
% will include noise, and bias on the gyros.
%
% Note that the magnetometer and accelerometer data come out as unit
% vectors (e.g.: post-tumble calibration correction).
%
% Inputs: dT is the timestep of your sensor system (seconds)
%         noiseFlag will add noise to sensors if set to 'true'
%
% Acc is the body fixed accelerometer readings in floats (unit norm)
% Mag is the body fixed magnetometer readings in floats (unit norm)
% wGyro is the body fixed gyro measurements in signed ints
% Eul is the true euler angles (noise free) for each time step (yaw, pitch, roll) [deg]

wdT = (rand(3,1)-0.5)*2*pi;
Ro = Rexp(wdT, 1.0);                     % initial random attitude

AscaleFactor = 0.5*(2^15-1);        % conversion of g's to bits
HscaleFactor = 1/0.15;              % bits/uT
GscaleFactor = (1/250)*(2^15-1);    % bits/(deg/s)

gyrobias = 10*(rand(3,1)-0.5);      % gyrobias (deg/s)
gyronoise = 0.1;                    % degrees/sec RMS
accelnoise = 0.008;                 % accelerometer noise in g's
magnoise = 0.01;                    % magnetomoeter noise in Earth field units

He = [22770;5329;41510.2]/1000;     % Earth's magnetic field in uT (NED)
Hu = He/norm(He);                   % magnetic field unit vector
Ge = [0;0;1];                       % Earth's gravitational field in g (NED)

Tp = 0.5;                           % time of flight for polynomial (sec)
Tc = 3;                             % time of flight for constant (sec)
TotAng = 180;                       % total angle to cover (deg)
MaxRate = TotAng/(Tp+Tc);           % maximum rate in (deg/s)

%
% Generate time vector and body-rate for 180 degree rotation and back
%

TimeVec = [(dT:dT:Tp)'-dT;          % rise time polynomial
           (Tp:dT:Tp+Tc-dT)';       % cruize at constant
           (Tp+Tc:dT:Tp+Tc+Tp)'];   % fall time polynomial
OneSecond = [0:dT:1]';              % 1 second from 0-1 in dT steps
       
xp = (1/Tp)*((dT:dT:Tp)'-dT);
xc = (Tp:dT:Tp+Tc-dT)';
       
wVec = MaxRate*[3*xp.^2 - 2*xp.^3;      % rise time values (deg/s)
                ones(size(xc));         % constant cruise time
             1-(3*xp.^2 - 2*xp.^3);0];  % fall time polynomial
             
wRoundTrip = [zeros(size(OneSecond));   % High Low High rate return to 0
              wVec;
              zeros(size(OneSecond));
             -wVec;
              zeros(size(OneSecond))];
          
%
% Create the trajectory path
%

npts = length(wRoundTrip);
G = [zeros(npts,2) wRoundTrip;                  % r rotation in yaw
     zeros(npts,1) wRoundTrip zeros(npts,1);    % q rotation in pitch
     wRoundTrip zeros(npts,2);                  % p rotation in roll
     wRoundTrip zeros(npts,1) -wRoundTrip;      % p and r together
     zeros(npts,1) -wRoundTrip wRoundTrip;      % q and r together
     -wRoundTrip wRoundTrip zeros(npts,1)];     % p and q together
     
          
npts = length(G);
A = zeros(npts,3);
H = zeros(npts,3);
Eul = zeros(npts,3);

R = Ro;
for i = 1:npts,
    A(i,:) = (R*Ge)';                   % rotate unit norm gravity into body frame
    H(i,:) = (R*Hu)';                   % rotate unit norm magnetic field
    Eul(i,:) = [atan2(R(1,2),R(1,1)) ...
               -asin(R(1,3)) ...
                atan2(R(2,3),R(3,3))]*180/pi;  % yaw pitch roll (deg)
    R = Rexp(G(i,:)*pi/180, dT) * R;       % update rotation matrix
end

%
% Scale to integer units and add bias and noise
%

NoiA = accelnoise*randn(npts,3);    % noise for accelerometer
NoiH = magnoise*randn(npts,3);      % noise for magnetometer
NoiG = gyronoise*randn(npts,3);     % wideband noise on gyros (in deg/s)
BiasG = (ones(3,npts).*gyrobias)';  % gyrobias (in deg/s)

Gnoise = G + NoiG + BiasG;          % corrupted gyro measurements in deg/s
Anoise = A + NoiA;                  % corrupted accelerometer measurements
Hnoise = H + NoiH;                  % corrupted magnetometer measurements

Gnoise = floor(GscaleFactor*Gnoise);% scaled to signed 16bit ints
G = floor(GscaleFactor*G);          % scaled to signed 16bit ints

if noiseFlag,
    Acc = Anoise;
    Mag = Hnoise;
    wGyro = Gnoise;
else,
    Acc = A;
    Mag = H;
    wGyro = G;
end
    



  

              