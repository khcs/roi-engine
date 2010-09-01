function hoo_read_mriw_xml

% Load the Java Path
javaaddpath /home/hshin/workspace/ROI-Engine/src/matlab/javabin/ParseDICOM.jar

inputfile = 'cosine_results.xml';
%data_directory = '/home/hshin/host/hshin/Works/PhD/Dataset/ICR/JamesD/srtf_breast/DICOM/';
data_directory = './testdata/srtf_breast/DICOM/';


% Load my Java class for manipulating the XML files
parseResultManipulator = ParseDICOM.ManipulateDICOMparseResult;

% Get the reference filename
reference_filename_java = parseResultManipulator.readFromMriwXML_referenceFilename(inputfile);
reference_filename = char(reference_filename_java);
%disp(reference_filename)

% Get the dynamic filenames
dynamic_filenames_java  = parseResultManipulator.readFromMriwXML_dynamicFilenames(inputfile);
dynamic_filenames = char(dynamic_filenames_java);
%for i=1:length(dynamic_filenames)
%    disp(dynamic_filenames(i,:))
%end

% Get the SOPInstanceUIDs of the dynamic files
sop_instance_uids_dynamic_files_java = parseResultManipulator.readFromMriwXML_dynamicFilenames_SopInstanceUID(inputfile);
sop_instance_uids_dynamic_files = char(sop_instance_uids_dynamic_files_java);

% Get the SeriesUIDs of the dynamic files
series_uids_dynamic_files_java = parseResultManipulator.readFromMriwXML_dynamicFilenames_SeriesUID(inputfile);
series_uids_dynamic_files = char(sop_instance_uids_dynamic_files_java);

% Get the StudyInstanceUIDs of the dynamic files
study_instance_uid_java = parseResultManipulator.readFromMriwXML_dynamicFilenames_StudyUID(inputfile);
study_instance_uid = char(study_instance_uid_java);

% For the moment, assume that the SereisInstanceUIDs are all same for the
% dynamic files.
SeriesInstanceUID = series_uids_dynamic_files(1,:);
dicom_info = dicominfo(strtrim([data_directory dynamic_filenames(1,:)]));
SeriesDescription = dicom_info.SeriesDescription;
dicom_metadatas{1,1,1} = 'SeriesDescription';
dicom_metadatas{1,1,2} = SeriesDescription;
dicom_metadatas{1,2,1} = 'SeriesInstanceUID';
dicom_metadatas{1,2,2} = SeriesInstanceUID;
StudyInstanceUID = study_instance_uid;
for i=1:length(dynamic_filenames)
    dicom_files{1,i,1} = strtrim(dynamic_filenames(i,:));
    dicom_files{1,i,2} = sop_instance_uids_dynamic_files(i,:);
end

% Get the ROI creation info
roi_creation_info_java = parseResultManipulator.readFromMriwXML_ROIcreationInfo(inputfile);
roi_creation_info = char(roi_creation_info_java);
%1: Time, 2: Program Name, 3: User ID
%for i=1:3
%    disp(roi_creation_info(i,:))
%end

% Get the x & y coordinates of the ROI
xs = parseResultManipulator.readFromMriwXML_ROIcoordinates_x(inputfile);
ys = parseResultManipulator.readFromMriwXML_ROIcoordinates_y(inputfile);
%for i=1:length(xs)
%    disp([int2str(xs(i)) ', ' int2str(ys(i))])
%end





dicom_files_interest = dynamic_filenames;


%[dicom_files, dicom_infos, StudyInstanceUID] = hoo_parse_dicom(data_directory);
%dicom_metadatas = hoo_extract_metadata(dicom_infos);
parseResultManipulator.writeToXML(data_directory, dicom_files, dicom_metadatas, StudyInstanceUID);


reference_image = dicomread([data_directory reference_filename]);
%for i=1:length(xs)
%    reference_image(ys(i), xs(i)) = 2569;
%end
%imshow(reference_image, 'DisplayRange', []);
%imcontrast;


dynamic_images_roi = zeros(size(reference_image,1), size(reference_image,2), length(dynamic_filenames));
dynamic_images = zeros(size(reference_image,1), size(reference_image,2), length(dynamic_filenames));
% mask the DICOM files in ROI with white
for i=1:length(dynamic_filenames)
    dynamic_image = dicomread(strtrim([data_directory dynamic_filenames(i,:)]));
    dynamic_images(:,:,i) = dynamic_image;
    for j=1:length(xs)
        dynamic_image(ys(j), xs(j)) = 2569;
    end
    dynamic_images_roi(:,:,i) = dynamic_image;    
end

dynamic_images_bflt = hoo_bfilter2_3d(dynamic_images_roi);
dynamic_images_segt = zeros(size(dynamic_images));
for i=1:length(dynamic_filenames)
    dynamic_images_segt(:,:,i) = dynamic_images_segt(:,:,i) + ...
                                    regiongrowing(dynamic_images_bflt(:,:,i), ...
                                               xs(ceil(length(xs)/2)), ...
                                               ys(ceil(length(ys)/2)), ...
                                               0.2);
end

m = ceil(length(dynamic_filenames)/10);
n = 10;
figure;
set(gcf, 'name', 'images');
for i=1:length(dynamic_filenames)    
    subplot(m, n, i)
    imshow(dynamic_images(:,:,i), 'DisplayRange', [])
    title(dynamic_filenames(i,:))
end
truesize

dynamic_images_segt = imcomplement(dynamic_images_segt);
[im_3d_roi, boundaries_cell] = hoo_get_3d_roi(dynamic_images_segt, dynamic_images);


i = 1;
boundaries_cell_array{i} = boundaries_cell;
i = i + 1;
xml_filename = char(['./rpacs_processing/' 'rpacs_processing', strrep(data_directory, '/', '_'), '.xml']);




% To know the size of matrix to pre-allocate
num_max_ROI_lables = size(boundaries_cell_array, 2);
num_files = size(dicom_files_interest,1);
num_max_ROI_pixels = 1;
for i=1:num_max_ROI_lables
    boundaries_inner_cell_array = boundaries_cell_array{i};    
    for j=1:num_files        
        if num_max_ROI_pixels < size(boundaries_inner_cell_array{j}, 1)
            num_max_ROI_pixels = size(boundaries_inner_cell_array{j}, 1);
        end
    end
end

% Pre-allocate the boundaries array
boundaries_double_array = zeros(num_max_ROI_lables, num_files, num_max_ROI_pixels, 2);

% Allocate the 4-dimensional boundaries array
for i=1:num_max_ROI_lables
    boundaries_inner_cell_array = boundaries_cell_array{i};
    for j=1:num_files
        boundaries = boundaries_inner_cell_array{j};
        for k=1:size(boundaries, 1)
            boundaries_double_array(i,j,k,:) = boundaries(k,:);
            
            %size(boundaries_inner_cell_array{j})
            %size(boundaries_double_array(i,j,k,:))
            %boundaries_double_array(i,j,k,:) = boundaries_inner_cell_array{j};
        end
    end
end

% Pass the 4-dimensional double boundaries array with other infos to XML
% writer
application_name = roi_creation_info(2,:); % 'Hoo Matlab-Java ROI Tool';
roi_dimension = 2;
xml_filename_tmp = [xml_filename '.tmp'];
movefile(xml_filename, xml_filename_tmp);
series_n = 1;
parseResultManipulator.writeToXML(xml_filename_tmp, xml_filename, ...
                                  boundaries_double_array, series_n, ...
                                  application_name, roi_dimension, ...
                                  roi_creation_info(3,:), ...
                                  roi_creation_info(1,:));
delete(xml_filename_tmp);


