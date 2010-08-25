/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ParseDICOM;

import ParseDICOM_Test.ReadDICOMparseResult;
import ParseDICOM_Test.TransformDICOMparseResult;

/**
 *
 * @author hshin
 */
public class MainTesterClass {
    public static void main(String[] a){
        TransformDICOMparseResult transformer = new TransformDICOMparseResult();
        ReadDICOMparseResult reader = new ReadDICOMparseResult();

        String directory_name = "/Users/hshin/Research/3D-ROI/Matlab_Workspace/Code-26.Jan.10/parse_results";
        String tmp_file_name = "parseDICOMresult_tmp.txt";

        transformer.writeToXML(directory_name, tmp_file_name);
    }
}
