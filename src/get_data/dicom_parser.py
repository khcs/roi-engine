#!/usr/bin/env python
#
##
## DICOM Parser
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#
"""
Module for getting data from DICOM files.

:func:`read_dicom_files`: Read DICOM files from a folder specified by the user.

:func:`study_series_selector`: Let user select a study series to analyze.

:func:`get_image`: Get 3D image array.

==================================
dicom_parser function definitions
==================================
"""



import os
from os import path

import dicom
import numpy


def read_dicom_files(dicom_path):
  """
  read_dicom_files

  .. tabularcolumns:: |l|L|

  ==============   ====================================================
  Keyword          Description
  ==============   ====================================================
  dicom_path       Path to the DICOM files to load.
  ==============   ====================================================

  returns the parse result as a Python dictionary type::
  
  --{''Series Name'':  
  ----{'StudyInstanceUID': 'x.x.x.x',
  -----'SeriesInstanceUID': 'x.x.x.x',
  -----'dicom_files':
  ------{''DICOM file name'':
  --------{'SOPInstanceUID': 'x.x.x.x'}
  ------}
  ----}
  --}
  """

  files_list = os.listdir(dicom_path)

  study_structure = {}
  dicom_files_list = {}

  for file_n in files_list:
    i_file = dicom.read_file(path.join(dicom_path, file_n))

    try:
      study_structure_sub = study_structure[i_file.SeriesDescription]
      dicom_files_list = study_structure_sub['dicom_files']
      dicom_files_list[file_n] = {'SOPInstanceUID': i_file.SOPInstanceUID}

    except KeyError:
      dicom_files_list = {}
      dicom_files_list[file_n] = {'SOPInstanceUID': i_file.SOPInstanceUID}

    study_structure[i_file.SeriesDescription] = \
            {'SeriesInstanceUID': i_file.SeriesInstanceUID, \
             'StudyInstanceUID': i_file.StudyInstanceUID, \
             'PixelSpacing': i_file.PixelSpacing, \
             'SliceThickness': i_file.SliceThickness, \
             'dicom_files': dicom_files_list}

  return study_structure



def study_series_selector(study_structure_in):
  """
  study_series_selector

  .. tabularcolumns:: |l|L|

  ===================   ====================================================
  Keyword               Description
  ===================   ====================================================
  study_structure_in    study_structure returned from the 
                        :func:`read_dicom_files`
  ===================   ====================================================

  returns SeriesDescription of user's selection.
  """
    
  n = 0
  series_name = []

  for series in study_structure_in.iteritems():
    n = n + 1
    series_name.append(series[0])
    print n, series[0]

  series_n_to_study = input('Enter the number of the Series to study: ')
  series_name_to_study =  series_name[series_n_to_study - 1]

  return series_name_to_study



def get_image(dicom_path, study_structure_in, series_name_to_study_in):
  """
  get_image

  .. tabularcolumns:: |l|L|

  =======================   =================================================
  Keyword                   Description
  =======================   =================================================
  dicom_path                Path to the DICOM files.
  study_structure_in        study_structure returned from the 
                            :func:`read_dicom_riles`
  series_name_to_study_in   series_name_to_study returned from the 
                            :func:`study_series_selector`
  =======================   =================================================

  returns 3D image array, PixelSpacing and SliceThickness.
  """
  series_structure = study_structure_in[series_name_to_study_in]

  dicom_files_structure = series_structure['dicom_files']

  dicom_files_list = []
  
  for files_key in sorted(dicom_files_structure.iterkeys()):
    dicom_files_list.append(files_key)

  for i, dicom_file in enumerate(dicom_files_list):
    dicom_read = dicom.read_file(path.join(dicom_path, dicom_file))

    if i == 0:
      pixel_array = dicom_read.pixel_array
      image_array_3d = numpy.zeros((len(dicom_files_list), \
                                    pixel_array.shape[0], \
                                    pixel_array.shape[1]), dtype = numpy.int16)

    image_array_3d[i] = dicom_read.pixel_array

  pixel_spacing = dicom_read.PixelSpacing
  slice_thickness = dicom_read.SliceThickness


  return image_array_3d, pixel_spacing, slice_thickness



if __name__=='__main__':
  # import the viewers -- for test --
  import sys, os
  sys.path.append(os.path.abspath('../'))
  from viewers.show import *

  #dicom_path_input = raw_input('Enter the directory path to read the \
  #                              DICOM files from:')
  dicom_path_input = '/Users/hshin/Works/PhD/Dataset/ICR/cvehlow/Liver_Pat3' + \
                     '/DICOM'

  study_structure_get = read_dicom_files(dicom_path_input)

  series_name_get = study_series_selector(study_structure_get)

  im_3d, pixel_spacing, slice_thickness = \
              get_image(dicom_path_input, study_structure_get, series_name_get)

  show_image(im_3d)

