package ParseDICOM;

import java.io.*;
import javax.xml.stream.XMLStreamException;


public class ImportMriwXmlROI {
	public static void main(String[] args) throws XMLStreamException, IOException{
		
		String filename = args[0];
		//String filename = "/Users/hshin/Downloads/mriwresultset_RSNA.xml";
		
		String reference_filename = ManipulateDICOMparseResult.readFromMriwXML_referenceFilename(filename);
		String[] dynamic_filename = ManipulateDICOMparseResult.readFromMriwXML_dynamicFilenames(filename);
		
		String[] sop_instance_uids_dynamic_files = 
					ManipulateDICOMparseResult.readFromMriwXML_dynamicFilenames_SopInstanceUID(filename);
		String[] series_uids_dynamic_files = ManipulateDICOMparseResult.readFromMriwXML_dynamicFilenames_SeriesUID(filename);
		
		String study_instance_uid = ManipulateDICOMparseResult.readFromMriwXML_dynamicFilenames_StudyUID(filename);
		
		String seriesInstanceUID = series_uids_dynamic_files[0];
		
		String seriesDescription = "SeriesDescription_TEMP";
		
		String[][][] dicom_metadatas = new String[1][2][2];
		dicom_metadatas[0][0][0] = "SeriesDescription";
		dicom_metadatas[0][0][1] = seriesDescription;
		dicom_metadatas[0][1][0] = "SeriesInstanceUID";
		dicom_metadatas[0][1][1] = seriesInstanceUID;
		
		String[][][] dicom_files = new String[1][dynamic_filename.length][2];
		
		for(int i=0; i<dynamic_filename.length; i++){
			dicom_files[0][i][0] = dynamic_filename[i];
			dicom_files[0][i][1] = sop_instance_uids_dynamic_files[i];
		}
		
		String[] roi_creation_info = ManipulateDICOMparseResult.readFromMriwXML_ROIcreationInfo(filename);
		String[] xs = ManipulateDICOMparseResult.readFromMriwXML_ROIcoordinatesForMRIW_x(filename);
		String[] ys = ManipulateDICOMparseResult.readFromMriwXML_ROIcoordinatesForMRIW_y(filename);
		

	
		String[] image_size = ManipulateDICOMparseResult.readFromMriwXML_getImageSize(filename);
		
		String working_directory = "containing_directory";			
		ManipulateDICOMparseResult.writeToXML(working_directory, dicom_files, dicom_metadatas, study_instance_uid);
		
		
		String xml_filename = "rpacs_processing/rpacs_processing" + working_directory + ".xml";
		String xml_filename_tmp = xml_filename + ".tmp";
		
		String application_name = roi_creation_info[1];
		int roi_dimension = 2;
		
		Runtime.getRuntime().exec("mv " + xml_filename + " " + xml_filename_tmp);
		Runtime.getRuntime().exec("rm " + xml_filename_tmp);
		
		int series_n = 1;		
		
		ManipulateDICOMparseResult.writeToXML(xml_filename_tmp, xml_filename, xs, ys, series_n, application_name, roi_dimension, roi_creation_info[2], roi_creation_info[0], image_size);
				
	}
}
