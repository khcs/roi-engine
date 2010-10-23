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
	
	
	// Read the ROI coordinates of the series_n
	// and return the filenames string array to Matlab
	public static String[] readFromXML_roi_coordinates(String filename, int series_n)
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
									String filenames_roi_coords[] = new String[num_files];
									int j = 0;
									while(reader.hasNext()){
										event = reader.nextEvent();
										if(event.isStartElement()){											
											StartElement file_start = event.asStartElement();
											if (file_start.getName().getLocalPart().equals("file")){
												while(reader.hasNext()){
													event = reader.nextEvent();
													if(event.isStartElement()){
														StartElement roi_2d_start = event.asStartElement();
														if(roi_2d_start.getName().getLocalPart().equals("roi_2d")){
															QName coordQName = new QName("coordinates");
															filenames_roi_coords[j] = roi_2d_start.getAttributeByName(coordQName).getValue();
															j++;														
/*															while(reader.hasNext()){
																event = reader.nextEvent();
																if(event.isCharacters()){
																	filenames_roi_coords[j] = event.toString();
																	
																	j++;
																	if(j>=num_files){
																		reader.close();
																		return filenames_roi_coords;
																	}
																	//System.out.println(j);
																}
															}*/
														}
														if(j>=num_files){
															reader.close();
															return filenames_roi_coords;
														}
													}
												}												
												//QName fileQName = new QName("filename");
												//System.out.println(file_start.getAttributeByName(fileQName).getValue());
												//filenames[j] = file_start.getAttributeByName(fileQName).getValue();
												//j++;																					
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
	
	// Read the ROI coordinates of the series_n
	// and return the filenames string array to Matlab
	public static String readFromXML_directory_location(String filename, int series_n)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int i=1;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("study")){					
					if (i == series_n){
						QName directory_location_Qname = new QName("directory_location");
						String directory_location = start.getAttributeByName(directory_location_Qname).getValue();
						return directory_location;
					}
					i++;
				}
			}
		}
		reader.close();
		return null;
	}
	
	
	// Read the reference file name in MRIW-XML
	// and return the filenames string array to Matlab
	public static String readFromMriwXML_referenceFilename(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int i = 1;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("reference")){
					while(reader.hasNext()){
						event = reader.nextEvent();
						if(event.isStartElement()){
							StartElement file_start = event.asStartElement();							
							if(file_start.getName().getLocalPart().equals("file")){
								while(reader.hasNext()){									
									QName fileQName = new QName("name");
									String reference_filename = file_start.getAttributeByName(fileQName).getValue();
									return reference_filename;
								}
							}
						}
					}					
				}
			}
		}
		System.out.println("readFromMriwXML_referenceFilename Java Class run - not successful!");
		reader.close();
		return null;
	}
	
	// Read the dynamic filenames in MRIW-XML
	// and return the filenames string array to Matlab
	public static String[] readFromMriwXML_dynamicFilenames(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int num_files = readFromMriwXML_getNumDynamicFilenames(filename);
		int j = 0;
		String filenames[] = new String[num_files];
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("reference")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("dynamic")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if (file_start.getName().getLocalPart().equals("file")){
											QName fileQName = new QName("name");
											//System.out.println(file_start.getAttributeByName(fileQName).getValue());
											filenames[j] = file_start.getAttributeByName(fileQName).getValue();
											j++;
										}											
									}										
								}									
							}								
						}							
					}
					reader.close();					
					return filenames;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Get the number of the dynamic filenames in MRIW-XML
	public static int readFromMriwXML_getNumDynamicFilenames(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int j = 0;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("reference")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("dynamic")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if (file_start.getName().getLocalPart().equals("file")){
											QName fileQName = new QName("name");
											j++;
										}											
									}										
								}									
							}								
						}							
					}
					reader.close();
					return j;					
				}
			}
		}
		reader.close();
		return 0;
	}
	
	// Read the SOPInstanceUID's of the dynamic filenames in MRIW-XML
	// and return the filenames string array to Matlab
	public static String[] readFromMriwXML_dynamicFilenames_SopInstanceUID(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int num_files = readFromMriwXML_getNumDynamicFilenames(filename);
		int j = 0;
		String filenames_sop[] = new String[num_files];
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("reference")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("dynamic")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if (file_start.getName().getLocalPart().equals("file")){
											QName fileQName = new QName("sop-instance-uid");
											//System.out.println(file_start.getAttributeByName(fileQName).getValue());
											filenames_sop[j] = file_start.getAttributeByName(fileQName).getValue();
											j++;
										}											
									}										
								}									
							}								
						}							
					}
					reader.close();					
					return filenames_sop;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Read the SeriesUID's of the dynamic filenames in MRIW-XML
	// and return the filenames string array to Matlab
	public static String[] readFromMriwXML_dynamicFilenames_SeriesUID(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int num_files = readFromMriwXML_getNumDynamicFilenames(filename);
		int j = 0;
		String filenames_series[] = new String[num_files];
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("reference")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("dynamic")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if (file_start.getName().getLocalPart().equals("file")){
											QName fileQName = new QName("series-uid");
											//System.out.println(file_start.getAttributeByName(fileQName).getValue());
											filenames_series[j] = file_start.getAttributeByName(fileQName).getValue();
											j++;
										}											
									}										
								}									
							}								
						}							
					}
					reader.close();					
					return filenames_series;
				}
			}
		}
		reader.close();
		return null;
	}

	
	
	
	// Read the ROI creation info in MRIW-XML
	// and return the filenames string array to Matlab
	public static String[] readFromMriwXML_ROIcreationInfo(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		String creationinfo[] = new String[3];
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("mriw-result-set")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("provenance")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if(file_start.getName().getLocalPart().equals("program")){
											QName fileQName = new QName("name");
											//System.out.println(file_start.getAttributeByName(fileQName).getValue());
											creationinfo[1] = file_start.getAttributeByName(fileQName).getValue();										
										}
										if(file_start.getName().getLocalPart().equals("creation")){
											QName userQName = new QName("user");
											QName timeQName = new QName("time");
											creationinfo[0] = file_start.getAttributeByName(timeQName).getValue();
											creationinfo[2] = file_start.getAttributeByName(userQName).getValue();
										}
									}										
								}									
							}								
						}							
					}
					reader.close();					
					return creationinfo;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Get the number of the data-record in MRIW-XML
	public static int readFromMriwXML_getNumDataRecord(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int j = 0;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("results")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("converter-output")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if (file_start.getName().getLocalPart().equals("data-record")){											
											j++;
										}											
									}										
								}									
							}								
						}							
					}
					reader.close();
					return j;					
				}
			}
		}
		reader.close();
		return 0;
	}
	
	// Get the x coordinates of ROI in MRIW-XML
	// and return the filenames string array to Matlab
	public static int[] readFromMriwXML_ROIcoordinatesForMatlab_x(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int num_x = readFromMriwXML_getNumDataRecord(filename);
		int j = 0;
		int xs[] = new int[num_x];
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("results")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("converter-output")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if (file_start.getName().getLocalPart().equals("data-record")){
											QName fileQName = new QName("x");
											//System.out.println(file_start.getAttributeByName(fileQName).getValue());
											xs[j] = Integer.parseInt(file_start.getAttributeByName(fileQName).getValue());
											j++;
										}											
									}										
								}									
							}								
						}							
					}
					reader.close();					
					return xs;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Get the y coordinates of ROI in MRIW-XML
	// and return the filenames string array to Matlab
	public static int[] readFromMriwXML_ROIcoordinatesForMatlab_y(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int num_y = readFromMriwXML_getNumDataRecord(filename);
		int j = 0;
		int ys[] = new int[num_y];
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("results")){					
					while(reader.hasNext()){
						event = reader.nextEvent();							
						if(event.isStartElement()){
							StartElement files_start = event.asStartElement();
							if(files_start.getName().getLocalPart().equals("converter-output")){								
								while(reader.hasNext()){
									event = reader.nextEvent();
									if(event.isStartElement()){											
										StartElement file_start = event.asStartElement();
										if (file_start.getName().getLocalPart().equals("data-record")){
											QName fileQName = new QName("y");
											//System.out.println(file_start.getAttributeByName(fileQName).getValue());
											ys[j] = Integer.parseInt(file_start.getAttributeByName(fileQName).getValue());
											j++;
										}											
									}										
								}									
							}								
						}							
					}
					reader.close();					
					return ys;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Read the StudyInstanceUID of the dynamic files in MRIW-XML
	// and return the filenames string array to Matlab
	public static String readFromMriwXML_dynamicFilenames_StudyUID(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int i = 1;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("input")){
					while(reader.hasNext()){
						event = reader.nextEvent();
						if(event.isStartElement()){
							StartElement file_start = event.asStartElement();							
							if(file_start.getName().getLocalPart().equals("dynamic")){
								while(reader.hasNext()){									
									QName fileQName = new QName("study-uid");
									String reference_filename = file_start.getAttributeByName(fileQName).getValue();
									return reference_filename;
								}
							}
						}
					}					
				}
			}
		}
		System.out.println("readFromMriwXML_referenceFilename Java Class run - not successful!");
		reader.close();
		return null;
	}
	
	// Read the image size from the MRIW XML file
	// and return the filenames string array to Matlab
	public static String[] readFromMriwXML_getImageSize(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int j = 0;
		String image_size[] = new String[2];
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("roi")){
					QName xSizeQName = new QName("x-size");
					QName ySizeQName = new QName("y-size");
					
					image_size[0] = start.getAttributeByName(xSizeQName).getValue();
					image_size[1] = start.getAttributeByName(ySizeQName).getValue();
										
					reader.close();					
					return image_size;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Read the x coords of ROI from MRIW
	// and return the coords CSV formatted string to Matlab 
	public static String[] readFromMriwXML_ROIcoordinatesForMRIW_x(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int j = 0;
		String coord_x_csv = null;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("roi-x")){		
					event = reader.nextEvent();
					if(event.isCharacters()){
						coord_x_csv = event.toString();
					}
							
					String[] coord_x_array = null;
					if (coord_x_csv != null || !coord_x_csv.equalsIgnoreCase("")){
						coord_x_array = coord_x_csv.split(",");
					}
					
					//return coord_x_csv;
					return coord_x_array;
				}
			}
		}
		reader.close();
		return null;
	}
	
	// Read the x coords of ROI from MRIW
	// and return the coords CSV formatted string to Matlab 
	public static String[] readFromMriwXML_ROIcoordinatesForMRIW_y(String filename)
	throws FileNotFoundException, XMLStreamException{
		XMLInputFactory factory = XMLInputFactory.newInstance();
		XMLEventReader reader = factory.createXMLEventReader(filename, new FileInputStream(filename));
		
		int j = 0;
		String coord_y_csv = null;
		while(reader.hasNext()){
			XMLEvent event = reader.nextEvent();
			if(event.isStartElement()){
				StartElement start = event.asStartElement();
				if(start.getName().getLocalPart().equals("roi-y")){		
					event = reader.nextEvent();
					if(event.isCharacters()){
						coord_y_csv = event.toString();
					}
							
					String[] coord_y_array = null;
					if (coord_y_csv != null || !coord_y_csv.equalsIgnoreCase("")){
						coord_y_array = coord_y_csv.split(",");
					}
					
					//return coord_x_csv;
					return coord_y_array;
				}
			}
		}
		reader.close();
		return null;
	}
	
	
	
	
	
	// Write the ROI info to the XML file
	public static void writeToXML(String in_xml_filename, String out_xml_filename, double boundaries_array[][][][], int series_n, String application_name, int roi_dimension) 
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
						
						String roi_coords = "";
						// Write the coordinates of the ROI as character element
						for(int j=0; j<boundaries_array[i][file_element_counter].length; j++){
							String roi_coord;
							roi_coord = "(" + Double.toString(boundaries_array[i][file_element_counter][j][0]) + "," + Double.toString(boundaries_array[i][file_element_counter][j][1]) + ")";
							if(boundaries_array[i][file_element_counter][j][0] != 0 && boundaries_array[i][file_element_counter][j][1] != 0){							
								//xmlw.writeCharacters(roi_coord);
								roi_coords += roi_coord;
							}
							//xmlw.writeCharacters(" ");
							roi_coords += " ";
						}
						xmlw.writeAttribute("coordinates", roi_coords);
						
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
    public static void writeToXML(String working_directory,
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
    
    
    
    
	// Write the ROI info to the XML file
	public static void writeToXML(String in_xml_filename, String out_xml_filename, double boundaries_array[][][][], int series_n, String application_name, int roi_dimension, String roi_creation_username, String roi_creation_date, String image_size[]) 
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
						xmlw.writeAttribute("creation_date", roi_creation_date);
						xmlw.writeAttribute("creator_app", application_name);						
						xmlw.writeAttribute("creator_id", roi_creation_username);
						
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
						
						
						// For James and MRIW
						for(int i=0; i<boundaries_array.length; i++){
							xmlw.writeStartElement("roi_for_mriw");
							
							xmlw.writeAttribute("x-size", image_size[0]);
							xmlw.writeAttribute("y-size", image_size[1]);
							
							String roi_coords = "";
							// Write the coordinates of the ROI as character element
							for(int j=0; j<boundaries_array[i][file_element_counter].length; j++){
								String roi_coord;
								roi_coord = "(" + Double.toString(boundaries_array[i][file_element_counter][j][1]) + "," + Double.toString(boundaries_array[i][file_element_counter][j][0]) + ")";
								if(boundaries_array[i][file_element_counter][j][1] != 0 && boundaries_array[i][file_element_counter][j][0] != 0){							
									//xmlw.writeCharacters(roi_coord);
									roi_coords += roi_coord;
								}
								//xmlw.writeCharacters(" ");
								roi_coords += " ";
							}
							xmlw.writeAttribute("coordinates", roi_coords);
							
							xmlw.writeEndElement();
						}
						
						
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
						
						String roi_coords = "";
						// Write the coordinates of the ROI as character element
						for(int j=0; j<boundaries_array[i][file_element_counter].length; j++){
							String roi_coord;
							roi_coord = "(" + Double.toString(boundaries_array[i][file_element_counter][j][0]) + "," + Double.toString(boundaries_array[i][file_element_counter][j][1]) + ")";
							if(boundaries_array[i][file_element_counter][j][0] != 0 && boundaries_array[i][file_element_counter][j][1] != 0){							
								//xmlw.writeCharacters(roi_coord);
								roi_coords += roi_coord;
							}
							//xmlw.writeCharacters(" ");
							roi_coords += " ";
						}
						xmlw.writeAttribute("coordinates", roi_coords);
						
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
	
	
	// Write the ROI info to the XML file
	public static void writeToXML(String in_xml_filename, String out_xml_filename, String xs[], String ys[], int series_n, String application_name, int roi_dimension, String roi_creation_username, String roi_creation_date, String image_size[]) 
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
						xmlw.writeAttribute("creation_date", roi_creation_date);
						xmlw.writeAttribute("creator_app", application_name);						
						xmlw.writeAttribute("creator_id", roi_creation_username);
						
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
						
						
						// For James and MRIW
						//for(int i=0; i<boundaries_array.length; i++){
							xmlw.writeStartElement("roi_for_mriw");
							
							xmlw.writeAttribute("x-size", image_size[0]);
							xmlw.writeAttribute("y-size", image_size[1]);
							
							String roi_coords = "";
							// Write the coordinates of the ROI as character element
							//for(int j=0; j<boundaries_array[i][file_element_counter].length; j++){
							for(int j=0; j<xs.length; j++){
								String roi_coord;
								//roi_coord = "(" + Double.toString(boundaries_array[i][file_element_counter][j][1]) + "," + Double.toString(boundaries_array[i][file_element_counter][j][0]) + ")";
								roi_coord = "(" + xs[j] + "," + ys[j] + ")"; 
								//if(boundaries_array[i][file_element_counter][j][1] != 0 && boundaries_array[i][file_element_counter][j][0] != 0){							
									//xmlw.writeCharacters(roi_coord);
								//	roi_coords += roi_coord;
								//}
								//xmlw.writeCharacters(" ");
								roi_coords += " ";
							}
							xmlw.writeAttribute("coordinates", roi_coords);
							
							xmlw.writeEndElement();
						//}
						
						
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
					int i = 0;
					//for(int i=0; i<boundaries_array.length; i++){
						xmlw.writeStartElement("roi_2d");
						xmlw.writeAttribute("label", Integer.toString(i));
						
						String roi_coords = "";
						// Write the coordinates of the ROI as character element
						//for(int j=0; j<boundaries_array[i][file_element_counter].length; j++){
						for(int j=0; j<xs.length; j++){
							String roi_coord;
							//roi_coord = "(" + Double.toString(boundaries_array[i][file_element_counter][j][0]) + "," + Double.toString(boundaries_array[i][file_element_counter][j][1]) + ")";
							roi_coord = "(" + ys[j] + "," + xs[j] + ")";
							//if(boundaries_array[i][file_element_counter][j][0] != 0 && boundaries_array[i][file_element_counter][j][1] != 0){							
								//xmlw.writeCharacters(roi_coord);
							//	roi_coords += roi_coord;
							//}
							//xmlw.writeCharacters(" ");
							roi_coords += " ";
						}
						xmlw.writeAttribute("coordinates", roi_coords);
						
						xmlw.writeEndElement();
					//}
										
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
    
    
}
