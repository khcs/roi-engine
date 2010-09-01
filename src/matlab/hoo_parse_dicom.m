% Parse the directory of DICOM files and show the DICOM Series Descriptions
% Author: Hoo Chang Shin
% Date: 02. Dec. 2010

function [dicom_files, dicom_infos, StudyInstanceUID] = hoo_parse_dicom(working_directory)

disp(' ');
disp('Hoo Matlab DICOM Parser');
disp('ver. 1.0');
disp('Author: Hoo Chang Shin');
disp('E-mail: hoo.shin@icr.ac.uk');
disp(' ');
disp('Parsing...');
disp(' ');


% Test for Java wrapper and XML parser
% Get the whole files of the working directory with the wildcard character
dirOutput = dir(fullfile(working_directory, '*'));
fileNames = {dirOutput.name}';

% Parse the whole files in the directory and sort out the files which are
% not DICOM files.
valid_dicom_files_index = 0;
dicom_series_index = 0;
dicom_files_char = [];
dicom_series_indexer = [];

% Create waitbar
h = waitbar(0, 'Parsing the directory for the DICOM files...');
set(h, 'Name', 'DICOM Parsing Progress');

for i=1:size(fileNames, 1)
    
    waitbar(i/size(fileNames, 1));
    
    try        
        %disp(char(fileNames(i)));
        dicom_info = dicominfo([working_directory char(fileNames(i))]);        
        valid_dicom_files_index = valid_dicom_files_index + 1;
        
        if valid_dicom_files_index == 1
            dicom_info_cache = dicom_info;
            dicom_series_indexer(dicom_series_index) = valid_dicom_files_index;
        end
        
        dicom_files_char(valid_dicom_files_index, :) = char(fileNames(i));
        sopInstanceUID = dicom_info.SOPInstanceUID;
        
        try
            sopInstanceUIDs(valid_dicom_files_index, :) = sopInstanceUID;
        catch exception2
            % Some SOPInstanceUIDs are shorter than the others, then make
            % the lengths equal filling in white spaces
            if size(sopInstanceUIDs,2) < length(sopInstanceUID)
                diff = length(sopInstanceUID) - size(sopInstanceUIDs,2);
                space = [];
                for j=1:diff
                space(j) = ' ';
                end    
            else
                diff = size(sopInstanceUIDs,2) - length(sopInstanceUID);
                space = [];
                for j=1:diff
                    space(j) = ' ';
                end
            end
            sopInstanceUIDs(valid_dicom_files_index, :) = [sopInstanceUID space];
        end
           
        % Give each series of DICOM files with different Series Description
        % different identifier (number)
        if ~strcmp(dicom_info_cache.SeriesDescription, dicom_info.SeriesDescription)                        
            dicom_series_index = dicom_series_index + 1;
            disp([num2str(dicom_series_index) ': ' dicom_info.SeriesDescription]);            
            dicom_info_cache = dicom_info;
            dicom_series_indexer(dicom_series_index) = valid_dicom_files_index;            
            dicom_infos{dicom_series_index} = dicom_info;
%             j=1;
        end
        
    catch exception
        %disp('exception in hoo_parse_dicom.m')
        %disp('Down');
        %disp(exception.message);                                
    end
end
StudyInstanceUID = dicom_info.StudyInstanceUID;
% Close waitbar
close(h);

for i=1:length(dicom_series_indexer)-1
    k=1;
    for j=dicom_series_indexer(i):dicom_series_indexer(i+1)-1
        dicom_filename = char(dicom_files_char(j,:));
        dicom_files{i,k,1} = dicom_filename;
        %dicom_info = dicominfo([working_directory dicom_filename]);
        sopInstanceUID = char(sopInstanceUIDs(j,:));
        dicom_files{i,k,2} = sopInstanceUID;
        k=k+1;
    end
end
i=i+1;
k=1;
for j=dicom_series_indexer(i):length(dicom_files_char)
    dicom_filename = char(dicom_files_char(j,:));
    dicom_files{i,k,1} = dicom_filename;
    %dicom_info = dicominfo([working_directory dicom_filename]);
    sopInstanceUID = char(sopInstanceUIDs(j,:));
    dicom_files{i,k,2} = sopInstanceUID;
    k=k+1;
end


