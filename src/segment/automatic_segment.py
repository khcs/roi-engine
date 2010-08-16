#!/usr/bin/env python
#
##
## Automatic Segmentation
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#
"""
Module for automatically segmenting a 3D image.

:func:`automatic_segment_n_ROIs_preprocess`: Does preprocessing for automatic\
segmentation for n ROIs.

:func:`automatic_segmentation`: Does automatic segmentation for one ROI at a\
time.

:func:`automatic_segment_n_ROIs_postprocess`: Does postprocessing for automatic\
segmentation for n ROIs. In each automatic_segmentation, only one VOI is obtained.
This function adds all of the VOIs (the number of the VOIs specified by the user.)
to a volume.

:func:`automatic_segmentation_n_ROIs`: Gets 3D image and the number of ROIs to return.
Does an automatic segmentation based on statistics of the 3D image.

:func:`watershed_segment`: Gets (gaussian filtered) 3D image, 3d image with seeds\
(should be 'bool' type) and threshold, and returns segmented 3D image.

:func:`get_threshold`: Gets (gaussian filtered) 3D image, and returns threshold\
for finding ROIs.

:func:`get_3d_image_with_seeds`: Gets (gaussian filtered) 3D image and maximum\
of the 3D iamge and returns 3D image with seeds ('bool' type)

:func:`get_slices_with_seeds`: Currently not used for the `automatic_segmentation`.
Getting only the slices with seeds from the seeds_tuple returned from the \
`get_seeds`. It's actually grouping (segmenting) and categorizing the groups\
and returns only one member of each group from the group.

:func:`get_seeds`: Currently not used for the `automatic_segmentation`.
From a 3d image, it returns seeds tuple and gaussian filtered 3d image.

======================================
automatic_segment function definitions
======================================
"""


import numpy
from numpy import *
import scipy
import pylab
from scipy import ndimage

import pymorph
import mahotas



def get_slices_with_seeds(seeds_tuple):
  """
  get_slices_with_seeds

  .. tabularcolumns:: |l|L|

  ================   ====================================================
  Keyword            Description
  ================   ====================================================
  seeds_tuple        Python tuple with seeds  
  ================   ====================================================

  returns a list of slices with seeds.
  """
  
  slices_tuple = sorted(seeds_tuple[0])
  init = slices_tuple[0]
  slices_with_seeds = [init]
  for i in range(len(slices_tuple)):
    if init != slices_tuple[i]:
      slices_with_seeds.append(slices_tuple[i])
      init = slices_tuple[i]

  return slices_with_seeds



def get_seeds(im_3d_in):
  """
  get_seeds

  .. tabularcolumns:: |l|L|

  ================   ====================================================
  Keyword            Description
  ================   ====================================================
  im_3d_in           3D image to get seeds from
  ================   ====================================================

  returns Python tuple with seeds, and gaussian filtered 3D image::
  
  --{seeds_z_coordinate = seeds_tuple[0]}  
  --{seeds_x_coordinate = seeds_tuple[1]}
  --{seeds_y_coordinate = seeds_tuple[2]}
  """
  
  # convert to uint16
  im_3d_uint = numpy.array(im_3d_in, dtype='uint16')

  # apply gaussian filter
  im_3d_uint_gf_float64 = zeros(im_3d_uint.shape)
  for i in range(im_3d_uint.shape[0]):
      im_3d_uint_gf_float64[i] = ndimage.gaussian_filter(im_3d_uint[i], 1)

  # find maxima
  im_3d_uint_gf_float64_max = im_3d_uint_gf_float64.max()

  # locate the maxima
  im_3d_uint_gf_float64_max_tuple = \
                 numpy.where(im_3d_uint_gf_float64 == im_3d_uint_gf_float64_max)

  # seeds tuple
  seeds_tuple = im_3d_uint_gf_float64_max_tuple

  # gaussian filtered image in uint16
  im_3d_gf_uint16 = numpy.array(im_3d_uint_gf_float64, dtype='uint16')

  return seeds_tuple, im_3d_gf_uint16




def get_3d_image_with_seeds(im_3d_gf_uint16, max):
  """
  get_3d_image_with_seeds

  .. tabularcolumns:: |l|L|

  ================   ====================================================
  Keyword            Description
  ================   ====================================================
  im_3d_gf_uint16    (Gaussian filtered) 3D image in 'uint16' format
  max                Maximum value of the pixels in the image
  ================   ====================================================

  returns 'bool' type 3D image with seeds.
  """
  im_3d_with_seeds = zeros((im_3d_gf_uint16.shape[0], \
                            im_3d_gf_uint16.shape[1], \
                            im_3d_gf_uint16.shape[2]))
  im_3d_with_seeds = numpy.array(im_3d_with_seeds, dtype='bool')

  im_3d_with_seeds[im_3d_gf_uint16 == max] = True

  return im_3d_with_seeds



