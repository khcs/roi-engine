function dicom_metadatas = hoo_extract_metadata(dicom_infos)

%length(dicom_infos)

for i=1:length(dicom_infos)
    
    dicom_metadatas{i,1,1} = 'SeriesDescription';
    dicom_metadatas{i,1,2} = dicom_infos{i}.SeriesDescription;
    
    %dicom_metadatas{i,2,1} = 'StudyInstanceUID';
    %dicom_metadatas{i,2,2} = dicom_infos{i}.StudyInstanceUID;
    
    dicom_metadatas{i,2,1} = 'SeriesInstanceUID';
    dicom_metadatas{i,2,2} = dicom_infos{i}.SeriesInstanceUID;
    
    %dicom_metadatas{i,4,1} = 'SOPInstanceUID';
    %dicom_metadatas{i,4,2} = dicom_infos{i}.SOPInstanceUID;
end


%xmlManipulator.writeToXML('metadata', dicom_infos);

