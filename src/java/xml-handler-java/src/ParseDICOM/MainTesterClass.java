/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ParseDICOM;

import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

import javax.xml.stream.XMLStreamException;

import ParseDICOM_Test.ReadDICOMparseResult;
import ParseDICOM_Test.TransformDICOMparseResult;

/**
 *
 * @author hshin
 */
public class MainTesterClass {
    public static void main(String[] a) throws XMLStreamException, IOException{
/*    	
        TransformDICOMparseResult transformer = new TransformDICOMparseResult();
        ReadDICOMparseResult reader = new ReadDICOMparseResult();

        String directory_name = "/Users/hshin/Research/3D-ROI/Matlab_Workspace/Code-26.Jan.10/parse_results";
        String tmp_file_name = "parseDICOMresult_tmp.txt";

        transformer.writeToXML(directory_name, tmp_file_name);
*/
    	
    	
/*    	
  		String rfilename = ManipulateDICOMparseResult.readFromMriwXML_referenceFilename("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/cosine_results.xml");
    	System.out.println(rfilename);
    	
    	String[] dfilenames = ManipulateDICOMparseResult.readFromMriwXML_dynamicFilenames("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/cosine_results.xml");
    	for(int i=0; i<dfilenames.length; i++){
    		System.out.println(dfilenames[i]);
    	}
    	
    	String[] creationinfo = ManipulateDICOMparseResult.readFromMriwXML_ROIcreationInfo("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/cosine_results.xml");
    	for(int i=0; i<creationinfo.length; i++){
    		System.out.println(creationinfo[i]);
    	}
    	
    	int num_data_record = ManipulateDICOMparseResult.readFromMriwXML_getNumDataRecord("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/cosine_results.xml");
    	System.out.println(num_data_record);

    	int[] xs = ManipulateDICOMparseResult.readFromMriwXML_ROIcoordinates_x("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/cosine_results.xml");
    	int[] ys = ManipulateDICOMparseResult.readFromMriwXML_ROIcoordinates_y("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/cosine_results.xml");
    	for(int i=0; i<xs.length; i++){
    		System.out.println(xs[i] +", " + ys[i]);
    	}
*/    	
		//FileWriter outFile = new FileWriter("roi_coords.txt");
		//PrintWriter out = new PrintWriter(outFile);
    	
    	//String[] roi_2d_coordinates = ManipulateDICOMparseResult.readFromXML_roi_coordinates("/home/hshin/workspace/ROI-Engine/src/matlab/rpacs_processing/rpacs_processing_home_hshin_host_hshin_Works_PhD_Dataset_ICR_JamesD_srtf_breast_DICOM_.xml", 1);
    	//System.out.println(roi_2d_coordinates.length);    	
    	//for (int i=0; i<roi_2d_coordinates.length; i++){
    	//	//System.out.println(roi_2d_coordinates[i]);
    	//	System.out.println(roi_2d_coordinates[i]);
    	//}
    	//out.close();
    	
    	//String d_location = ManipulateDICOMparseResult.readFromXML_directory_location("/home/hshin/workspace/ROI-Engine/src/matlab/rpacs_processing/rpacs_processing_home_hshin_host_hshin_Works_PhD_Dataset_ICR_JamesD_srtf_breast_DICOM_.xml", 1);
    	//System.out.println(d_location);
    	
    	//String[] image_size = ManipulateDICOMparseResult.readFromMriwXML_getImageSize("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/cosine_results.xml");
    	//for(int i=0; i<image_size.length; i++){
    	//	System.out.println(image_size[i]);
    	//}
    	
    	String[] roi_coord_x_array = ManipulateDICOMparseResult.readFromMriwXML_ROIcoordinatesForMRIW_x("/home/hshin/workspace/ROI-Engine/src/java/xml-handler-java/test_data/csv_cosine_results.xml"); 
    	//System.out.println(roi_coord_x_csv);
    	for(int i=0; i<roi_coord_x_array.length; i++){
    		System.out.print(roi_coord_x_array[i] + " ");    		
    	}
    }
}
