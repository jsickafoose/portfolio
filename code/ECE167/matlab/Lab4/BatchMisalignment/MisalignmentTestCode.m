%%
% m-file to simulate multivector alignment algorithm
%
% Gabriel H Elkaim - July 2012
%
clc
close all
clear

addnoise = 1;   % change to a one to add noise to measurements
sigman = 0.01;  % sigma relative to unit length vector measurement
plotflag = 1;
verbose = 1;

%% m-file to generate points for misaligned data
n = 4;                            % number of points to generate
rotvec = 2*pi*0.03*(randn(3,1));    % small misalignment (change 0.05 to 1 for large misalignment
Rmis = expm(skew(rotvec));         % misalignment DCM
mi = rand(3,1)-0.5;
mi = mi/norm(mi);
si = rand(3,1)-0.5;
si = si/norm(si);
%si = mi;          % uncomment this line to test mutliple of the same sensors

Mb = []; %main body
Sb = []; %secondary body

for i = 1:n,
    Ri = expm(skew((randn(3,1))*2*pi));
    Mb(:,i) = Ri*mi;
    Sb(:,i) = Ri*si;
end
Mbn = sigman*randn(size(Mb));
Sbn = sigman*randn(size(Sb));
Sbmeas = Rmis*Sb;

%% Plot out points
if plotflag,
    figure(1); clf;
    quiver3(0*Mb(1,:),0*Mb(2,:),0*Mb(3,:),Mb(1,:),Mb(2,:),Mb(3,:),0,'k'); hold on
    axis([-1 1 -1 1 -1 1]);
    quiver3(0*Sb(1,:),0*Sb(2,:),0*Sb(3,:),Sb(1,:),Sb(2,:),Sb(3,:),0,'b');
    quiver3(0*Sbmeas(1,:),0*Sbmeas(2,:),0*Sbmeas(3,:),Sbmeas(1,:),Sbmeas(2,:),Sbmeas(3,:),0,'g--');
    quiver3([0 0],[0 0],[0 0],[mi(1) si(1)],[mi(2) si(2)],[mi(3) si(3)],0,'r');
    v = extractAxis(Rmis);
    quiver3(0,0,0,v(1),v(2),v(3),0,'r:','filled');

    if addnoise,
        Mbb = (Mb+Mbn)';
        Sbb = (Sbmeas + Sbn)';
        plot3(Mbb(:,1),Mbb(:,2),Mbb(:,3),'kv');
        plot3(Sbb(:,1),Sbb(:,2),Sbb(:,3),'gv');
    end
        
    nsteps = 300;
    for alfa = [1/nsteps:1/nsteps:(1-1/nsteps)],
        Sbmis = expm(skew(alfa*rotvec))*Sb;
        plot3(Sbmis(1,:),Sbmis(2,:),Sbmis(3,:),'g.');
    end
   
    axis('equal');
end
%% Call Elkaim Code
[Rge,Pge] = AlignPrimarySecondary(Mb+addnoise*Mbn,Sbmeas+addnoise*Sbn,mi,si,eye(3));
if verbose,
    fprintf('\nMisalignment Results:');
    Rmis-Rge
    norm(Rmis(:)-Rge(:))
    Pbody = (0.01)^2*Pge
end

if(plotflag),
    figure(1)
    v = extractAxis(Rmis);
    quiver3(0,0,0,v(1),v(2),v(3),0,'r','LineWidth',2);
end