def get_threshold(im_3d_gf):
  """
  get_threshold

  .. tabularcolumns:: |l|L|

  ================   ====================================================
  Keyword            Description
  ================   ====================================================
  im_3d_gf           (Gaussian filtered) 3D image to get threshold from
  ================   ====================================================

  returns threshold
  """
  
  print 'Computing threshold for ROIs ... '
  T_list = []
  for slice_n in range(len(im_3d_gf)):
    im_3d_gf_slice_n = im_3d_gf[slice_n]
    # filter out the background  
    T_filter_out_background = \
                           mahotas.thresholding.otsu(im_3d_gf_slice_n)
    im_3d_gf_slice_n_bg_suppressed = im_3d_gf_slice_n
    im_3d_gf_slice_n_bg_suppressed[im_3d_gf_slice_n \
                                             <= T_filter_out_background] = 0

    # filter out the region-of-no-interest(RONI)
    im_3d_gf_slice_n_bg_filtered_1d_float64 = \
             zeros(im_3d_gf_slice_n.shape[0] * im_3d_gf_slice_n.shape[1] \
                       - (array(im_3d_gf_slice_n_bg_suppressed) == 0).sum())

    # get the list of foreground pixels
    k = 0
    for i in range(im_3d_gf_slice_n.shape[0]):
      for j in range(im_3d_gf_slice_n.shape[1]):
        if im_3d_gf_slice_n_bg_suppressed[i][j] > 0:
          im_3d_gf_slice_n_bg_filtered_1d_float64[k] = \
                                       im_3d_gf_slice_n_bg_suppressed[i][j]
          k = k + 1

    im_3d_gf_slice_n_bg_filtered_1d_uint16 = \
           numpy.array(im_3d_gf_slice_n_bg_filtered_1d_float64, dtype='uint16')

    T_slice_n = \
              mahotas.thresholding.otsu(im_3d_gf_slice_n_bg_filtered_1d_uint16)
    T_list.append(T_slice_n)

  print '\t\t\t\t... done.'
  T = max(T_list)   

  return T



def watershed_segment(im_3d_gf_uint16, im_3d_with_seeds, T):
  """
  watershed_segmentation

  .. tabularcolumns:: |l|L|

  ================   ====================================================
  Keyword            Description
  ================   ====================================================
  im_3d_gf_uint16    (Gaussian filtered) 3D image (in 'uint16') type.
  im_3d_with_seeds   'bool' type image with seeds.
  T                  Threshold for getting ROIs
  ================   ====================================================

  returns 'bool' type 3D image with ROIs (which is one volume of interest)
  """
  
  print 'Segmentation processing ...'
  dist_3d = ndimage.distance_transform_edt(im_3d_gf_uint16 > T)
  dist_3d = dist_3d.max() - dist_3d
  dist_3d -= dist_3d.min()
  dist_3d = dist_3d/float(dist_3d.ptp()) * 255
  dist_3d = dist_3d.astype(numpy.uint8)

  rois_3d = zeros((dist_3d.shape[0], dist_3d.shape[1], dist_3d.shape[2]))

  for i in range(im_3d_gf_uint16.shape[1]):
    rois_3d[:,i,:] = pymorph.cwatershed(dist_3d[:,i,:], im_3d_with_seeds[:,i,:])

  for i in range(im_3d_gf_uint16.shape[2]):
    rois_3d[:,:,i] = pymorph.cwatershed(dist_3d[:,:,i], im_3d_with_seeds[:,:,i])

  for i in range(len(dist_3d)):
    rois_3d[i] = pymorph.cwatershed(dist_3d[i], rois_3d[i])

  print '\t\t\t... done.'

  return rois_3d



