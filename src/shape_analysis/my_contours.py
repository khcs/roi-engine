#! /usr/bin/env python

print "OpenCV Python version of contours"

# import the necessary things for OpenCV
import cv
import numpy

# some default constants
_SIZE = 500
_DEFAULT_LEVEL = 3

# definition of some colors
_red =  (0, 0, 255, 0);
_green =  (0, 255, 0, 0);
_white = cv.RealScalar (255)
_black = cv.RealScalar (0)


# the callback on the trackbar, to set the level of contours we want
# to display
def on_trackbar (position):

    # create the image for putting in it the founded contours
    contours_image = cv.CreateImage ( (_SIZE, _SIZE), 8, 3)

    # compute the real level of display, given the current position
    levels = position - 3

    # initialisation
    _contours = contours
    
    if levels <= 0:
        # zero or negative value
        # => get to the nearest face to make it look more funny
        _contours = contours.h_next().h_next().h_next()
        
    # first, clear the image where we will draw contours
    cv.SetZero (contours_image)
    
    # draw contours in red and green
    cv.DrawContours (contours_image, _contours,
                       _red, _green,
                       levels, 3, cv.CV_AA,
                        (0, 0))

    # finally, show the image
    cv.ShowImage ("contours", contours_image)



if __name__ == '__main__':


    # import the modules -- for test --
    import sys, os
    sys.path.append(os.path.abspath('../'))
    from get_data.dicom_parser import *
    from viewers.show import *
    from segment.automatic_segment import *
    from converters.opencv import *
    

    # create the image where we want to display results
    #image = cv.LoadImage("contour_test_2.bmp", cv.CV_LOAD_IMAGE_GRAYSCALE)
    image = cv.LoadImage("mri_liver_roi.bmp", cv.CV_LOAD_IMAGE_GRAYSCALE)


    # create window and display the original picture in it
    cv.NamedWindow ("image", 1)
    cv.ShowImage ("image", image)

    # create the storage area
    storage = cv.CreateMemStorage (0)
    
    # find the contours
    contours = cv.FindContours(image,
                               storage,
                               cv.CV_RETR_TREE,
                               cv.CV_CHAIN_APPROX_SIMPLE,
                               (0,0))
    
    print contours

    # comment this out if you do not want approximation
    contours_a = cv.ApproxPoly (contours, 
                                storage,
                                cv.CV_POLY_APPROX_DP, 3, 1)
    
    
    
    # create the window for the contours
    #cv.NamedWindow ("contours", 1)

    # create the trackbar, to enable the change of the displayed level
    #cv.CreateTrackbar ("levels+3", "contours", 3, 7, on_trackbar)

    # call one time the callback, so we will have the 1st display done
    #on_trackbar (_DEFAULT_LEVEL)

    # wait a key pressed to end
    #cv.WaitKey (0)
    


    contours_o = cv.FindContours(image,
                               storage,
                               cv.CV_RETR_TREE,
                               cv.CV_CHAIN_APPROX_NONE,
                               (0,0))



    contours_image = cv.CreateImage ( (_SIZE, _SIZE), 8, 1)
    levels = 3
    _contours = contours
    cv.SetZero (contours_image)
    cv.DrawContours (contours_image, _contours, \
                       _white, _white, \
                       levels, 1, cv.CV_AA, \
                        (0, 0))
    cv.ShowImage ("contours", contours_image)
