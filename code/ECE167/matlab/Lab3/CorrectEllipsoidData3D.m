function [Xcorr,Ycorr,Zcorr] = CorrectEllipsoidData3D(Xmeas,Ymeas,Zmeas,Atilde,Btilde)
% function [Xcorr,Ycorr,Zcorr] = CorrectEllipsoidData3D(Xmeas,Ymeas,Zmeas,Atilde,Btilde)
%
% This function applies a correction to Ellipse 3D data given that you have
% already calibrated the sensor/environment.
%
% Atilde and Btilde come from the CalibrateEllipsoidData3D function
%
Xcorr = [];
Ycorr = [];
Zcorr = [];

for i = 1:length(Xmeas),
    xyz = Atilde*[Xmeas(i);Ymeas(i);Zmeas(i)] + Btilde;
    Xcorr(i) = xyz(1);
    Ycorr(i) = xyz(2);
    Zcorr(i) = xyz(3);
end

