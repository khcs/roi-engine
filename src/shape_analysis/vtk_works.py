#!/usr/bin/env python
#
##
## VTK Works
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#

import numpy
from numpy import *
import pylab

import os
from os import path

#from vmtk import pypes
from vmtk import vmtkscripts
from vmtk import pype


def show_volume_roi_surface(dicom_path_input, working_data_directory, \
                            study_structure_get, im_3d, rois_3d, \
                            series_name_get):
  # write initial volume numpy array to DICOM in the working folder
  working_directory, working_name = modify_pixel_data(dicom_path_input, \
                                        study_structure_get, \
                                        series_name_get, im_3d, \
                                        working_data_directory)

  # write ROI numpy array volume to DICOM in the working folder
  working_directory_ROI, working_name = modify_pixel_data(dicom_path_input, \
                                        study_structure_get, \
                                        series_name_get, rois_3d, \
                                        working_data_directory, 'ROIs', \
                                        im_3d.max())

  # vmtk vtk convert initial volume
  working_directory_dicom = path.join(working_directory, 'DICOM')
  vtk_file_name = path.join(working_directory, working_name) + '.vtk'
  vtk_convert_argument = 'vmtkimagereader -f dicom -d ' + \
                         working_directory_dicom + \
                         ' --pipe vmtkimagewriter -ofile ' + \
                         vtk_file_name
  vtk_convert_argument = pype.PypeRun(vtk_convert_argument)

  # vmtk vtk convert ROI volume
  working_directory_ROI_dicom = path.join(working_directory_ROI, 'DICOM')
  vtk_ROI_file_name = path.join(working_directory_ROI, working_name + '_ROIs') \
                      + '.vtk'
  vtk_ROI_convert_argument = 'vmtkimagereader -f dicom -d ' + \
                         working_directory_ROI_dicom + \
                         ' --pipe vmtkimagewriter -ofile ' + \
                         vtk_ROI_file_name
  vtk_convert_pype = pype.PypeRun(vtk_ROI_convert_argument)

  # vmtk surface extraction
  vtk_surface_file_name = path.join(working_directory_ROI, working_name + \
                                '_Surface') + '.vtp'
  surface_extract_argument = 'vmtkmarchingcubes -ifile ' + \
                             vtk_ROI_file_name + ' -l 800 ' + \
                             ' -ofile ' + vtk_surface_file_name
  surface_extract_pype = pype.PypeRun(surface_extract_argument)
  
  # show images in vtk viewer
  vtk_init_volume_show_argument = 'vmtkimagereader -ifile ' + vtk_file_name + \
                      ' --pipe vmtkimageviewer'
  init_volume_show_pype = pype.PypeRun(vtk_init_volume_show_argument)

  vtk_ROI_volume_show_argument = 'vmtkimagereader -ifile ' + vtk_ROI_file_name+\
                                 ' --pipe vmtkimageviewer'
  roi_volume_show_pype = pype.PypeRun(vtk_ROI_volume_show_argument)

  vtk_ROI_surface_show_argument = 'vmtksurfacereader -ifile ' + \
                                  vtk_surface_file_name + \
                                  ' --pipe vmtksurfaceviewer'
  vtk_ROI_surface_show_pype = pype.PypeRun(vtk_ROI_surface_show_argument)





if __name__=='__main__':
  # import the modules -- for test --
  import sys, os
  sys.path.append(os.path.abspath('../'))
  from get_data.dicom_parser import *
  from viewers.show import *
  from segment.automatic_segment import *
  from set_data.dicom_writer import *

  # read image
  dicom_path_input = \
                   '/Users/hshin/Works/PhD/Dataset/ICR/cvehlow/Liver_Pat3/DICOM/'
  study_structure_get = read_dicom_files(dicom_path_input)
  series_name_get = study_series_selector(study_structure_get)
  im_3d, pixel_spacing, slice_thickness = \
         get_image(dicom_path_input, study_structure_get, series_name_get)

  # automatic segmentation
  num_ROIs = 1
  T, im_3d_gf_uint16, rois_3d = automatic_segment_n_ROIs_preprocess(im_3d)
  for i in range(num_ROIs):
    # automatic segmentation
    rois_3d_current = automatic_segmentation(im_3d_gf_uint16, T)

    # automatic segmentation post-processing
    im_3d_gf_uint16, rois_3d = automatic_segment_n_ROIs_postprocess(rois_3d, \
                                                             rois_3d_current, \
                                                             im_3d_gf_uint16)


  working_data_directory = path.join('../../data/')
  show_volume_roi_surface(dicom_path_input, working_data_directory, \
                          study_structure_get, im_3d, rois_3d, \
                          series_name_get)
