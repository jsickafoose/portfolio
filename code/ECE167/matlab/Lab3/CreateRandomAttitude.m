function R = CreateRandomAttitude()
% function R = CreateRandomAttitude()
% 
% Function returns a randomly generated direction cosine matrix through the
% use of a matrix exponential integration of a randomly generated rotation

wdT = (rand(3,1)-0.5)*2*pi;
R = Rexp(wdT);

    function R_exp = Rexp(w)
    % function R_exp = Rexp(w)
    %
    % returns the exponential Rodrigues parameter form of the integration that
    % keeps R on SO(3). See Park and Chung paper.
    %
    wnorm = norm(w);
    rx = rcross(w);
    s = 2*sin(wnorm/2)/wnorm;
    c = cos(wnorm/2);
    R_exp = [1 0 0;0 1 0;0 0 1] + s*c*rx + s*s/2*rx*rx;
    end

    function rx = rcross(r)
        % function rx = rcross(r)
        % forms the skew symmetric x-product matrix of a 3x1 vector
        rx=[0    -r(3)  r(2);
            r(3)  0    -r(1);
            -r(2)  r(1)  0];
    end
end