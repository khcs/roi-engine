'''
Created on 2 Sep 2010

@author: hshin
'''

import cherrypy
from lib import template

from os import path
import sys, zipfile, os

from cherrypy.lib.static import serve_file


class ReadMriwXML(object):
    
    @cherrypy.expose
    @template.output('mriw.html')
    def index(self):
      return template.render()
    
    
    def unzip_file_into_subdir(self, file, dir):
      zfobj = zipfile.ZipFile(file)
      for name in zfobj.namelist():
        if name.endswith('/'):
          if not path.exists(os.path.join(dir, name)):
            os.mkdir(os.path.join(dir, name))
        else:
          outfile = open(os.path.join(dir, name), 'wb')
          outfile.write(zfobj.read(name))
          outfile.close()
          
    def run_matlab(self, xml_file, dicom_dir):
      os.chdir('../matlab')
      remove_previous_images_script = 'rm ' + \
                                      '../../data/mriw_temp/download/image/*'
      remove_previous_xml_files_script = 'rm ' + \
                                      '../../data/mriw_temp/download/xml/*'
      os.system(remove_previous_images_script)
      
      run_matlab_script = 'matlab -r ' + '"' +  'hoo_read_mriw_xml' + ' ' \
                          + xml_file + ' ' \
                          + ' ' + dicom_dir + '"'
      #matlab -r "hoo_read_mriw_xml cosine_results.xml /home/hshin/workspace/ROI-Engine/src/matlab/testdata/srtf_breast/DICOM/"
      os.system(run_matlab_script)
      images = os.listdir('../../data/mriw_temp/download/image')
      for i in range(len(images)):
        convert_to_jpg_script = 'convert ' + \
                                '../../data/mriw_temp/download/image/' + \
                                images[i] + \
                                ' ../../data/mriw_temp/download/image/' + \
                                images[i] + \
                                '.jpg'
        os.system(convert_to_jpg_script)
        remove_bmp_script = 'rm ' + '../../data/mriw_temp/download/image/' + \
         images[i]
        os.system(remove_bmp_script)
                                    
      os.chdir('../webserver')
      
      displayimage_html_string = '<html><body>'
      for i in range(len(images)):
        displayimage_html_string = displayimage_html_string + \
          '<img src="' + \
           '/images/' +\
           images[i] + '.jpg"' + '/>'
      
      post_xml_file_list = os.listdir('../../data/mriw_temp/download/xml')
      post_xml_file = post_xml_file_list[0]
      absPath = \
              path.abspath('../../data/mriw_temp/download/xml/' + post_xml_file)
      displayimage_html_string += '<br />' + \
                                  '<a href="download/?filepath=' + absPath + \
                                  '">' + 'Download the ROI-XML-File' + \
                                  '</a><br />'
            
      displayimage_html_string += '</body></html>'
      return displayimage_html_string
    
    @cherrypy.expose 
    def upload(self, mriwXmlFile, dicomFileMriwXmlZip):
      mriw_xml_file = path.join('..', '..', 'data', 'mriw_temp', \
                                mriwXmlFile.filename)
      mriw_xml_file_w = open(mriw_xml_file, 'wb')
      while True:
        data = mriwXmlFile.file.read(1024 * 8)
        if not data: break
        mriw_xml_file_w.write(data)
      mriw_xml_file_w.close()
        
      mriw_dicom_file_zip = path.join('..', '..', 'data', 'mriw_temp', \
                                      dicomFileMriwXmlZip.filename)
      mriw_dicom_file_zip_w = open(mriw_dicom_file_zip, 'wb')
      while True:
        data = dicomFileMriwXmlZip.file.read(1024 * 8)
        if not data: break
        mriw_dicom_file_zip_w.write(data)
      mriw_dicom_file_zip_w.close()
      
      unzipped_dir = path.join('..', '..', 'data', 'mriw_temp', 'DICOM')
      self.unzip_file_into_subdir(mriw_dicom_file_zip, unzipped_dir)
      
      unzipped_dir_list = os.listdir(unzipped_dir)
      if len(unzipped_dir_list) == 1:
        dicom_dir = path.join(unzipped_dir, unzipped_dir_list[0])
      else:
        dicom_dir = unzipped_dir
        
      returnstring = \
       self.run_matlab(path.abspath(mriw_xml_file), path.abspath(dicom_dir)+'/')
      
      return returnstring
      

class Download:
  @cherrypy.expose
  def index(self, filepath):
    return serve_file(filepath, "application/x-download", "attachment")
