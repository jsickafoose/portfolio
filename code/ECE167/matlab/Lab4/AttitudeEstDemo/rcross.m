function rx = rcross(r)
% function rx = rcross(r)
% forms the skew symmetric x-product matrix of a 3x1 vector
rx=[0    -r(3)  r(2);
    r(3)  0    -r(1);
   -r(2)  r(1)  0];
end