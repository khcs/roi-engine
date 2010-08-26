/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ParseDICOM_Test;

import java.io.*;
import org.xml.sax.*;
import org.xml.sax.helpers.AttributesImpl;

/**
 *
 * @author hshin
 */
public class ReadDICOMparseResult implements XMLReader {
    ContentHandler handler;

    String nsu = ""; // NamespaceURI
    Attributes atts = new AttributesImpl();
    String rootElement = "DICOM files parse result";
    //String indent; // for readability
    String[] parent_elements = {"working_directory", "series_number"};

    public void parse(InputSource input)
            throws IOException, SAXException{
        try{
            // Get an efficient reader for the file
            java.io.Reader r = input.getCharacterStream();
            BufferedReader br = new BufferedReader(r);

            // Read the file and display its contents
            String line;// = br.readLine();
            //System.out.println(line);

            if (handler == null){
                throw new SAXException("No content handler");
            }

           
            // Ignoring setDocumentLocator() for the moment
            handler.startDocument();
            
            int indent_step = 0;
            String indent = indentMaker(indent_step);

            handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
            handler.startElement(nsu, rootElement, rootElement, atts);

            String name;
            while( (name = output(br,2)) != null ){
                handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
                handler.endElement(nsu, name, name);
                //output(reader, indent_step);
            }


            /*
            while(null != (line = br.readLine())){                
                if (line.startsWith("working_directory"))
                    break;
            }            
            int startIndex = "working_directory".length() + 2;            
            String text = line.substring(startIndex);
            int textLength = line.length() - startIndex;
            handler.ignorableWhitespace(indent_3.toCharArray(), 0, indent_3.length());
            handler.startElement(nsu, "working_directory", "working_directory", atts);
            handler.characters(line.toCharArray(), startIndex, textLength);

            

            handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
            String name;
            int deliminator_index;
            while(null != (line = br.readLine())){
                deliminator_index = line.indexOf(":");
                name = line.substring(0, deliminator_index);                
                output(name, line);
            }

            handler.endElement(nsu, "working_directory", "working_directory");             
             */

            handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
            handler.endElement(nsu, rootElement, rootElement);                  
            handler.endDocument();

        }catch(Exception e){
            e.printStackTrace();
        }
    }

    String output(BufferedReader reader, int indent_step)
            throws SAXException{

        try{
            String line = reader.readLine();
            if(line == null){
                return null;
            }
            String indent = indentMaker(indent_step);
            
            int deliminator_index = line.indexOf(":");
            String name = line.substring(0, deliminator_index);

            int startIndex = name.length() + 2; //2=length of ": " after the name

            handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
            handler.startElement(nsu, name, name /*"qName"*/, atts);
                String text = line.substring(startIndex);
                int textLength = line.length() - startIndex;
                handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
                handler.characters(line.toCharArray(), startIndex, textLength);

            for(int i=0; i<parent_elements.length; i++){
                if(name.equals(parent_elements[i])){                 
                    output(reader, indent_step+2);
                }else{                    
                    //handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
                    //handler.endElement(nsu, name, name);
                    //output(reader, indent_step);
                }
            }

            //handler.ignorableWhitespace(indent.toCharArray(), 0, indent.length());
            //handler.endElement(nsu, name, name);
            //output(reader, indent_step);

            //return indent_step;
            return name;
        }catch(Exception e){
            e.printStackTrace();
            return null;
        }
        
    }

    String indentMaker(int step){
        String indent = "\n";
        for(int i=0; i<step; i++){
            indent = indent + "    ";
        }
        return indent;
    }

    
    /*
    public void writeToXML(String stored_info, String working_directory,
            String dicom_files[][], String dicom_metadata[][][]){


        // Print out to StdOutput
        System.out.println();
        System.out.println(stored_info);
        System.out.println(working_directory);
        System.out.println();

        for(int i=0; i<dicom_metadata.length; i++){
            for(int j=0; j<dicom_metadata[i].length; j++){
                System.out.println(dicom_metadata[i][j][0] + " : " + dicom_metadata[i][j][1]);
            }

            for(int k=0; k<dicom_files[i].length; k++){
                if(dicom_files[i][k] != null)
                    System.out.println(dicom_files[i][k]);
            }
            System.out.println();
        }
        ///

    }
    */
    

    

    /** Allow an application to register a content event handler. */
    public void setContentHandler(ContentHandler handler) {
        this.handler = handler;
    }

    /** Return the current content handler. */
    public ContentHandler getContentHandler() {
        return this.handler;
    }

    //=============================================
    // IMPLEMENT THESE FOR A ROBUST APP
    //=============================================
    public void setErrorHandler(ErrorHandler handler) {
    }

    /** Return the current error handler. */
    public ErrorHandler getErrorHandler() {
        return null;
    }

    //=============================================
    // IGNORE THESE
    //=============================================

    /** Return the current DTD handler. */
    public DTDHandler getDTDHandler() {
        return null;
    }

    /** Return the current entity resolver. */
    public EntityResolver getEntityResolver() {
        return null;
    }

    /** Allow an application to register an entity resolver. */
    public void setEntityResolver(EntityResolver resolver) {
    }

    /** Allow an application to register a DTD event handler. */
    public void setDTDHandler(DTDHandler handler) {
    }

    /** Look up the value of a property. */
    public Object getProperty(String name) {
        return null;
    }

    /** Set the value of a property. */
    public void setProperty(String name, Object value) {
    }

    /** Set the state of a feature. */
    public void setFeature(String name, boolean value) {
    }

    /** Look up the value of a feature. */
    public boolean getFeature(String name) {
        return false;
    }

    public void parse(String systemId) throws IOException, SAXException {
        throw new UnsupportedOperationException("Not supported yet.");
    }


}
