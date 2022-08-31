function R_exp = Rexp(w, deltaT)
% function R_exp = Rexp(w, deltaT)
%
% returns the exponential Rodrigues parameter form of the integration that
% keeps R on SO(3). See Park and Chung paper. Requires a time step and the Rotation
% rate (omega).
%
wnorm = norm(w);
wx = rcross([w(1); w(2); w(3)]);
if wnorm < 0.2, % just plucked this one out of the air, need a better number here
   sincW = deltaT - (deltaT^3 * wnorm^2)/6.0 + (deltaT^5 * wnorm^4)/120.0;
   oneMinusCosW = (deltaT^2)/2.0 - (deltaT^4 * wnorm^2)/24.0 + (deltaT^6 * wnorm^4)/720.0;
else
   sincW = sin(wnorm * deltaT)/ wnorm;
   oneMinusCosW = (1.0 - cos(wnorm * deltaT)) / wnorm^2;
end
R_exp = [1 0 0;0 1 0;0 0 1] - sincW * wx + oneMinusCosW * wx * wx;