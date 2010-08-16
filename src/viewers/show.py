#!/usr/bin/env python
#
##
## Image Viewers (Show)
## Hoo Chang Shin
## E-Mail: hoo.shin@icr.ac.uk
##
#
"""
Module for showing images

:func:`show_image`: Show the 3D image in a series of 2D image slices.

:func:`attach_images`: Gets two images and attach them to one image to show to\
the user in one window.

==================================
show function definitions
==================================
"""



import os
from os import path
import pylab
import numpy
from numpy import *



def show_image(im_3d_in):
  """
  show_image

  .. tabularcolumns:: |l|L|

  ===================   ====================================================
  Keyword               Description
  ===================   ====================================================
  im_3d_in              3D image array returned from the :func:`get_image`
  ===================   ====================================================

  On user input:
  'Enter': show the next slice.
  'p'    : show the previous slice.
  'q'    : quit the viewer.

  Does not return anything.
  """
  
  i=1
  while True:
    im_2d = im_3d_in[i-1]
    pylab.imshow(im_2d)
    pylab.gray()

    if i == 1:
      print 'Beginning of the 3D image slices.'
    elif i == len(im_3d_in):
      i = 1
    elif i == 0:
      i = len(im_3d_in)
    else:
      pass

    print 'Slice Number: ', i, '/', len(im_3d_in)

    navigate = \
     raw_input('press Enter to view the next image, \
p to view the previous, q to quit: ')

    if navigate == 'p':
      i = i-1
    elif navigate == 'q':
      break
    else:
      i = i + 1



def attach_images(im_3d_1, im_3d_2):
  """
  attach_images

  .. tabularcolumns:: |l|L|

  ================   ====================================================
  Keyword            Description
  ================   ====================================================
  im_3d_1            3D image to attach first (on the left)
  im_3d_2            3D image to attach second (on the right)
  ================   ====================================================

  returns two 3D images attached in a row
  """
  im_3d_3 = zeros((im_3d_1.shape[0], im_3d_1.shape[1], \
                   im_3d_1.shape[2] + im_3d_2.shape[2]))
  
  if im_3d_2.dtype == 'bool':
    im_3d_2_uint16 = numpy.array(im_3d_2, dtype='uint16')
    im_3d_2_uint16[im_3d_2 == True] = im_3d_1.max()
    im_3d_2 = im_3d_2_uint16
  elif im_3d_2.dtype == 'float64':
    im_3d_2_uint16 = numpy.array(im_3d_2, dtype='uint16')
    im_3d_2_uint16[im_3d_2 >= 1] = im_3d_1.max()
    im_3d_2 = im_3d_2_uint16
  
  for i in range(len(im_3d_1)):
    im_3d_3[i,:,:] = hstack((im_3d_1[i,:,:], im_3d_2[i,:,:]))

  return im_3d_3