def automatic_segment_n_ROIs_preprocess(im_3d):
  """
  automatic_segment_n_ROIs_preprocess

  .. tabularcolumns:: |l|L|

  ==============   ====================================================
  Keyword          Description
  ==============   ====================================================
  im_3d            3D image to segment
  ==============   ====================================================

  returns threshold T, gaussian filtered image im_3d_gf_uint16, and
  preallocated 3d 'bool' type image with ROIs.
  """
  
  rois_3d = zeros((im_3d.shape[0], im_3d.shape[1], im_3d.shape[2]))
  rois_3d = numpy.array(rois_3d, dtype='float64')

  # apply gaussian filter
  im_3d_gf_uint16 = zeros(im_3d.shape)
  im_3d_gf_uint16 = numpy.array(im_3d, dtype='uint16')
  for i in range(im_3d.shape[0]):
      im_3d_gf_uint16[i] = ndimage.gaussian_filter(im_3d_gf_uint16[i], 1)

  # conver the gaussian filtered image to uint16 type
  im_3d_gf_uint16 = numpy.array(im_3d_gf_uint16, dtype='uint16')  

  # get the threshold
  T = get_threshold(im_3d_gf_uint16)

  return T, im_3d_gf_uint16, rois_3d



def automatic_segmentation(im_3d_gf_uint16, T):
  """
  automatic_segmentation

  .. tabularcolumns:: |l|L|

  ===============   ====================================================
  Keyword           Description
  ===============   ====================================================
  im_3d_gf_uint16   Gaussian filtered 'uint16' type 3D image.
  T                 Threshold for segmentation.
  ===============   ====================================================

  returns 3D 'boolean' image with ROIs (one VOI).
  """
  
  # get the image with seed points
  im_3d_with_seeds = get_3d_image_with_seeds(im_3d_gf_uint16, \
                                             im_3d_gf_uint16.max())

  rois_3d = watershed_segment(im_3d_gf_uint16, im_3d_with_seeds, T)

  return rois_3d



def automatic_segment_n_ROIs_postprocess(rois_3d, rois_3d_current, \
                                         im_3d_gf_uint16):
  """
  automatic_segment_n_ROIs_postprocess

  Adds n ROIs (actually VOIs) to a volume.

  .. tabularcolumns:: |l|L|

  ===============   ====================================================
  Keyword           Description
  ===============   ====================================================
  rois_3d           3D 'boolean' image with ROIs
  rois_3d_current   3D 'boolean' image with the ROIs (one VOI) just previously\
                    segmented
  im_3d_gf_uint16   Gaussian filtered 3D 'uint16' type image
  ===============   ====================================================

  returns gaussian filtered 3D 'uint16' type image, 3D 'boolean' image with ROIs.
  """

  # add the result of the current segmentation to the 3D image with previous
  # ROIs
  rois_3d = rois_3d + rois_3d_current
    
  # for getting the next ROI
  rois_pixels = numpy.where(rois_3d == 1.0)

  rois_z = rois_pixels[0]
  rois_x = rois_pixels[1]
  rois_y = rois_pixels[2]

  for j in range(len(rois_z)):
      im_3d_gf_uint16[rois_z[j], rois_x[j], rois_y[j]] = 0

  return im_3d_gf_uint16, rois_3d



def automatic_segmentation_n_ROIs(im_3d, num_ROIs):
  """
  automatic_segmentation_n_ROIs

  .. tabularcolumns:: |l|L|

  ==============   ====================================================
  Keyword          Description
  ==============   ====================================================
  im_3d            3D image to segment
  num_ROIs         Number of ROIs to find
  ==============   ====================================================

  ...
  returns nothing yet ...
  """

  # automatic segmentation pre-processing
  T, im_3d_gf_uint16, rois_3d = automatic_segment_n_ROIs_preprocess(im_3d)

  # do the segmentation for n ROIs
  for i in range(num_ROIs):

    # automatic segmentation
    rois_3d_current = automatic_segmentation(im_3d_gf_uint16, T)

    # automatic segmentation post-processing
    im_3d_gf_uint16, rois_3d = automatic_segment_n_ROIs_postprocess(rois_3d, \
                                                             rois_3d_current, \
                                                             im_3d_gf_uint16)
    

  ### show the images
  images_in_a_row = attach_images(im_3d, rois_3d)
  show_image(images_in_a_row)




if __name__=='__main__':

  # import the get_data  -- for test --
  import sys, os
  sys.path.append(os.path.abspath('../'))
  from get_data.dicom_parser import *
  from viewers.show import *
  import filters

  # read and show the image
  #dicom_path_input = raw_input('Enter the directory path to read the DICOM files from:')
  dicom_path_input = \
                   '/Users/hshin/Works/PhD/Dataset/ICR/cvehlow/Liver_Pat3/DICOM/'
  study_structure_get = read_dicom_files(dicom_path_input)
  series_name_get = study_series_selector(study_structure_get)
  im_3d, pixel_spaceing, slice_thickness = \
              get_image(dicom_path_input, study_structure_get, series_name_get)
  #show_image(im_3d)


  automatic_segmentation_n_ROIs(im_3d, 8)


  

