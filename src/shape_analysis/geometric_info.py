#!/usr/bin/env python
#
##
## Geometric Info
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#
"""
Module for geometric analysis on ROIs.

:func:`get_boundary`: Get the boundary of the ROI (region).

:func:`get_center_of_mass_VOI_for_coordinate`: Get the Center of Mass for VOI
for a coordinate ('x', 'y', or 'z').

:func:`get_center_of_mass_VOI`: Get the Center of the Mass for the VOI. Returns
the Center of the Mass in (x,y,z)-coordinate.

:func:`fill_lost_z_slices_in_3d_roi`: (More work might be needed to be done on
this and related functions...). For 3D polynomial approximation and interpolation,
it fills the gap between the slices filling (for now) just blank slices, with the
numbers of the slices corresponding to the (approximated) MRI slice thickness.

:func:`b_spline_approx`: Does B-Spline polynomial approximation on those given
control points.

:func:`draw_b_spline_approx`: Draws the result of the B-Spline polynomial
approximation on each coordinate view.

===================================
geometric_info function definitions
===================================
"""



import cv
import numpy
from numpy import *

from scipy.signal import cspline1d, cspline1d_eval
from scipy import ogrid, sin, mgrid, ndimage, array
from numpy import arange, cos, linspace, pi, sin, random
from scipy.interpolate import splprep, splev

import pylab

import sys, os
sys.path.append(os.path.abspath('../'))
from converters.opencv import *


def get_boundary(rois_3d, approx_level=None):
  """
  get_boundary

  .. tabularcolumns:: |l|L|

  ================  ============================================================
  Keyword           Description
  ================  ============================================================
  rois_3d           3D (can be also 2D though) image (volume) with ROI to
                    extract boundary from.
  approx_level      Level of approximation for the contour approximation of the
                    ROI boundary. When 'Simple' it approximates the original
                    boundary with about the half of the original number of the
                    boundary pixels and draws contour between those approximated
                    points, and when it's 'Poly' it approximates the original
                    boundary with about the 1/10 of the original number of the
                    boundary pixels and draws polygon between them.
  ================  ============================================================

  returns 3D (or 2D) image with extracted boundaries, and list of the
   (approximated) contour points of the boundaries.
  """
  
  # ROIs Boundary
  rois_3d_boundary = zeros(rois_3d.shape)
  contours_list = []

  _white = cv.RealScalar (255)
  _SIZE_h = rois_3d.shape[2]
  _SIZE_v = rois_3d.shape[1]
  levels = 3
  line_width = 1

  contours_image = cv.CreateImage((_SIZE_h, _SIZE_v), 8, 1)
  storage = cv.CreateMemStorage()
  for i in range(len(rois_3d)):    
    image_cv = array2cv(numpy.array(rois_3d[i], dtype='uint8'))

    if approx_level == 'Simple' or approx_level == 'Poly':
      contours = cv.FindContours(image_cv, storage, \
                                 cv.CV_RETR_TREE, \
                                 cv.CV_CHAIN_APPROX_SIMPLE, (0,0))
    else:
      contours = cv.FindContours(image_cv, storage, \
                                 cv.CV_RETR_TREE, \
                                 cv.CV_CHAIN_APPROX_NONE, (0,0))

    if approx_level == 'Poly':
      contours_array = numpy.asarray(contours)
      if len(contours_array) > 0:
        contours = cv.ApproxPoly(contours, storage, \
                                 cv.CV_POLY_APPROX_DP, 3, 1)

  
    cv.SetZero(contours_image)
    cv.DrawContours(contours_image, contours, _white, _white, levels, \
                    line_width, cv.CV_AA, (0, 0))

    contours_image_py = cv2array(contours_image)
    rois_3d_boundary[i] = contours_image_py

    contours_list.append(contours)

  del contours
  del contours_image

  return rois_3d_boundary, contours_list
    


