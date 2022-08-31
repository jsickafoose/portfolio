function R = DCMfromTrial(mags, accels, magInertial, accelInertial)
% function R = DCMfromTrial(mags, accels, magInertial, accelInertial)
%
% Implements a solution to Wahba's problem based in the TRIAD algorithm to
% give you an estimate of the DCM from two non-collinear vector
% measurements
%
% Inputs: magnetic field vector in body coordinates (mags)
%         gravity vector in body coordinated (accels)
%         Inertial magnetic reference vector (magInertial)
%         Inertial gravity reference vector (accelInertial)
%
% Outputs: DCM estimate

accels = accels/norm(accels);                       % set mags and accels to unit vectors
mags = mags/norm(mags);

magInertial = magInertial/norm(magInertial);        % set inertial reference vectors to unit vectors
accelInertial = accelInertial/norm(accelInertial);

m = rcross(mags)*accels;
m = m/norm(m);

M = rcross(magInertial) * accelInertial;
M = M/norm(M);

A = [magInertial M rcross(magInertial)*M]*[mags m rcross(mags)*m]';
R = A';

