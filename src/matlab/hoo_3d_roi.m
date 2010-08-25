function hoo_3d_roi

% Load the Java Path
javaaddpath /Users/hshin/workspace/XML-ROI-Matlab-Java/bin/ParseDICOM/
javaaddpath /Users/hshin/workspace/XML-ROI-Matlab-Java/bin/ParseDICOM/ParseDICOM.jar

% Get the directory containing the DICOM files to work with
working_directory = input('Enter the directory with the DICOM files: ', 's');


% Windows
%working_directory = 'z:\Works\PhD\Dataset\ICR\cvehlow\Liver_Pat3\DICOM\';

% Mac
%working_directory = '/Users/hshin/Works/PhD/Dataset/ICR/cvehlow/Liver_Pat3/DICOM/';


% Load my Java class for manipulating the XML files
parseResultManipulator = ParseDICOM.ManipulateDICOMparseResult;

try
    % Done a processing already? - Yes
    rpacs_files_list = ls('rpacs_processing');
    
    
    % Have you entered the location of the directory to work on?
    if isempty(working_directory)
        % No.
        % Then I guess you're sure that there's a log
        log_fid_r = fopen('./rpacs_processing/rpacs_processing.log');
        tline = fgetl(log_fid_r);
        if ~isempty(strmatch('working_directory', tline))
            working_directory = strtrim(tline(findstr(tline, '=') + 1 : length(tline)));
        end
        fclose(log_fid_r);
        
        % Now we have the location of the working directory         
        % - Read the XML file
        xml_filename = char(['./rpacs_processing/' 'rpacs_processing', strrep(working_directory, '/', '_'), '.xml']);
        parseResultManipulator.readFromXML(xml_filename);%(2:length(xml_filename)));
        
    else
        % Yes.
        xml_fils_list = ls('./rpacs_processing');
        xml_filename = char(['./rpacs_processing/' 'rpacs_processing', strrep(working_directory, '/', '_'), '.xml']);
                
        % Have we already worked on the directory?
        if isempty(xml_files_list, xml_filename)
            % No.
            % - Parse the directory and write the log file.
            [dicom_files, dicom_infos, StudyInstanceUID] = hoo_parse_dicom(working_directory);
            dicom_metadatas = hoo_extract_metadata(dicom_infos);
            
            log_fid_w = fopen('./rpacs_processing/rpacs_processing.log', 'w');
            fprintf(log_fid_w, 'working_directory = %s', working_directory);
            fclose(log_fid_w);
        else
            % Yes.
            % - Read the XML file
            parseResultManipulator.readFromXML(xml_filename);
        end
    end
    
catch exception
    disp(exception.message);
    % No.
    
    % Have you entered the directory location to work on?
    if isempty(working_directory)
        % No.
        % - When No, you should enter the location of the directory to work
        % with!
        error('No record of previous processing found. Please enter the working directory');
    end
    
    % Yes.
    % - Make the directory of log file and .xml files and parse the
    % directory and make the log file.
    mkdir('rpacs_processing');
    log_fid_w = fopen('./rpacs_processing/rpacs_processing.log', 'w');
    fprintf(log_fid_w, 'working_directory = %s', working_directory);
    fclose(log_fid_w);
    
    [dicom_files, dicom_infos, StudyInstanceUID] = hoo_parse_dicom(working_directory);
    dicom_metadatas = hoo_extract_metadata(dicom_infos);
    
    % Write the result of the parsing to the XML file
    parseResultManipulator.writeToXML(working_directory, dicom_files, dicom_metadatas, StudyInstanceUID);
end


% Get the user input to select the DICOM file series
series_n = input('Input the number of the series to work on: ');

% Read the DICOM filenames of the series from the XML file 
dicom_files_java = parseResultManipulator.readFromXML(xml_filename, series_n);

for i=1:length(dicom_files_java)
    dicom_files_interest = char(dicom_files_java);
end


% Loop for segmenting more than 1 region
loop='Y';
i=1;
while loop == 'Y'
    disp('For the labeling issue of the segmented regions, please give one seed at a time!');

    [im_rg_seg, im_dicom_3d] = hoo_rg_segment_frontend(dicom_files_interest, working_directory);

    [im_3d_roi, boundaries_cell] = hoo_get_3d_roi(im_rg_seg, im_dicom_3d);
    
    boundaries_cell_array{i} = boundaries_cell;
    i = i + 1;
    
    loop = input('Want to give more seeds for more ROIs? (Y/N) ', 's');
end

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
application_name = 'Hoo Matlab-Java ROI Tool';
roi_dimension = 2;
xml_filename_tmp = [xml_filename '.tmp'];
movefile(xml_filename, xml_filename_tmp);
parseResultManipulator.writeToXML(xml_filename_tmp, xml_filename, boundaries_double_array, series_n, application_name, roi_dimension);
delete(xml_filename_tmp);


