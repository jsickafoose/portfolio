function AnimateAttitude(dT, Eul)
% function AnimateAttitude(dT, Eul)
%
% Animation for visulization of attitude from Euler angle data
% dT is time step (in seconds)
% Eul is [Yaw Pitch Roll] x n points (in degrees)
%
% Function sets up transparent sphere with cardinal X-Y-Z vectors and then
% animates a very crude aircraft through the euler angles seen in the Eul
% vector.

D2R = pi/180;
X = [1 0;-0.5 -0.5;-0.5 -0.5];
Y = [0 0;0.5 0;-0.5 0];
Z = [0 0;0 0;0 -0.75];
XYZ_body = [X(:,1) Y(:,1) Z(:,1)];
XYZ_tail = [X(:,2) Y(:,2) Z(:,2)];

ned2plot = [1 0 0;0 -1 0;0 0 -1];

XYZ_body = (ned2plot*XYZ_body')';
XYZ_tail = (ned2plot*XYZ_tail')';

figure(10), clf
[xx,yy,zz] = sphere(50);
h = surf(xx,yy,zz);
set(h,'LineStyle','none');
hold on
colormap('gray');
alpha(0.1);
axis('equal');
h = gca;
set(h,'XTickLabel',[],'YTickLabel',[],'ZTickLabel',[]);
quiver3(0,0,0,1.5,0,0,'r','filled','LineWidth',2)
quiver3(0,0,0,0,-1.5,0,'g','filled','LineWidth',2)
quiver3(0,0,0,0,0,-1.5,'b','filled','LineWidth',2)
g = patch(XYZ_body(:,1),XYZ_body(:,2),XYZ_body(:,3),'red');
h = patch(XYZ_tail(:,1),XYZ_tail(:,2),XYZ_tail(:,3),'blue');
xlabel('North'), ylabel('East'), zlabel('Down')

    for i=1:length(Eul),
        R = eul2dcm(Eul(i,:)'*D2R);
        XYZ_body = (ned2plot*R*[X(:,1) Y(:,1) Z(:,1)]')';
        XYZ_tail = (ned2plot*R*[X(:,2) Y(:,2) Z(:,2)]')';
        g.XData = XYZ_body(:,1);
        g.YData = XYZ_body(:,2);
        g.ZData = XYZ_body(:,3);
        h.XData = XYZ_tail(:,1);
        h.YData = XYZ_tail(:,2);
        h.ZData = XYZ_tail(:,3);
        drawnow limitrate
        pause(dT);
    end
end
    
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
