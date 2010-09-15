function hoo_roi_engine_liver

% Load the Java Path
javaaddpath /home/hshin/workspace/ROI-Engine/src/matlab/javabin/ParseDICOM.jar

fid = fopen('./dicom_files.txt');
scan_result = textscan(fid, '%s %s');


dicom_files = scan_result{1};
working_directory_tmp = scan_result{2};
working_directory = working_directory_tmp{1};


for i=1:size(dicom_files, 1)    
    dicom_file = [working_directory dicom_files{i}];
    im_dicom = dicomread(dicom_file);
    im_dicom_3d(:,:,i) = im_dicom;
end


num_files = size(dicom_files, 1);
%im_bflt_3d = hoo_bfilter2_3d(im_dicom_3d);


fid = fopen('./seed_points.txt');
scan_result = textscan(fid, '%s %s %s');

xs = scan_result{1};
ys = scan_result{2};
zs = scan_result{3};


for i=1:size(dicom_files, 1)
    im_overlayed_3d_rgb(:,:,1,i) = imadjust(im_dicom_3d(:,:,i));
    im_overlayed_3d_rgb(:,:,2,i) = imadjust(im_dicom_3d(:,:,i));
    im_overlayed_3d_rgb(:,:,3,i) = imadjust(im_dicom_3d(:,:,i));
end


for nth_ROI=1:length(xs)
    fid = fopen(['./ROI_' int2str(nth_ROI-1) '.txt']);
    scan_result = textscan(fid, '%s %s %s');
    ROI_x = scan_result{1};
    ROI_y = scan_result{2};
    ROI_z = scan_result{3};
    
    color_matrix = select_color(nth_ROI);

    for i=1:length(ROI_x)
        im_overlayed_3d_rgb(str2double(ROI_y(i))+1, str2double(ROI_x(i))+1, 1, str2double(ROI_z(i))+1) = color_matrix(1) * 65535;
        im_overlayed_3d_rgb(str2double(ROI_y(i))+1, str2double(ROI_x(i))+1, 2, str2double(ROI_z(i))+1) = color_matrix(2) * 65535;
        im_overlayed_3d_rgb(str2double(ROI_y(i))+1, str2double(ROI_x(i))+1, 3, str2double(ROI_z(i))+1) = color_matrix(3) * 65535;
    end
    
end


for i=1:size(dicom_files, 1)
    imwrite(im2uint8(im_overlayed_3d_rgb(:,:,:,i)), ['../../data/mriw_temp/download/image/', int2str(i), '.bmp'], 'bmp');
end


exit;


% Show the segmented images
% m = ceil(num_files/10);
% n=10;
% figure;
% set(gcf, 'Name', 'Segmented images');
% for i=1:num_files
%     subplot(m, n, i);
%     imshow(im_overlayed_3d_rgb(:,:,:,i));
%     title(i)
% end
% truesize



function color_matrix = select_color(color)

switch color
    case 1
        a = 1;
        b = 0;
        c = 0;
    case 2
        a = 1;
        b = 0.5;
        c = 0;
    case 3
        a = 1;
        b = 1;
        c = 0;
    case 4
        a = 0.3;
        b = 1;
        c = 0.5;
    case 5
        a = 1;
        b = 0;
        c = 0.5;
    case 6
        a = 1;
        b = 0;
        c = 1;
    case 7
        a = 1;
        b = 0.5;
        c = 0.5;
    case 8
        a = 0.5;
        b = 0;
        c = 0;
    case 9
        a = 0.5;
        b = 0.5;
        c = 0;
    case 10
        a = 0.5;
        b = 0.5;
        c = 0.5;
    case 11
        a = 0.5;
        b = 0;
        c = 0.5;
    case 12
        a = 0.5;
        b = 0;
        c = 1;
    case 13
        a = 0.5;
        b = 0.5;
        c = 1;
    case 14
        a = 0.5;
        b = 1;
        c = 0.5;
    case 15
        a = 0.5;
        b = 1;
        c = 1;
    case 16
        a = 0.5;
        b = 1;
        c = 0;
    case 17
        a = 0;
        b = 0.5;
        c = 0;
    case 18
        a = 0;
        b = 1;
        c = 0;
    case 19
        a = 0;
        b = 0.5;
        c = 1;
    case 20
        a = 0;
        b = 0.5;
        c = 0.5;
    case 21
        a = 0;
        b = 0;
        c = 0.5
    case 22
        a = 0.2
        b = 0.3;
        c = 0.5;
    case 23
        a = 0;
        b = 1;
        c = 0.5;
    case 24
        a = 0;
        b = 1;
        c = 1;
    case 25
        a = 0;
        b = 0;
        c = 1;
end

color_matrix = [a, b, c];
