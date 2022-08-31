function v_x = skew (v)
%v_x = skew (v)
%
%Obtem a matriz skew-simmetric correspondente ao produto
%externo a partir de v
%Recebe: v - vector (3x1)
%Devolve: v_x=[0     -v(3)     v(2);
%              v(3)    0      -v(1);
%             -v(2)   v(1)       0];

v_x=[0     -v(3)     v(2);
     v(3)    0      -v(1);
    -v(2)   v(1)       0];