/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ParseDICOM;

import javax.xml.namespace.QName;
import javax.xml.stream.*;
import javax.xml.stream.events.*;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Iterator;

/**
 *
 * @author hshin
 */
public class ManipulateDICOMparseResult {
	
	// Read the all filenames of the XML file
	// (read the result of parsing)
	// and show it to StdOut with the series identifier number
	public void readFromXML(String filename) 
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int i=1;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("series")){
					QName seriesQName = new QName("SeriesDescription");
					System.out.println(Integer.toString(i) + ": " + start.getAttributeByName(seriesQName).getValue());
					i++;
				}				
			}
		}
		reader.close();
	}
	
	// Read the filenames of the series_n
	// and return the filenames string array to Matlab
	public String[] readFromXML(String filename, int series_n)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int i=1;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("series")){					
					if (i == series_n){
						while(reader.hasNext()){
							event = reader.nextEvent();
							if(event.isStartElement()){
								StartElement files_start = event.asStartElement();
								if(files_start.getName().getLocalPart().equals("files")){
									QName filesQName = new QName("num_files");
									int num_files = Integer.parseInt( files_start.getAttributeByName(filesQName).getValue() );
									String filenames[] = new String[num_files];
									int j = 0;
									while(reader.hasNext()){
										event = reader.nextEvent();
										if(event.isStartElement()){											
											StartElement file_start = event.asStartElement();
											if (file_start.getName().getLocalPart().equals("file")){
												QName fileQName = new QName("filename");
												//System.out.println(file_start.getAttributeByName(fileQName).getValue());
												filenames[j] = file_start.getAttributeByName(fileQName).getValue();
												j++;
											}
											if(j>=num_files){
												reader.close();
												return filenames;
											}
										}										
									}									
								}
							}
						}
					}
					i++;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Write the ROI info to the XML file
	public void writeToXML(String in_xml_filename, String out_xml_filename, double boundaries_array[][][][], int series_n, String application_name, int roi_dimension) 
	throws XMLStreamException, IOException{
		
		// Name of the original XML file was given changed as .tmp file
		// and it will be written again with original name with the additional ROI info
		
		XMLInputFactory xmlif = XMLInputFactory.newInstance();
		XMLEventReader reader = xmlif.createXMLEventReader(in_xml_filename, new FileInputStream(in_xml_filename));
		
		XMLOutputFactory xmlof = XMLOutputFactory.newInstance();
		XMLStreamWriter xmlw = xmlof.createXMLStreamWriter(new FileWriter(out_xml_filename));
				
		boolean in_roi_element = false;
		boolean in_roi_2d_element = false;
		int file_element_counter = 0;
		
		int series_counter=1;
		while(reader.hasNext()){
			XMLEvent readerEvent = reader.nextEvent();
			if(readerEvent.isStartDocument()){
				xmlw.writeStartDocument("UTF-8", "1.0");
				xmlw.writeComment("xml-stylesheet entry omitted for debgging purpose.");
			}else if(readerEvent.isStartElement()){
				StartElement start = readerEvent.asStartElement();
				
				// Is the event now in ... element?
				in_roi_element = false;
				in_roi_2d_element = false;
				
				// String to store the value of the roi_dimensions attribute
				String roi_dimensions = "";
				
				// Starting element of the document -> just write it with default namespace
				if (start.getName().getLocalPart().equals("rpacs_processing")){
					xmlw.writeStartElement(start.getName().getLocalPart());	
					xmlw.writeDefaultNamespace(start.getName().getNamespaceURI());
					
				// Series element -> write the element and attributes
				}else if(start.getName().getLocalPart().equals("series")){
					file_element_counter = 0;
					
					// Write the element and attributes
					xmlw.writeStartElement(start.getName().getLocalPart());	
					for(Iterator attr_i = start.getAttributes(); attr_i.hasNext(); ){
						Attribute attr = (Attribute) attr_i.next();
						xmlw.writeAttribute(attr.getName().getLocalPart(), attr.getValue());
					}
					
					// When it's the series of user's choice
					if(series_counter == series_n){														
						
						// Write the roi_info in the series element to the XML file
						xmlw.writeStartElement("roi_info");
						
						// Get creation time and date
						Calendar cal = Calendar.getInstance();
						String DATE_FORMAT_NOW = "yyyy-MM-dd HH:mm:ss";
						SimpleDateFormat sdf = new SimpleDateFormat(DATE_FORMAT_NOW);
						
						// Write creation time and date, creator application name, UserID of creator
						xmlw.writeAttribute("creation_date", sdf.format(cal.getTime()));						
						xmlw.writeAttribute("creator_app", application_name);						
						xmlw.writeAttribute("creator_id", System.getProperty("user.name"));
						
						// See if there's already information stored about ROI of another dimension
						// write it again with the new ROI dimension info
						if (!roi_dimensions.isEmpty()){
							if (roi_dimensions.equals(roi_dimension))
								xmlw.writeAttribute("roi_dimensions", roi_dimensions);
							else if(roi_dimensions.contains(Integer.toString(roi_dimension)))
								xmlw.writeAttribute("roi_dimensions", roi_dimensions);
							else
								xmlw.writeAttribute("roi_dimensions", Integer.toString(roi_dimension));							
						}else
							xmlw.writeAttribute("roi_dimensions", Integer.toString(roi_dimension));
						
						xmlw.writeEndElement();
						
						//series_counter++;
						//continue;
					}
					series_counter++;
					
				// To skip writing the roi_info element again, set the in_roi_element to true.
				// And read out the value of the roi_dimensions attribute
				}else if(start.getName().getLocalPart().equals("roi_info") && series_n+1 == series_counter){
					in_roi_element = true;
					
					for(Iterator roi_attr_i = start.getAttributes(); roi_attr_i.hasNext(); ){
						Attribute roi_attr = (Attribute) roi_attr_i.next();
						if(roi_attr.getName().getLocalPart().equals("roi_dimensions")){
							roi_dimensions = roi_attr.getValue();								
						}
					}
					
				// To skip writing the roi_2d element again, set the in_roi_2d_element to true.
				// And write the EndElement for the file element.
				}else if(start.getName().getLocalPart().equals("roi_2d") && series_n+1 == series_counter){
					in_roi_2d_element = true;
					xmlw.writeEndElement();
					
				// In the file element.
				}else if(start.getName().getLocalPart().equals("file") && series_n+1 == series_counter){					
					xmlw.writeStartElement(start.getName().getLocalPart());					
					for(Iterator attr_i = start.getAttributes(); attr_i.hasNext(); ){
						Attribute attr = (Attribute) attr_i.next();
						xmlw.writeAttribute(attr.getName().getLocalPart(), attr.getValue());
					}					
					
					// Write the roi_2d element in the file element.
					// As many as the number of labels of the ROI.
					for(int i=0; i<boundaries_array.length; i++){
						xmlw.writeStartElement("roi_2d");
						xmlw.writeAttribute("label", Integer.toString(i));
						
						// Write the coordinates of the ROI as character element
						for(int j=0; j<boundaries_array[i][file_element_counter].length; j++){
							String roi_coord;
							roi_coord = "(" + Double.toString(boundaries_array[i][file_element_counter][j][0]) + "," + Double.toString(boundaries_array[i][file_element_counter][j][1]) + ")";
							if(boundaries_array[i][file_element_counter][j][0] != 0 && boundaries_array[i][file_element_counter][j][1] != 0)							
								xmlw.writeCharacters(roi_coord);	
							xmlw.writeCharacters(" ");
						}
						
						xmlw.writeEndElement();
					}					
					
					file_element_counter++;
				}
				
				// Any other elements
				else{
					xmlw.writeStartElement(start.getName().getLocalPart());	
					
					for(Iterator attr_i = start.getAttributes(); attr_i.hasNext(); ){
						Attribute attr = (Attribute) attr_i.next();
						xmlw.writeAttribute(attr.getName().getLocalPart(), attr.getValue());
					}
				}
				
			}else if(readerEvent.isEndElement()){
				// Write EndElement skipping those elements
				if(series_n+1 == series_counter && in_roi_element){					
				}else if(series_n+1 == series_counter && in_roi_2d_element){
				}else{
					xmlw.writeEndElement();
				}
			}else if(readerEvent.isEndDocument()){
				xmlw.writeEndDocument();
			}
		}
		
		reader.close();
		xmlw.close();
		
		/*
		System.out.println("num_labels: " + Integer.toString( boundaries_array.length ));
		for(int i=0; i<boundaries_array.length; i++){
			System.out.println("label: " + Integer.toString(i+1) + " num_files: " + Integer.toString(boundaries_array[i].length));
			for(int j=0; j<boundaries_array[i].length; j++){
				System.out.println("file_num: " + j + " " + Integer.toString(boundaries_array[i][j].length));
				for(int k=0; k<boundaries_array[i][j].length; k++){
					System.out.println(boundaries_array[i][j][k][0] + " " + boundaries_array[i][j][k][1]);
				}
			}
		}
		*/
	}
	
	// Write the result of parsing to XML file
    public void writeToXML(String working_directory,
            String dicom_files[][][], String dicom_metadata[][][], String studyInstanceUID)
    throws XMLStreamException, IOException{

    	// On Mac, replace the '/' character in directory structure to '_' character
    	// and have the directory name as part of the XML filename
        String working_directory_fname = working_directory.replaceAll("/", "_");
        String XMLFileName = "rpacs_processing/rpacs_processing" + working_directory_fname + ".xml";

        // Default namespace
        String Namespace = "http://domain.com/ResearchPACS";

        // Create an output factory
        XMLOutputFactory xmlof = XMLOutputFactory.newInstance();

        // Create an XML stream writer
        XMLStreamWriter xmlw = xmlof.createXMLStreamWriter(new FileWriter(XMLFileName));

        xmlw.writeStartDocument("UTF-8", "1.0");
        //xmlw.writeProcessingInstruction("xml-stylesheet href='ResearchPACS-DICOM-ParseResult.xsl' type='text/xsl'");
        xmlw.writeComment("xml-stylesheet entry omitted for debugging purpose.");

        // This document starts with this element
        xmlw.writeStartElement("rpacs_processing");
        xmlw.writeDefaultNamespace(Namespace);

        xmlw.writeStartElement("study");
        xmlw.writeAttribute("StudyInstanceUID", studyInstanceUID);

        xmlw.writeAttribute("directory_location", working_directory);

        for(int i=0; i<dicom_metadata.length; i++){
            xmlw.writeStartElement("series");
            
            for(int j=0; j<dicom_metadata[i].length; j++){
                xmlw.writeAttribute(dicom_metadata[i][j][0], dicom_metadata[i][j][1]);                              
            }
            
            int num_files = 0;
            xmlw.writeStartElement("files");
            for(int k=0; k<dicom_files[i].length; k++){
            	if(dicom_files[i][k][0] != null){
            		++num_files;
            	}
            }
            
            xmlw.writeAttribute("num_files", Integer.toString(num_files));
            for(int k=0; k<dicom_files[i].length; k++){                
                if(dicom_files[i][k][0] != null){
                    xmlw.writeStartElement("file");

                    xmlw.writeAttribute("filename", dicom_files[i][k][0]);
                    xmlw.writeAttribute("SOPInstanceUID", dicom_files[i][k][1]);
                    
                    xmlw.writeEndElement();
                }                
            }            
            xmlw.writeEndElement();
            
            //System.out.println();
            xmlw.writeEndElement();
        }

        xmlw.writeEndElement();
        xmlw.writeEndElement();
        xmlw.writeEndDocument();
        xmlw.close();
        
    }
}
