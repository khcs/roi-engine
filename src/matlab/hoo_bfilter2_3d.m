function I_bflt_3d = hoo_bfilter2_3d(I)

% 3D Bilateral Filter
% Author: Hoo Chang Shin
% Hoo.Shin@icr.ac.uk
% BSD License
%
% Modified bfilter2.m of R. Lanman
% (http://www.mathworks.com/matlabcentral/fileexchange/12191)
% for 3D image.


% Set bilateral filter parameters
w = 5;  % bilateral filter half-width
sigma = [3 0.1];    % bilateral filter standard deviations


% Create waitbar
h = waitbar(0, 'Applying bilateral filter to 3D image...');
set(h, 'Name', 'Bilateral Filter Progress');

for i=1:size(I, 3)
    % Images must be double precision in the interval [0,1]    
    im_double = double(I(:,:,i)/4095);
    
    % Introduce AWGN into image
    % Note: This will show the benefit of bilateral filtering
    im_double = im_double + 0.03*randn(size(im_double));
    im_double(im_double<0) = 0; im_double(im_double>1) = 1;
    
    % Apply bilateral filter to each image
    im_bflt = bfilter2(im_double, w, sigma);
    
    I_bflt_3d(:,:,i) = im_bflt;
    waitbar(i/size(I,3));
end

% Close waitbar
close(h);