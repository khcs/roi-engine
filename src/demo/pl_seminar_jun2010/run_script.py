#!/usr/bin/env python
#
##
## Presentation for Physics Lunchtime Seminar
## 15. June. 2010
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

from scipy.signal import cspline1d, cspline1d_eval
from scipy import ogrid, sin, mgrid, ndimage, array
from numpy import arange, cos, linspace, pi, sin, random
from scipy.interpolate import splprep, splev

import socket



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

  n = 1000

  while True:

    navigate = \
             raw_input('Enter to proceed, p to previous, i to initialize, f to first slide, q to quit: ')

    if navigate == 'i':
      n = 0
    elif navigate == 'f':
      n = 1
    elif navigate == 'p':
      n -= 1
    elif navigate == 'q':
      break
    else:
      try:
        nn = int(navigate)
        n = nn
      except ValueError:
        n += 1
      
    if n == 0:
      ## initialize ##

      # read image
      dicom_path_input = \
                  '/Users/hshin/Works/PhD/Dataset/ICR/cvehlow/Liver_Pat3/DICOM/'
                  
      study_structure_get = read_dicom_files(dicom_path_input)
      series_name_get = study_series_selector(study_structure_get)
      im_3d, pixel_spacing, slice_thickness = \
             get_image(dicom_path_input, study_structure_get, series_name_get)
      print im_3d.max()
      break

      working_data_directory = \
                               path.join('/Users/hshin/workspace/ROI-Engine/data/')

      # automatic segmentation
      num_ROIs = 10
      T, im_3d_gf_uint16, rois_3d_n10 = automatic_segment_n_ROIs_preprocess(im_3d)

      for i in range(num_ROIs):
        rois_3d_current = automatic_segmentation(im_3d_gf_uint16, T)

        # automatic segmentation post-processing
        im_3d_gf_uint16, rois_3d_n10 = \
                         automatic_segment_n_ROIs_postprocess(rois_3d_n10, \
                                                             rois_3d_current, \
                                                             im_3d_gf_uint16)
 
      # automatic segmentation
      num_ROIs = 1
      T, im_3d_gf_uint16, rois_3d = automatic_segment_n_ROIs_preprocess(im_3d)

      for i in range(num_ROIs):
        rois_3d_current = automatic_segmentation(im_3d_gf_uint16, T)
      
        # get the center of the mass
        com_z, com_y, com_x = get_center_of_mass_VOI(rois_3d_current)
  
        # extract Boundary
        rois_3d_boundary, contours_list = get_boundary(rois_3d_current)

        # extract Boundary approx 1
        rois_3d_boundary_approx_1, contours_list_approx_1 = \
                               get_boundary(rois_3d_current, 'Simple')

        # extract Boundary poly approx
        rois_3d_boundary_approx_poly, contours_list_approx_poly = \
                               get_boundary(rois_3d_current, 'Poly')


        # write initial volume numpy array to DICOM in the working folder
        working_directory, working_name = modify_pixel_data(dicom_path_input, \
                                                         study_structure_get, \
                                                       series_name_get, im_3d, \
                                                       working_data_directory)

        # write ROI numpy array volume to DICOM in the working folder
        working_directory_ROI, working_name = modify_pixel_data(dicom_path_input, \
                                                          study_structure_get, \
                                             series_name_get, rois_3d_current, \
                                                  working_data_directory, 'ROIs', \
                                                                im_3d.max())

        # vmtk vtk convert initial volume
        working_directory_dicom = path.join(working_directory, 'DICOM')
        vtk_file_name = path.join(working_directory, working_name) + '.vtk'
        vtk_convert_argument = 'vmtkimagereader -f dicom -d ' + \
                               working_directory_dicom + \
                               ' --pipe vmtkimagewriter -ofile ' + \
                               vtk_file_name
        vtk_convert_argument = pypes.PypeRun(vtk_convert_argument)


        # vmtk vtk convert ROI volume
        working_directory_ROI_dicom = path.join(working_directory_ROI, 'DICOM')
        vtk_ROI_file_name = path.join(working_directory_ROI, working_name + '_ROIs') \
                      + '.vtk'
        vtk_ROI_convert_argument = 'vmtkimagereader -f dicom -d ' + \
                         working_directory_ROI_dicom + \
                         ' --pipe vmtkimagewriter -ofile ' + \
                         vtk_ROI_file_name
        vtk_convert_pype = pypes.PypeRun(vtk_ROI_convert_argument)


        # vmtk surface extraction
        vtk_surface_file_name = path.join(working_directory_ROI, working_name + \
                                '_Surface') + '.vtp'
        surface_extract_argument = 'vmtkmarchingcubes -ifile ' + \
                             vtk_ROI_file_name + ' -l 800 ' + \
                             ' -ofile ' + vtk_surface_file_name
        surface_extract_pype = pypes.PypeRun(surface_extract_argument)

        """
        # write n_ROI to DICOM
        working_directory_ROI_n10, working_name = \
                                 modify_pixel_data(dicom_path_input, \
                                                   study_structure_get, \
                                                   series_name_get, \
                                                   rois_3d_n10,\
                                                   working_data_directory, \
                                                   'ROIs_n10',\
                                                   im_3d.max())
        
        # write boundary extractions to DICOM
        working_directory_ROI_boundary, working_name = \
                                        modify_pixel_data(dicom_path_input, \
                                                          study_structure_get,\
                                                          series_name_get, \
                                                          rois_3d_boundary, \
                                                          working_data_directory, \
                                                          'ROIs_boundary',\
                                                          im_3d.max())

        
        working_directory_ROI_boundary_approx_1, working_name = \
                                        modify_pixel_data(dicom_path_input, \
                                                          study_structure_get,\
                                                          series_name_get, \
                                                          rois_3d_boundary_approx_1, \
                                                          working_data_directory, \
                                                          'ROIs_boundary_approx_1',\
                                                          im_3d.max())

        working_directory_ROI_boundary_approx_poly, working_name = \
                                        modify_pixel_data(dicom_path_input, \
                                                          study_structure_get,\
                                                          series_name_get, \
                                                       rois_3d_boundary_approx_poly, \
                                                          working_data_directory, \
                                                          'ROIs_boundary_approx_poly',\
                                                          im_3d.max())
      """

    elif n == 1:
      print n, ' VTK Initial Volume View'
      cv.DestroyWindow('Slicer-Seeded-Region-Growing-Success')

      vtk_initial_volume_view_argument = \
        'vmtkimagereader -f dicom -d ' + \
        '/Users/hshin/workspace/ROI-Engine/data/ep2d_diff_b0_750_spair_t_ADC/DICOM'\
        + ' --pipe vmtkimageviewer'
      pypes.PypeRun(vtk_initial_volume_view_argument)

    elif n == 2:
      print n, ' VTK 10 VOI View'

      slide = cv.LoadImage('./Data/vtk_initial_volume_viewer_capture.png')
      cv.ShowImage('VTK Initial Volume', slide)

      vtk_ROIn10_volume_view_argument = \
        'vmtkimagereader -f dicom -d ' + \
        '/Users/hshin/workspace/ROI-Engine/data/' + \
        'ep2d_diff_b0_750_spair_t_ADC/ROIs_n10/DICOM' + \
        ' --pipe vmtkimageviewer'
      pypes.PypeRun(vtk_ROIn10_volume_view_argument)

      slide = cv.LoadImage('./Data/vtk_initial_volume_viewer_capture.png')
      cv.ShowImage('VTK Initial Volume', slide)

    elif n == 3:
      print n, ' VTK 1 VOI View'

      vtk_ROI_view_argument = \
        'vmtkimagereader -f dicom -d ' + \
        '/Users/hshin/workspace/ROI-Engine/data/ep2d_diff_b0_750_spair_t_ADC/' +\
        'ROIs/DICOM' + \
        ' --pipe vmtkimageviewer'
      pypes.PypeRun(vtk_ROI_view_argument)

    elif n == 4:
      print n, ' VTK ROI Boundary View'

      vtk_ROI_bonudary_view_argument = \
        'vmtkimagereader -f dicom -d ' + \
        '/Users/hshin/workspace/ROI-Engine/data/ep2d_diff_b0_750_spair_t_ADC' + \
        '/ROIs_boundary/DICOM' + \
        ' --pipe vmtkimageviewer'
      pypes.PypeRun(vtk_ROI_bonudary_view_argument)      

    elif n == 5:
      print n, ' VTK ROI Surface View'

      vtk_ROI_surface_file_name = \
        '/Users/hshin/workspace/ROI-Engine/data/ep2d_diff_b0_750_spair_t_ADC/ROIs'+\
        '/ep2d_diff_b0_750_spair_t_ADC_Surface.vtp'
      vtk_ROI_surface_view_argument = \
        'vmtksurfacereader -ifile ' + \
        vtk_ROI_surface_file_name + \
        ' --pipe vmtksurfaceviewer'
      pypes.PypeRun(vtk_ROI_surface_view_argument)

    elif n == 6:
      print n, ' VTK ROI Boundary Approx 1 View'

      slide2 = cv.LoadImage('./Data/vtk_ROI_boundary_viewer_capture.png')
      cv.ShowImage('VTK ROI No.1 Boundary', slide2)

      vtk_ROI_surface_approx_1_folder_name = \
        '/Users/hshin/workspace/ROI-Engine/data/ep2d_diff_b0_750_spair_t_ADC/'+ \
        'ROIs_boundary_approx_1/DICOM'
      vtk_ROI_surface_approx_1_view_argument = \
        'vmtkimagereader -f dicom -d ' + \
        vtk_ROI_surface_approx_1_folder_name + \
        ' --pipe vmtkimageviewer'
      pypes.PypeRun(vtk_ROI_surface_approx_1_view_argument)

    elif n == 7:
      print n, ' VTK ROI Boundary Poly Approx View'
      
      vtk_ROI_surface_approx_poly_folder_name = \
        '/Users/hshin/workspace/ROI-Engine/data/ep2d_diff_b0_750_spair_t_ADC/'+ \
        'ROIs_boundary_approx_poly/DICOM'
      vtk_ROI_surface_approx_poly_view_argument = \
        'vmtkimagereader -f dicom -d ' + \
        vtk_ROI_surface_approx_poly_folder_name + \
        ' --pipe vmtkimageviewer'
      pypes.PypeRun(vtk_ROI_surface_approx_poly_view_argument)

    elif n == 8:
      print n, ' Center of Mass and B-Spline Approximation'

      cv.DestroyWindow('VTK Initial Volume')
      cv.DestroyWindow('VTK ROI No.1 Boundary')
        
      com_z, com_y, com_x = get_center_of_mass_VOI(rois_3d_current)
      print 'C.O.M-z: ', com_z, ', C.O.M.-y: ', com_y, ', C.O.M.-x: ', com_x 

      draw_b_spline_approx(contours_list_approx_poly, rois_3d_current, \
                                              pixel_spacing, slice_thickness)

    elif n == 9:
      print n, ' Runges Phenomenon'
        
      slide = cv.LoadImage('./Data/632px-Rungesphenomenon-wiki.png')
      cv.ShowImage('Rugesphenomenon', slide)

      """
      elif n == 10:
      print n, ' Log-in ROI-Engine'
      
      cv.DestroyWindow('Rugesphenomenon')
      
      local_ip_address = socket.gethostbyname(socket.gethostname())
      os.system('open http://' + local_ip_address + ':9090')
      """

    elif n == 10:
      print n, ' ROI-Engine Server'
      
      #documentation = \
      #        '/Users/hshin/workspace/ROI-Engine/doc/sphinx/build/html/index.html'
      ROI_Engine = 'http://localhost:9090'
      os.system('open ' + ROI_Engine)

    else:
      n += 1
      print n
      pass



