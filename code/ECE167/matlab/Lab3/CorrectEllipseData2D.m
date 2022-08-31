function [Xcorr,Ycorr] = CorrectEllipseData2D(Xmeas,Ymeas,Atilde,Btilde)
% function [Xcorr,Ycorr] = CorrectEllipseData2D(Xmeas,Ymeas,Atilde,Btilde)
%
% This function applies a correction to Ellipse 2D data given that you have
% already calibrated the sensor/environment.
%
% Atilde and Btilde come from the CalibrateEllipseData2D function
%
Xcorr = [];
Ycorr = [];

for i = 1:length(Xmeas),
    xy = Atilde*[Xmeas(i);Ymeas(i)] + Btilde;
    Xcorr(i) = xy(1);
    Ycorr(i) = xy(2);
end

