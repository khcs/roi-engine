function [im3d_roi, boundaries_cell] = hoo_get_3d_roi(im_rg_seg, im_dicom_3d)

% Get the ROI of the segmented 3D image
im3d_roi = [];
im3d_roi_color = [];
for i=1:size(im_rg_seg, 3)
    try
        im3d_roi(:,:,i) = edge(im_rg_seg(:,:,i), 'sobel');
    catch %exception
        %disp(exception.message);
    end
end

max_value = max(max(max(im_dicom_3d)));

% Make the dicom-image as a color-image
im_dicom_3d_color = [];
for i=1:size(im_rg_seg, 3)
    im_dicom_3d_color(:,:,1,i) = im_dicom_3d(:,:,i)/max_value;
    im_dicom_3d_color(:,:,2,i) = im_dicom_3d(:,:,i)/max_value;
    im_dicom_3d_color(:,:,3,i) = im_dicom_3d(:,:,i)/max_value;    
end


% Show the ROI of the segmented images
num_files = size(im3d_roi, 3);
m = ceil(num_files/10);
n=10;
figure;
set(gcf, 'Name', 'ROI');

boundaries_cell = cell(num_files, 1);

for i=1:num_files

    BW = im2bw(im_rg_seg(:,:,i));
    [B, L] = bwboundaries(BW, 'noholes');
    
    
    for j=1:size(B,1)
        boundaries_cell{i} = vertcat(boundaries_cell{i}, B{j});
    end
    
    im3d_roi(:,:,i) = L;
    im3d_roi_color(:,:,:,i) = label2rgb(L, @jet, [0 0 0]);
    
    im_dicom_3d_color(:,:,:,i) = im_dicom_3d_color(:,:,:,i) + im3d_roi_color(:,:,:,i);
    
    subplot(m, n, i);    
    imshow(im_dicom_3d_color(:,:,:,i), 'DisplayRange', []);
    title(i);
end
truesize;


figure;
set(gcf, 'Name', 'ROIs-2');

for i=1:num_files
    subplot(m,n,i);
    imshow(im3d_roi_color(:,:,:,i));
    
    boundary = boundaries_cell{i};
    if ~isempty(boundary)
        hold on
        plot(boundary(:,2), boundary(:,1), 'w', 'LineWidth', 1);
    end
    
    title(i);
end
truesize;
