#!/usr/bin/env python
#
##
## DICOM Writer
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#
"""
Module for writing images to DICOM file format.

:func:`modify_pixel_data`: Write image, volume or 3D/2D ROI to DICOM file format.

==================================
dicom_writer function definitions
==================================
"""




import os
from os import path
import numpy

import dicom


def modify_pixel_data(dicom_path, study_structure, series_name, im_3d,\
                      modified_path, append_name=None, \
                      max_value_when_its_bool=None):
  """
  modify_pixel_data

  .. tabularcolumns:: |l|L|

  =======================   ====================================================
  Keyword                   Description
  =======================   ====================================================
  dicom_path                Path to the original DICOM files which is modified
                             from.
  study_structure           study_structure of the DICOM files, returned from
                             the :func:`read_dicom_files`
  series_name               series_name of the DICOM files to modify.
  im_3d                     3D image to save (it can be also 2D though).
  modified_path             New path to save the DICOM files.
  append_name               Name to append to the original DICOM files' names.
  max_value_when_its_bool   When the 3D ROI volume is in BOOL, the max value
                             (in int or float) to replace the TRUE of the BOOL.
  =======================   ====================================================

  returns the path to the saved DICOM files, and new name of the DICOM files.
  """
    
  series_structure = study_structure[series_name]
  dicom_files_structure = series_structure['dicom_files']


  new_path = path.join(modified_path, series_name)
  if path.exists(new_path):
    pass
  else:
    os.mkdir(new_path)


  #if append_name == 'ROIs':
  if append_name != None and 'ROIs' in append_name:
      
    new_path_ROI = path.join(new_path, append_name)    
    if path.exists(new_path_ROI):
      pass
    else:
      os.mkdir(new_path_ROI)

    new_path_ROI_dicom = path.join(new_path_ROI, 'DICOM')
    if path.exists(new_path_ROI_dicom):
      pass
    else:
      os.mkdir(new_path_ROI_dicom)
      
  else:
    new_path_dicom = path.join(new_path, 'DICOM')
    if path.exists(new_path_dicom):
      pass
    else:
      os.mkdir(new_path_dicom)


  dicom_files_list = []
  for files_key in sorted(dicom_files_structure.iterkeys()):
    dicom_files_list.append(files_key)

  print 'Saving data in DICOM format ...'
  for i, dicom_file in enumerate(dicom_files_list):
    dicom_read = dicom.read_file(path.join(dicom_path, dicom_file))


    if append_name != None and 'ROIs' in append_name:
      im_3d[im_3d == 1.0] = max_value_when_its_bool      
      im_3d = numpy.array(im_3d, dtype='int16')
      
      for j in range(im_3d[i].shape[0]):
        for k in range(im_3d[i].shape[1]):
          dicom_read.pixel_array[j][k] = im_3d[i][j][k]

      dicom_read.PixelData = dicom_read.pixel_array.tostring()

      new_name = dicom_file + '_' + append_name
      new_path_and_name = path.join(new_path_ROI_dicom, new_name)
    
      dicom_read.save_as(new_path_and_name)  
     
    else:
      new_name = dicom_file
      new_path_and_name = path.join(new_path_dicom, new_name)

      dicom_read.save_as(new_path_and_name)
      
      
  print '\t\t\t\t... done.'

  new_name = series_name
  if append_name != None and append_name == 'ROIs':
    new_path = new_path_ROI
  
  return new_path, new_name



def write_new_dicom_files(dicom_path, dicom_files_list, series_name, b_value, \
                          im_3d, modified_path):
  
  new_path_series = path.join(modified_path, series_name) 
  if path.exists(new_path_series):
    pass
  else:
    os.mkdir(new_path_series)
    
  new_path = path.join(new_path_series, 'B_'+str(b_value))
  if path.exists(new_path):
    pass
  else:
    os.mkdir(new_path)
    
  new_path_dicom = path.join(new_path, 'DICOM')
  if path.exists(new_path_dicom):
    pass
  else:
    os.mkdir(new_path_dicom)
    
    
  print 'Saving data in DICOM format ...'    
  
  for i, dicom_file in enumerate(dicom_files_list):
    dicom_read = dicom.read_file(path.join(dicom_path, dicom_file))
    if i == 0:
      series_number = dicom_read.SeriesNumber
      series_description = dicom_read.SeriesDescription
      series_instance_uid = dicom_read.SeriesInstanceUID
    
    if i < 10:
      new_name = '000' + str(i)
    elif i >= 10 and i < 100:
      new_name = '00' + str(i)
    elif i >= 100 and i < 1000:
      new_name = '0' + str(i)
    elif i >= 1000 and i < 10000:
      new_name = str(i)
 
    for j in range(im_3d[0].shape[0]):
      for k in range(im_3d[0].shape[1]):
        dicom_read.pixel_array[j][k] = im_3d[i][j][k]
    
    dicom_read.SeriesNumber = series_number
    dicom_read.SeriesDescription = series_description + '_B' + str(b_value)
    dicom_read.SeriesInstanceUID = series_instance_uid + '_B' + str(b_value)
        
    print str(i) + 'th / ' + str(len(dicom_files_list)) + ' files'      
        
    new_path_and_name = path.join(new_path_dicom, new_name)
    dicom_read.save_as(new_path_and_name)
    


def write_new_dicom_files_ROI(dicom_path, dicom_files_list, series_name, b_value, \
                          im_3d, modified_path, append_name,\
                          max_value_when_its_bool):
 
  new_path_series = path.join(modified_path, series_name) 
  if path.exists(new_path_series):
    pass
  else:
    os.mkdir(new_path_series)
    
  new_path_ini = path.join(new_path_series, 'B_'+str(b_value))
  if path.exists(new_path_ini):
    pass
  else:
    os.mkdir(new_path_ini)  
    
  new_path = path.join(new_path_ini, 'ROIs')
  if path.exists(new_path):
    pass
  else:
    os.mkdir(new_path)
    
  new_path_dicom = path.join(new_path, 'DICOM')
  if path.exists(new_path_dicom):
    pass
  else:
    os.mkdir(new_path_dicom)
    
    
  print 'Saving data in DICOM format ...'
  
  im_3d[im_3d == 1.0] = max_value_when_its_bool
  im_3d = numpy.array(im_3d, dtype='int16')
  
  for i, dicom_file in enumerate(dicom_files_list):
    dicom_read = dicom.read_file(path.join(dicom_path, dicom_file))
    if i == 0:
      series_number = dicom_read.SeriesNumber
      series_description = dicom_read.SeriesDescription
      series_instance_uid = dicom_read.SeriesInstanceUID
    
    if i < 10:
      new_name = '000' + str(i)
    elif i >= 10 and i < 100:
      new_name = '00' + str(i)
    elif i >= 100 and i < 1000:
      new_name = '0' + str(i)
    elif i >= 1000 and i < 10000:
      new_name = str(i)
     
    for j in range(im_3d[0].shape[0]):
      for k in range(im_3d[0].shape[1]):
        dicom_read.pixel_array[j][k] = im_3d[i][j][k]
        
    dicom_read.PixelData = dicom_read.pixel_array.tostring()
    
    dicom_read.SeriesNumber = series_number
    dicom_read.SeriesDescription = series_description + '_B' + str(b_value) +\
                                   'ROIs'
    dicom_read.SeriesInstanceUID = series_instance_uid + '_B' + str(b_value) +\
                                   'ROIs'
        
    print str(i) + 'th / ' + str(len(dicom_files_list)) + ' files'      
        
    new_path_and_name = path.join(new_path_dicom, new_name)
    dicom_read.save_as(new_path_and_name)

      
