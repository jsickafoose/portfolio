function [Rplus] = IntegrateOpenLoop(Rminus, gyros, deltaT)
% function [Rplus] = IntegrateOpenLoop(Rminus, gyros, deltaT)
%
% Function to Integrate the gyros to the attitude DCM
%
% Inputs: Previous attitute DCM (Rminus)
%         Body Fixed Rotation rates ([p;q;r]) in rad/s
%         Time between samples (deltaT) in seconds
%
% Outputs: New DCM (Rplus)
%
% Note: This code implements both a forward integration as well as the
% matrix exponential version of the integration, change the flag in the
% code below to pick between them.

UseMatrixExponential = 0;   % set to zero for forward integration

if (UseMatrixExponential),
    Rplus = Rexp(gyros, deltaT) * Rminus;
else
    Rplus = Rminus - rcross(gyros) * Rminus * deltaT ;
end
