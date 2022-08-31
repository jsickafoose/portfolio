function [Error] = CheckOrthonormality(R)
% function [Error] = CheckOrthonormality(R)
%
% Function checks the orthonormality of a matrix passed to it and returns a
% value that is the Frobinius norm of the residual. Smaller numbers
% indicate better orthonormality

Check = R'*R - eye(3);
Error = norm(Check,'fro');