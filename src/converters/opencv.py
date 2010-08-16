#!/usr/bin/env python
#
##
## OpenCV-Numpy Data Converter
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#
"""
Module for converting between various image formats and Numpy array.

:func:`image2array`: Convert PIL image to Numpy array.

:func:`cv2array`: Convert OpenCV image to Numpy array.

:func:`array2image`: Convert Numpy array to PIL image.

:func:`array2cv`: Convert Numpy array to OpenCV image.

================================================
OpenCV-Numpy Data Converter function definitions
================================================
"""


import Image
import cv
import numpy


def image2array(im):
  """
  image2array
  
  Convert PIL image to Numpy array.\n  
  Modified from Fredrik Lundh's code of 1998:\n  
  'convert between numerical arrays and PIL image memories'\n  
  (http://effbot.org/zone/pil-numpy.htm)
  """
  
  if im.mode not in ("L", "F"):
    raise ValueError, "can only convert single-layer images"
  if im.mode == "L":
    a = numpy.fromstring(im.tostring(), numpy.uint8)
  else:
    a = numpy.fromstring(im.tostring(), numpy.float32)
  a.shape = im.size[1], im.size[0]
  return a


def cv2array(cv_im):
  """
  cv2array
  
  Convert OpenCV image to Numpy array.

  .. tabularcolumns:: |l|L|

  ==============   ====================================================
  Keyword          Description
  ==============   ====================================================
  cv_im            OpenCV image
  ==============   ====================================================

  returns Numpy array form of the image.  
  """
  
  # I expect cv_im to be a grayscale (CV_LOAD_IMAGE_GRAYSCALE) image.
  pi = Image.fromstring("L", cv.GetSize(cv_im), cv_im.tostring())
  py_im = image2array(pi)
  return py_im


def array2image(a):
  """
  Convert Numpy array to PIL image.\n
  Modified from Fredrik Lundh's code of 1998:\n
  'convert between numerical arrays and PIL image memories'\n
  (http://effbot.org/zone/pil-numpy.htm)
  """
  
  if a.dtype == numpy.uint8:
    mode = "L"
  elif a.dtype == numpy.float32:
    mode = "F"
  else:
    raise ValueError, "unsupported image mode"

  return Image.fromstring(mode, (a.shape[1], a.shape[0]), a.tostring())


def array2cv(py_im):
  """
  array2cv
  
  Convert Numpy array to OpenCV image.

  .. tabularcolumns:: |l|L|

  ==============   ====================================================
  Keyword          Description
  ==============   ====================================================
  py_im            Numpy array form of the image
  ==============   ====================================================

  returns OpenCV form of the image.
  """
  
  pi = array2image(py_im)
  cv_im = cv.CreateImageHeader(pi.size, cv.IPL_DEPTH_8U, 1)
  cv.SetData(cv_im, pi.tostring())
  
  return cv_im


if __name__=='__main__':

  cv_im = cv.LoadImage("contour_test_1.bmp", cv.CV_LOAD_IMAGE_GRAYSCALE)

  # from OpenCV
  py_im = cv2array(cv_im)

  # to OpenCV
  cv_im2 = array2cv(py_im)
  
  
