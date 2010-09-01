function hoo_read_xml_show_roi



xml_file = input('Enter the full path of the XML file to process: ', 's');
if isempty(xml_file)
    xml_file = './rpacs_processing/rpacs_processing_home_hshin_host_hshin_Works_PhD_Dataset_ICR_JamesD_srtf_breast_DICOM_.xml';
end

[directory_location, filenames, roi_coords_x, roi_coords_y] = ...
    hoo_read_xml_return_filenames_roi_coords(xml_file);


for i=1:length(filenames)
   image(:,:,1,i) = imadjust(dicomread(strtrim([directory_location filenames(i,:)])));
   image(:,:,2,i) = image(:,:,1,i);
   image(:,:,3,i) = image(:,:,2,i);
   
   for j=1:length(roi_coords_x(i,:))
       image(roi_coords_x(i,j), roi_coords_y(i,j), 2, i) = 65535;
   end
end

m = ceil(length(filenames)/10);
n = 10;
for i=1:length(filenames)
    subplot(m,n,i);
    imshow(image(:,:,:,i), 'DisplayRange', []);
    
    title(filenames(i,:));
end
truesize;
