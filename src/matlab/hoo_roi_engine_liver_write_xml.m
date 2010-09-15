function hoo_roi_engine_liver_write_xml(nth_ROI, series_n)

if class(nth_ROI) == 'char'
    nth_ROI = str2double(nth_ROI);
    series_n = str2double(series_n);
end
    
% Load the Java Path
javaaddpath /home/hshin/workspace/ROI-Engine/src/matlab/javabin/ParseDICOM.jar

% Load my Java class for manipulating the XML files
parseResultManipulator = ParseDICOM.ManipulateDICOMparseResult;


fid = fopen('./dicom_files.txt');
scan_result = textscan(fid, '%s %s');

dicom_files = scan_result{1};
working_directory_tmp = scan_result{2};
working_directory = working_directory_tmp{1};


num_files = size(dicom_files, 1);


for i=1:num_files
    dicom_files_xml_writer_input{1,i,1} = dicom_files{i};
    dicom_file = [working_directory dicom_files{i}];
    dicom_info = dicominfo(dicom_file);
    dicom_files_xml_writer_input{1,i,2} = dicom_info.SOPInstanceUID;
end


dicom_file = [working_directory dicom_files{1}];
im_dicom = dicomread(dicom_file);
dicom_info = dicominfo(dicom_file);

StudyInstanceUID = dicom_info.StudyInstanceUID;
dicom_metadatas{1,1,1} = 'SeriesDescription';
dicom_metadatas{1,1,2} = dicom_info.SeriesDescription;
dicom_metadatas{1,2,1} = 'SeriesInstanceUID';
dicom_metadatas{1,2,2} = dicom_info.SeriesInstanceUID;

parseResultManipulator.writeToXML(working_directory, dicom_files_xml_writer_input, dicom_metadatas, StudyInstanceUID);


fid = fopen('./seed_points.txt');
scan_result = textscan(fid, '%s %s %s');

xs = scan_result{1};
ys = scan_result{2};
zs = scan_result{3};


im_roi = zeros(size(im_dicom,1), size(im_dicom,2), num_files);


fid = fopen(['./ROI_' int2str(nth_ROI-1) '.txt']);
scan_result = textscan(fid, '%s %s %s');
ROI_x = scan_result{1};
ROI_y = scan_result{2};
ROI_z = scan_result{3};



for i=1:length(ROI_x)
    im_roi(str2double(ROI_y(i)), str2double(ROI_x(i)), str2double(ROI_z(i))) = 1;
end
    


boundaries_cell = cell(num_files, 1);


for i=1:num_files

    BW = im2bw(im_roi(:,:,i));
    [B, L] = bwboundaries(BW, 'noholes');
    
    
    for j=1:size(B,1)
        boundaries_cell{i} = vertcat(boundaries_cell{i}, B{j});
    end
    
end



i = 1;
boundaries_cell_array{i} = boundaries_cell;
i = i + 1;
xml_filename = char(['./rpacs_processing/' 'rpacs_processing', strrep(working_directory, '/', '_'), '.xml']);



% To know the size of matrix to pre-allocate
num_max_ROI_lables = size(boundaries_cell_array, 2);
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
            
        end
    end
end

% Pass the 4-dimensional double boundaries array with other infos to XML
% writer
application_name = 'Hoo Matlab-Java ROI Tool';
roi_dimension = 2;
xml_filename_tmp = [xml_filename '.tmp'];
movefile(xml_filename, xml_filename_tmp);
parseResultManipulator.writeToXML(xml_filename_tmp, xml_filename, boundaries_double_array, series_n, application_name, roi_dimension);
delete(xml_filename_tmp);

copyfile(xml_filename, ['../../data/mriw_temp/download/xml/', strrep(working_directory, '/', '_'), '.xml']);

exit;