def get_center_of_mass_VOI_for_coordinate(rois_3d, coordinate):
  """
  get_center_of_mass_VOI_for_coordinate

  .. tabularcolumns:: |l|L|

  ==============  ==============================================================
  Keyword         Description
  ==============  ==============================================================
  rois_3d         3D ROI volume to get the center of mass.
  coordinate      Coordinate of the center of the mass to get.
  ==============  ==============================================================

  returns center of the mass in the required coordinate.
  """
  
  elements_init = 0
  elements = []

  if coordinate == 'Z' or coordinate == 'z':
    coordinate_num = 0
  elif coordinate == 'Y' or coordinate == 'y':
    coordinate_num = 1
  elif coordinate == 'X' or coordinate == 'x':
    coordinate_num = 2
  else:
    print 'Wrong coordinate value given.'
    raise ValueError
    
  coordinate_array_len = rois_3d.shape[coordinate_num]
  _c_len = coordinate_array_len
  _c_num = coordinate_num
  

  for i in range(_c_len):
      
    if _c_num == 0:
      i_slice = rois_3d[i]
    elif _c_num == 1:
      i_slice = rois_3d[:,i,:]
    else:
      i_slice = rois_3d[:,:,i]


    elements_before_i = 0
    elements_after_i = 0
    
    for j in range(i):

      if _c_num == 0:
        j_left_slice = rois_3d[j]
        j_right_slice = rois_3d[_c_len - j - 1]
      elif _c_num == 1:
        j_left_slice = rois_3d[:,j,:]
        j_right_slice = rois_3d[:, _c_len - j - 1, :]
      else:
        j_left_slice = rois_3d[:,:,j]
        j_right_slice = rois_3d[:, :, _c_len - j - 1]

      elements_before_i += len(j_left_slice[j_left_slice == 1.0])
      elements_after_i += len(j_right_slice[j_right_slice == 1.0])

    elements_after_i -= elements_before_i

    if elements_before_i > elements_after_i:
      break

  com_coordinate = i - 1

  return com_coordinate
  


def get_center_of_mass_VOI(rois_3d):
  """
  get_center_of_mass_VOI

  .. tabularcolumns:: |l|L|

  ==============  ==============================================================
  Keyword         Description
  ==============  ==============================================================
  rois_3d         3D ROI volume to get the center of the mass from.
  ==============  ==============================================================

  returns the center of the mass in (x,y,z) coordinate.
  """
  
  com_z = get_center_of_mass_VOI_for_coordinate(rois_3d, 'Z')
  com_y = get_center_of_mass_VOI_for_coordinate(rois_3d, 'Y')
  com_x = get_center_of_mass_VOI_for_coordinate(rois_3d, 'X')
  
  return com_z, com_y, com_x



def fill_lost_z_slices_in_3d_roi(rois_3d, pixel_spacing, slice_thickness):
  """
  fill_lost_z_slices_in_3d_roi

  .. tabularcolumns:: |l|L|

  ===============  =============================================================
  Keyword          Description
  ===============  =============================================================
  rois_3d          3D ROI volume to fill the slices in.
  pixel_spacing    pixel_spacing of the original DICOM files.
  slice_thickness  slice_thickness of the original DICOM files.
  ===============  =============================================================

  returns 3D image volume with between the original slices filled corresponding
   to the slice thickness
  """
  
  z_inter = int(floor(slice_thickness/ \
                      ((pixel_spacing[0] + pixel_spacing[1])/2) \
                     )
               )

  rois_3d_lost_z_filled = zeros((len(rois_3d) * z_inter, rois_3d.shape[1], \
                                 rois_3d.shape[2]), dtype='int16')

  j = 0
  for i in range(len(rois_3d) * z_inter):
    if i % z_inter == 0:
      rois_3d_lost_z_filled[i] = rois_3d[j]
      j += 1

  return rois_3d_lost_z_filled



