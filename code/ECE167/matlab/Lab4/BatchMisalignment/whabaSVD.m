function [R_est, Pbody] = whabaSVD(B_v,E_v,w)
% function R_est = whabaSVD(B_v,E_v,w)
%
% computes the optimal rotation matrix to minimize the cost function of
% J = 1/2 * Sum (w_i * |E_v - R*B_v|^2)
% using the SVD decomposition
%
% w is the 1xn weight vector.
% B_v and E_v are 3xn matrices that pack the vector readings
% B_v and E_v must be normalized
%
% if the function is called with only two arguments, w is equally weighted
% such that sum(w) = 1.
%
if (nargin < 3),
    [n,m] = size(B_v);
    w = ones(m,1)/m;
end

[m,n]=size(B_v);
if (m ~=3), error('B_v needs to be 3xn matrix of vector measurements'); end
[j,k]=size(E_v);
if (j ~=3), error('E_v needs to be 3xn matrix of vector measurements'); end
if (n ~= k), error('B_v and E_v need to have the same number of columns'); end

W = [w';w';w'];
B = (B_v.*W)*E_v';
[U,S,V]=svd(B);
R_est = (U*diag([1 1 det(U)*det(V)])*V')';

if (nargout == 2),
    d = det(U)*det(V);
    s1 = S(1,1);
    s2 = S(2,2);
    s3 = S(3,3);
    Pz = diag([(1-s1)/(s2-d*s3)^2 (1-s2)/(s1+d*s3)^2 (1-s3)/(s1+s2)^2]);
    Pbody = V*Pz*V';
end


