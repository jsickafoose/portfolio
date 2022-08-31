function [Rplus, Bplus] = IntegrateClosedLoop(Rminus, Bminus, gyros, mags, accels, magInertial, accelInertial, deltaT)
% function [Rplus, Bplus] = IntegrateClosedLoop(Rminus, Bminus, gyros, mags, accels, magInertial, accelInertial, deltaT)
%
% Function to implement the full complementary estimate and integration of
% gyros for full attitude estimation using an accelerometer and
% magnetometer feedback.
%
% Inputs: Previous attitute DCM (Rminus)
%         Previous bias estimate (Bminus)
%         Body Fixed Rotation rates ([p;q;r]) in rad/s (gyros)
%         Magnetometer Readings in body coordinates (mags)
%         Accelerometer Readings in body coordinates (accels)
%         Inertial reference magnetic field (magInertial)
%         Inertial reference gravity field (accelInertial)
%         Time between samples (deltaT) in seconds
%
% Outputs: New DCM (Rplus)
%          New Gyro Bias (Bplus)
%
% Note: This code implements a full complementary filter on the DCM using
% the matrix exponential integration of the gyros. Units of the mags and
% accels should match their respective reference inertial vectors. The
% gains are constant and set internally, modify as needed.


Kp_a=10;
Ki_a=Kp_a/10;

Kp_m=10;
Ki_m=Kp_m/10;

accels = accels/norm(accels);                       % set mags and accels to unit vectors
mags = mags/norm(mags);

magInertial = magInertial/norm(magInertial);        % set inertial reference vectors to unit vectors
accelInertial = accelInertial/norm(accelInertial);

gyroInputWithBias = gyros - Bminus;
wmeas_a = rcross(accels)*(Rminus * accelInertial); % accelerometer correction in the body frame
wmeas_m = rcross(mags) * (Rminus * magInertial);   % magnetometer correction in the body frame
    
gyroInputWithFeedback = gyroInputWithBias + Kp_a*wmeas_a + Kp_m*wmeas_m;
bdot=-Ki_a*wmeas_a - Ki_m*wmeas_m;
    
Rplus = Rexp(gyroInputWithFeedback, deltaT) * Rminus;
Bplus = Bminus + bdot*deltaT;

