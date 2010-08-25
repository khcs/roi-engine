function [im_rg_seg, im_dicom_3d] = hoo_rg_segment_frontend( dicom_files, working_directory )

% Author: Hoo Chang Shin
% Hoo.Shin@icr.ac.uk
% BSD License
% 8.Jan.10


% This was for the test purpose
%dicom_files = ['05878416'; '05878430'; '05878444'; '05878458'; '05878472'; '05878486'; '05878500'; '05878514'; '05878528'; '05878542'; ...
%                '05878556'; '05878570'; '05878584'; '05878598'; '05878612'; '05878626'; '05878640'; '05878654'; '05878668'; '05878682'; ...
%                '05878696'; '05878710'; '05878724'; '05878738'; '05878752'; '05878766'; '05878780'; '05878794'; '05878808'; '05878822'; ...
%                '05878836'; '05878850'];


% Load the DICOM images and collect it to 3D Array
im_dicom_3d = [];
im_dicom = [];
im_2d = [];
for i=1:size(dicom_files, 1)
    dicom_file = [working_directory dicom_files(i, :)];
    %im_dicom = dicomread(char(dicom_files(i, :)));
    im_dicom = dicomread(dicom_file);
    im_dicom_3d(:,:,i) = im_dicom;
end


% Show the images to user
num_files = size(dicom_files, 1);

m = ceil(num_files/10);
n = 10;

figure;
set(gcf, 'Name', 'DICOM images');
for i=1:num_files
    subplot(m, n, i)
    imshow(im_dicom_3d(:,:,i), 'DisplayRange', [])
    title(i)
end
truesize


seed_points = [];

i=0;
%while(true)

    % Get the user input to select a image to be seeded
    n = input('Enter the Nth image you want to give seed for the region growing segmentation: ');

    figure
    [yi, xi, P] = impixel(im_dicom_3d(:,:,n), []);
    % P is a 1x3 matrix
    for j=1:size(yi,1)
        i = i+1;
        seed_points(:, i) = [xi(j), yi(j), n, i];
    end
    
%    more = input('Do you have any other image you want to seed? (Y/N): ', 's');
    
%    if more == 'N'
%        break
%    end
%end


% Apply bilateral filter
im_bflt_3d = hoo_bfilter2_3d(im_dicom_3d);


im_rg_seg = zeros(size(im_dicom_3d));


% Region growing segmentation
for i=0:size(seed_points,2)-1
    j=1;
    xi = seed_points(j+i*4); j=j+1;
    yi = seed_points(j+i*4); j=j+1;
    n  = seed_points(j+i*4); j=j+1;
    j=j+1;
    
    im_rg_seg = im_rg_seg + hoo_rg_segment_3d(im_bflt_3d, xi, yi, n);
end


% Show the segmented images
% n=10;
% figure;
% set(gcf, 'Name', 'Segmented images');
% for i=1:num_files
%     subplot(m, n, i);
%     imshow(im_rg_seg(:,:,i));
%     title(i)
% end
% truesize

