function [Rmis, Pbody] = AlignMasterSlave(Mb,Sbmeas,mi,si,Rmishat_0,i);
% function [Rmis, Pbody] = AlignMasterSlave(Mb,Sbmeas,mi,si,Rmishat_0,i);
%
% function generates the misalignment matrix to bring the slave sensor
% triad into perfect alignment with the the master triad. Solution based on
% Markley's SVD solution to Whaba's problem.
%
% Inputs:
%         Mb - 3xn matrix of body master measurements
%         Sbmeas - 3xn matrix of body slave measurements
%         mi - master unit vector in inertial coordinates
%         si - slave unit vector in inertial coordinates
%         i - optional number of iterations
%
% Outputs:
%         Rmis - misalignment DCM such that Rmis'*Sbmeas = Sb
%
tol = 1e-15;
createPlot = 0;
animatePlot = 0;
verbose = 1;
Delta = [];

mi = mi/norm(mi);
si = si/norm(si);
Mb = colnorm(Mb);
Sbmeas = colnorm(Sbmeas);

Rmishat_old = zeros(3,3);

if (nargin < 5),
    Rmishat = eye(3);
else
    Rmishat = Rmishat_0;
end
%Rmishat = eye(3);
%Rmishat = [0 1 0;-1 0 0;0 0 1];
%Rmishat = [0 0 1;1 0 0;0 1 0];
if (nargin ==6), num2iter = i;
else num2iter = 1000;
end

for iter = 1:num2iter,
    if verbose,
        fprintf('(%g)',iter);
    end
    Sbhat = Rmishat' * Sbmeas;
    Sihat = [];
    [m,n]=size(Mb);
    for i = 1:n,
        Ri = whabaSVD([mi si],[Mb(:,i) Sbhat(:,i)]);
        Sihat(:,i) = Ri*si;
    end
    Rmishat_old = Rmishat;
    Rmishat = whabaSVD(Sihat,Sbmeas);
    if (animatePlot && ((iter < 200)||(rem(iter,5)==0))),
        Sbmis = Rmishat' * Sbmeas;
        v = extractAxis(Rmishat');      
        figure(1);
        plot3(Sbmis(1,:),Sbmis(2,:),Sbmis(3,:),'b.');
        quiver3(0,0,0,-v(1),-v(2),-v(3),0,'c','filled');
    end

    Delta(iter) = norm(Rmishat - Rmishat_old,'fro');
    if (norm(Rmishat - Rmishat_old,'fro') < tol), 
        break; 
    end
    if verbose && (rem(iter,5)==0),
        fprintf(' Delta: %g\n',norm(Rmishat - Rmishat_old,'fro'));
        fprintf('\n\n');
        disp(Rmishat);
    end;
end

Rmis = Rmishat;

if (createPlot),
    figure(2);
    semilogy([1:length(Delta)]',Delta','k+');
    grid on
    title('Frobenius norm of $$\hat{\mathcal{R}^k}_{mis} - \hat{\mathcal{R}^{k-1}}_{mis}$$',...
          'interpreter','latex')
    xlabel('Iterations'), ylabel('log(Norm)');
end

if (nargout == 2),
    [Rmis,Pbody] = whabaSVD(Sihat,Sbmeas);
end
end


function An = colnorm(A);
% function An = colnorm(A)
%
% makes every column in A have a unit norm
[n,m]=size(A);
den = ones(n,1)*sqrt(sum(A.*A,1));
An = A./den;
end