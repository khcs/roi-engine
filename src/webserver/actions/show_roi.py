'''
Created on 8 Sep 2010

@author: hshin
'''

import cherrypy
from lib import template

from os import path
import sys, zipfile, os

from cherrypy.lib.static import serve_file

import cgi, tempfile

sys.path.append(os.path.abspath('../'))
from get_data.dicom_parser import *
from viewers.show import *
from segment.automatic_segment import *
from set_data.dicom_writer import *
from shape_analysis.geometric_info import *
from converters.opencv import *

class myFieldStorage(cgi.FieldStorage):
  def make_file(self, binary=None):
    return tempfile.NamedTemporaryFile()

def noBodyProcess():
  cherrypy.request.process_request_body = False

cherrypy.tools.noBodyProcess = \
                            cherrypy.Tool('before_request_body', noBodyProcess)

class ShowROI(object):
  
    dicom_dir = None
    study_structure_get = None
    series_name = None
    series_num = None
    
    @cherrypy.expose
    @template.output('show_roi.html')
    def index(self):
      return template.render()  
      
    def unzip_file_into_subdir(self, file, dir):
      
      try:
        erase_dicom_related_files_script = 'rm -rf ../../data/show_roi_temp/DICOM/*'
        os.system(erase_dicom_related_files_script)
      finally:
        pass
      
      zfobj = zipfile.ZipFile(file)
      for name in zfobj.namelist():
        if name.endswith('/'):
          if not path.exists(os.path.join(dir, name)):
            os.mkdir(os.path.join(dir, name))
        else:
          outfile = open(os.path.join(dir, name), 'wb')
          outfile.write(zfobj.read(name))
          outfile.close()   
       
    def study_series_selector(self, dicom_path_input):      
      study_structure_get = read_dicom_files(dicom_path_input)
      self.study_structure_get = study_structure_get
      n = 0
      series_name = []
      
      returnstring = '<html><body>'
      returnstring += \
            '<h3>Enter the number of the series to study on</h3>'
            
      for series in study_structure_get.iteritems():
        n = n + 1
        series_name.append(series[0])
        returnstring = returnstring + str(n) + ' ' + series[0] + '<br />'      
      self.series_name = series_name
      
      returnstring += '<form action="get_image" method="post">'
      
      returnstring += '<input type="text" name="series_num_str" value=""'
      returnstring += 'size="3" maxlength="5"/>'
 
      returnstring += '<h3>Enther the number of the ROIs you want to find</h3>'
      returnstring += '<input type="text" name="num_rois_str" value=""'
      returnstring += 'size="3" maxlength="5"/>'
      
      returnstring += '<p><input type="submit" value="Submit" /></p>'
      
      returnstring += '</form>'
                              
      returnstring += '</body></html>'
      return returnstring
    
    
    def get_dicom_file_names(self, dicom_path, study_structure_in, \
                             series_name_to_study_in):
      series_structure = study_structure_in[series_name_to_study_in]

      dicom_files_structure = series_structure['dicom_files']

      dicom_files_list = []
      dicom_files_structured_list = {}
      dicom_files_structured_list_sorted = {}
       
      for files_key in sorted(dicom_files_structure.iterkeys()):
          dicom_files_list.append(files_key)
      
      return dicom_files_list
    
    
    @cherrypy.expose
    def get_image(self, series_num_str, num_rois_str):            
      series_num = int(series_num_str)
      num_ROIs = int(num_rois_str)
      
      self.series_num = series_num
      
      series_name_get = self.series_name[int(series_num) - 1]
      
      im_3d, pixel_spacing, slice_thickness = \
        get_image(self.dicom_dir, self.study_structure_get, series_name_get)
      
      working_data_directory = \
                            path.join('../data')
      
      T, im_3d_gf_uint16, rois_3d_nx = \
                                    automatic_segment_n_ROIs_preprocess(im_3d)  
      
      com_z = []
      com_y = []
      com_x = []            
      matlabpath = path.abspath(path.join('..', 'matlab'))
      
                        
      for i in range(num_ROIs):
        rois_3d_current = automatic_segmentation(im_3d_gf_uint16, T)
        z, y, x = get_center_of_mass_VOI(rois_3d_current)
        com_z.append(z)
        com_y.append(y)
        com_x.append(x)
        
 

        f = open(matlabpath + '/ROI_' + str(i) + '.txt', 'w')
        for j in range(rois_3d_current.shape[2]):
          for k in range(rois_3d_current.shape[1]):
            for l in range(rois_3d_current.shape[0]):
              if rois_3d_current[l,k,j] > 0:
                f.write(str(j) + '\t' + str(k) + '\t' + str(l) + '\n')        
        
        im_3d_gf_uint16, rois_3d_nx = \
                        automatic_segment_n_ROIs_postprocess(rois_3d_nx, \
                                                             rois_3d_current, \
                                                             im_3d_gf_uint16)        
                        
        f.close()       

      
      
      dicom_files_list = self.get_dicom_file_names(self.dicom_dir, \
                                      self.study_structure_get, series_name_get)
            
      f = open(matlabpath + '/dicom_files.txt', 'w')
      for i in range(len(dicom_files_list)):
        f.write(dicom_files_list[i] + '\t' + path.abspath(self.dicom_dir)\
                + '/' + '\n')
      f.close()
      
      f = open(matlabpath + '/seed_points.txt', 'w')
      for i in range(len(com_z)):
        f.write(str(com_x[i]) + '\t' + str(com_y[i]) + '\t' + str(com_z[i]) +\
                '\n')
      f.close()
      
      
      os.chdir('../matlab')
      remove_previous_images_script = 'rm ' + \
                                      '../../data/mriw_temp/download/image/*'
      os.system(remove_previous_images_script)
      
      run_matlab_script = 'matlab -r ' + '"' + 'hoo_roi_engine_liver' + '"'
      os.system(run_matlab_script)
      
      os.system(run_matlab_script)
      images = os.listdir('../../data/mriw_temp/download/image')
      for i in range(len(images)):
        convert_to_jpg_script = 'convert ' + \
                                '../../data/mriw_temp/download/image/' + \
                                images[i] + \
                                ' ../../data/mriw_temp/download/image/' + \
                                images[i] +\
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
           str(i+1) + '.bmp.jpg"' + '/>'
           #images[i] + '.jpg"' + '/>'
      
              
      displayimage_html_string += '<br />'
      
      copy_colors_script = 'cp ../matlab/colorset/* ' + \
                           '../../data/mriw_temp/download/image'
      os.system(copy_colors_script)
      
      for i in range(num_ROIs):
        displayimage_html_string += str(i+1) + 'th ROI: ' +\
                                    '<image src="/images/color-' + \
                                    str(i+1) + '.jpg" alt="' + \
                                    str(i+1) + 'th ROI"/> ' + \
                                    'center of mass: (' + str(com_x[i]) + \
                                    ',' + str(com_y[i]) + ',' + \
                                    str(com_z[i]) + ')<br />'
      
                                  
      displayimage_html_string += '<form action="select_roi" method="post">'
 
      displayimage_html_string += '<h3>Enther the number of the ROI of your interest:</h3>'
      displayimage_html_string += '<input type="text" name="roi_num_str" value=""'
      displayimage_html_string += 'size="3" maxlength="5"/>'
      
      displayimage_html_string += '<p><input type="submit" value="Submit" /></p>'
      
      displayimage_html_string += '</form>'
            
      displayimage_html_string += '</body></html>'
      
      
      return displayimage_html_string
    
      
    @cherrypy.expose
    def select_roi(self, roi_num_str):
      os.chdir('../matlab')
      
      print '!!! matlab -r "hoo_roi_engine_liver_write_xml !!!'
      
      run_matlab_script = 'matlab -r "hoo_roi_engine_liver_write_xml ' +\
                          roi_num_str + ' ' + str(self.series_num) + '"'
      os.system(run_matlab_script)
      
      erase_tmp_files_script_1 = 'rm dicom_files.txt'
      erase_tmp_files_script_2 = 'rm seed_points.txt'
      erase_tmp_files_script_3 = 'rm ROI_*.txt'
      
      os.system(erase_tmp_files_script_1)
      os.system(erase_tmp_files_script_2)
      os.system(erase_tmp_files_script_3)
      
      os.chdir('../webserver')      
      
      
      post_xml_file_list = os.listdir('../../data/mriw_temp/download/xml')
      post_xml_file = post_xml_file_list[0]
      absPath = \
              path.abspath('../../data/mriw_temp/download/xml/' + post_xml_file)
              
      displayimage_html_string = '<html><body>'
      displayimage_html_string += '<br />' + \
                                  '<a href="download/?filepath=' + absPath + \
                                  '">' + 'Download the ROI-XML-File' + \
                                  '</a><br />'
            
      displayimage_html_string += '</body></html>'
      return displayimage_html_string

       
    @cherrypy.expose
    def upload(self, dicomFileZip=None):
      
      cherrypy.response.timeout = 3600

      dicom_file_zip = path.join('..', '..', 'data', 'show_roi_temp',\
                               dicomFileZip.filename)
      dicom_file_zip_w = open(dicom_file_zip, 'wb')
      while True:
        data = dicomFileZip.file.read(1024 * 8)
        if not data: break
        dicom_file_zip_w.write(data)
      dicom_file_zip_w.close()
      
      unzipped_dir = path.join('..', '..', 'data', 'show_roi_temp', 'DICOM')
      self.unzip_file_into_subdir(dicom_file_zip, unzipped_dir)
      
      unzipped_dir_list = os.listdir(unzipped_dir)
      if len(unzipped_dir_list) == 1:
        dicom_dir = path.join(unzipped_dir, unzipped_dir_list[0])
      else:
        dicom_dir = unzipped_dir
        
      returnstring = self.study_series_selector(dicom_dir)
      self.dicom_dir = dicom_dir
      
      return returnstring
    

class Download:
  @cherrypy.expose
  def index(self, filepath):
    return serve_file(filepath, "application/x-download", "attachment")