def b_spline_approx(contours_list):
  """
  b_spline_approx

  .. tabularcolumns:: |l|L|

  ===============  =============================================================
  Keyword          Description
  ===============  =============================================================
  contours_list    list of points to approximate B-Spline from.
  ===============  =============================================================

  returns original x, y, z of the contours_list and the new B-Spline
  interpolated and approximated xnew, ynew, znew.
  """
  
  x = []
  y = []
  z = []
  for i in range(len(contours_list)):
    contours_list_i_array = numpy.asarray(contours_list[i])
    for j in range(len(contours_list_i_array)):
      x.append(contours_list_i_array[j][0])
      y.append(contours_list_i_array[j][1])
      z.append(i * 4)

  x_a = numpy.asarray(x)
  y_a = numpy.asarray(y)
  z_a = numpy.asarray(z)

  # add noise
  x_a += random.normal(scale=0.1, size=x_a.shape)
  y_a += random.normal(scale=0.1, size=y_a.shape)
  z_a += random.normal(scale=0.1, size=z_a.shape)

  # spline parameters
  s=3.0 # smoothness parameter
  k=2 # spline order
  nest=-1 # estimate of number of knots needed (-1 = maximal)

  # find the knot points
  tckp,u = splprep([x,y,z],s=s,k=k,nest=-1)

  # evaluate spline, including interpolated points
  xnew,ynew,znew = splev(linspace(0,1,400),tckp)

  return x, y, z, xnew, ynew, znew



def draw_b_spline_approx(contours_list, rois_3d, \
                         pixel_spacing, slice_thickness):
  """
  draw_b_spline_approx

  .. tabularcolumns:: |l|L|

  ===============  =============================================================
  Keyword          Description
  ===============  =============================================================
  contours_list    List of points to approximate B-Spline from.
  rois_3d          3D ROI volume. Used just for reference to have shape of the
                   volume.
  pixel_spacing    pixel_spacing of the original DICOM files.
  slice_thickness  slice_thickness of the original DICOM files.
  ===============  =============================================================
  """

  z_inter = int(floor(slice_thickness/ \
                      ((pixel_spacing[0] + pixel_spacing[1])/2) \
                     )
               )

  rois_3d_lost_z_filled = zeros((len(rois_3d) * z_inter, rois_3d.shape[1], \
                                 rois_3d.shape[2]), dtype='int16')
  

  x, y, z, xnew, ynew, znew = b_spline_approx(contours_list)

  pylab.subplot(2,2,1)
  data,=pylab.plot(x,y,'bo-',label='data')
  fit,=pylab.plot(xnew,ynew,'r-',label='fit')
  pylab.legend()
  pylab.xlabel('x')
  pylab.ylabel('y')

  pylab.subplot(2,2,2)
  data,=pylab.plot(x,z,'bo-',label='data')
  fit,=pylab.plot(xnew,znew,'r-',label='fit')
  pylab.legend()
  pylab.xlabel('x')
  pylab.ylabel('z')

  pylab.subplot(2,2,3)
  data,=pylab.plot(y,z,'bo-',label='data')
  fit,=pylab.plot(ynew,znew,'r-',label='fit')
  pylab.legend()
  pylab.xlabel('y')
  pylab.ylabel('z')




if __name__=='__main__':
    
  # import the modules -- for test --
  import sys, os
  sys.path.append(os.path.abspath('../'))
  from get_data.dicom_parser import *
  from viewers.show import *
  from segment.automatic_segment import *
  from converters.opencv import *

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

    # extract Boundary
    rois_3d_boundary, contours_list = get_boundary(rois_3d_current)

    # extract Boundary approx 1
    rois_3d_boundary_approx_1, contours_list_approx_1 = \
                               get_boundary(rois_3d_current, 'Simple')

    # extract Boundary poly approx
    rois_3d_boundary_approx_poly, contours_list_approx_poly = \
                               get_boundary(rois_3d_current, 'Poly')
    
    # automatic segmentation post-processing
    im_3d_gf_uint16, rois_3d = automatic_segment_n_ROIs_postprocess(rois_3d, \
                                                             rois_3d_current, \
                                                             im_3d_gf_uint16)

    com_z, com_y, com_x = get_center_of_mass_VOI(rois_3d_current)

    draw_b_spline_approx(contours_list_approx_poly, rois_3d_current, \
                                              pixel_spacing, slice_thickness)
    

  #for i in range(len(contours_list)):
  #  contours = numpy.asarray(contours_list[i])
  #  print len(contours)
