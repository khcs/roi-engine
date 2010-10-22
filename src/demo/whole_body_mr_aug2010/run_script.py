#!/usr/bin/env python
#
##
## To test ROI-Engine with Matt.B.'s whole body mr scan data
## 16.Aug.2010
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#

import os
from os import path

import numpy
from numpy import *
import pylab

import cv

from vmtk import pypes
from vmtk import vmtkscripts


def do_the_work():
  dicom_path_input = raw_input('Enter the directory path to read the ' +\
                                'DICOM files from: ')
  if len(dicom_path_input) <= 1:
    dicom_path_input = \
            '/Users/hshin/Works/PhD/Dataset/ICR/Matt.B/WBDWI_pat_280110/DICOM/'
            
  study_structure_get = read_dicom_files(dicom_path_input)
  series_name_get = study_series_selector(study_structure_get) 
  im_3d, pixel_spacing, slice_thickness, dicom_files_list, b_value = \
        get_image(dicom_path_input, study_structure_get, series_name_get, True)
  


  working_data_directory = \
                            path.join('/Users/hshin/workspace/ROI-Engine/data/')
  working_data_directory_series_dicom = path.join(working_data_directory, \
                                                  series_name_get, \
                                                  'B_' + str(b_value), 'DICOM')                          
  working_data_directory_series_dicom_ROIs = path.join(working_data_directory, \
                                                  series_name_get, \
                                                  'B_' + str(b_value),\
                                                  'ROIs', 'DICOM')
                            
  if path.exists(path.join(working_data_directory_series_dicom_ROIs)):
    print 'You have a history of working on dataset.'
    redo = raw_input('Would you like to re-do it? (Y/N): ')
    if redo == 'Y' or redo == 'y':
      pass
    else:
      return b_value
  
  

  
  # automatic segmentation
  num_ROIs = 10
  T, im_3d_gf_uint16, rois_3d_n20 = automatic_segment_n_ROIs_preprocess(im_3d)
  
  for i in range(num_ROIs):
        rois_3d_current = automatic_segmentation(im_3d_gf_uint16, T)
        print str(i) + 'th ROI'
        # automatic segmentation post-processing
        im_3d_gf_uint16, rois_3d_n20 = \
                         automatic_segment_n_ROIs_postprocess(rois_3d_n20, \
                                                              rois_3d_current, \
                                                              im_3d_gf_uint16)
                         
  
            
            
  # automatic segmentation
  num_ROIs = 1
  T, im_3d_gf_uint16, rois_3d = automatic_segment_n_ROIs_preprocess(im_3d)

  for i in range(num_ROIs):
    rois_3d_current_1ROI = automatic_segmentation(im_3d_gf_uint16, T)
      
    # get the center of the mass
    #com_z, com_y, com_x = get_center_of_mass_VOI(rois_3d_current)
  
    # extract Boundary
    rois_3d_boundary, contours_list = get_boundary(rois_3d_current_1ROI)

    # extract Boundary approx 1
    #rois_3d_boundary_approx_1, contours_list_approx_1 = \
    #                                    get_boundary(rois_3d_current, 'Simple')

    # extract Boundary poly approx
    rois_3d_boundary_approx_poly, contours_list_approx_poly = \
                                          get_boundary(rois_3d_current_1ROI,\
                                                       'Poly')



 
 
  # write initial volume numpy array to DICOM in the working folder  
  write_new_dicom_files(dicom_path_input, dicom_files_list, series_name_get, \
                        b_value, im_3d, working_data_directory)
  
  # vmtk vtk convert initial volume
  vtk_file_name = path.join(working_data_directory,\
                            series_name_get,
                            'B_' + str(b_value), \
                            series_name_get + '_B_' + str(b_value)) + '.vtk'
  vtk_convert_argument = 'vmtkimagereader -f dicom -d ' + \
                          working_data_directory_series_dicom + \
                          ' --pipe vmtkimagewriter -ofile ' + \
                          vtk_file_name
  vtk_convert_argument = pypes.PypeRun(vtk_convert_argument)
  
  
  
  
  # write ROI numpy array volume to DICOM in the working folder
  write_new_dicom_files_ROI(dicom_path_input, dicom_files_list, series_name_get,\
                        b_value, rois_3d_n20, working_data_directory,\
                        'ROIs', 1000)
  
  # vmtk vtk convert ROI volume
  vtk_file_name_ROIs = path.join(working_data_directory,\
                            series_name_get,
                            'B_' + str(b_value), \
                            'ROIs',
                            series_name_get + '_B_' + str(b_value)) \
                            + '_ROIs' + '.vtk'
  vtk_convert_argument_ROIs = 'vmtkimagereader -f dicom -d ' + \
                          working_data_directory_series_dicom_ROIs + \
                          ' --pipe vmtkimagewriter -ofile ' + \
                          vtk_file_name_ROIs
  vtk_convert_argument_ROIs = pypes.PypeRun(vtk_convert_argument_ROIs)


  return b_value



if __name__ == '__main__':
  # import my modules
  import sys, os
  sys.path.append(os.path.abspath('/Users/hshin/workspace/ROI-Engine/src'))
  from get_data.dicom_parser import *
  from viewers.show import *
  from segment.automatic_segment import *
  from set_data.dicom_writer import *
  from shape_analysis.geometric_info import *
  from converters.opencv import *
  
  
  b_value = do_the_work()

  
  # view the initial volume
  vtk_initial_volume_view_argument = \
        'vmtkimagereader -f dicom -d ' + \
        '/Users/hshin/workspace/ROI-Engine/data/ep2d_diff_386a_WBDWI_IR'\
        + '/B_' + str(b_value) + '/DICOM'\
        + ' --pipe vmtkimageviewer'
  pypes.PypeRun(vtk_initial_volume_view_argument)
  
  # view the ROIs volume
  vtk_ROIs_volume_view_argument = \
        'vmtkimagereader -ifile ' + \
        ' /Users/hshin/workspace/ROI-Engine/data/' + \
        'ep2d_diff_386a_WBDWI_IR/B_900/ROIs/' + \
        'ep2d_diff_386a_WBDWI_IR_B_900_ROIs.vtk ' + \
        '--pipe vmtkimageviewer'
  pypes.PypeRun(vtk_ROIs_volume_view_argument)
  
        
  
  