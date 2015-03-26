# Introduction #

The project is aiming for search engine (like [Google](http://www.google.com) for Regions of Interest (ROIs) in medical images.


# Features #

  * A user connects to the server with a web-browser, as like they connect to [Google](http://www.google.com).

![https://lh6.googleusercontent.com/_bMwkuo210r8/TZxrY5PKLKI/AAAAAAAAAC0/-UPxFXmwN_E/s640/MainPage.png](https://lh6.googleusercontent.com/_bMwkuo210r8/TZxrY5PKLKI/AAAAAAAAAC0/-UPxFXmwN_E/s640/MainPage.png)

  * Upload a series of medical images in compressed [DICOM](http://en.wikipedia.org/wiki/DICOM) format.

![https://lh5.googleusercontent.com/_bMwkuo210r8/TZxrZHAs4LI/AAAAAAAAAC8/9MjscXRTElM/s640/UploadFiles.png](https://lh5.googleusercontent.com/_bMwkuo210r8/TZxrZHAs4LI/AAAAAAAAAC8/9MjscXRTElM/s640/UploadFiles.png)

  * The engine finds all the study-series in the uploaded files. Choose one to proceed, and say how many ROIs you want the engine to find for you.

![https://lh6.googleusercontent.com/_bMwkuo210r8/TZxrYhTfjgI/AAAAAAAAAC4/BPxMF3gHlO0/s640/SelectSeries.png](https://lh6.googleusercontent.com/_bMwkuo210r8/TZxrYhTfjgI/AAAAAAAAAC4/BPxMF3gHlO0/s640/SelectSeries.png)

  * It finds N (the number you gave) number of ROIs in the study series, ranking from the most brightest region to the Nth least brightest region. It uses [region growing segmentation](http://en.wikipedia.org/wiki/Region_growing) to do the 3D segmentation of the regions.

![https://lh3.googleusercontent.com/_bMwkuo210r8/TZxsQZptL_I/AAAAAAAAADQ/gBalZ8EQiR8/s720/SearchResult.png](https://lh3.googleusercontent.com/_bMwkuo210r8/TZxsQZptL_I/AAAAAAAAADQ/gBalZ8EQiR8/s720/SearchResult.png)

  * You select one and download the XML file containing the coordinates of the ROIs and name of the files containing them.

  * When you have [Apache Tomcat](http://tomcat.apache.org/) installed correctly, specified $TOMCAT shell variable correctly and have [installed the documentation](http://code.google.com/p/roi-engine/wiki/InstallationAndUsage#Install) with the script provided in the /doc of the source code, [Sphinx](http://sphinx.pocoo.org/) powered documentation server is hosted as well.

![https://lh6.googleusercontent.com/_bMwkuo210r8/TZxsQcKYe4I/AAAAAAAAADM/q0aX1R8Ih7Q/s640/Documentation.png](https://lh6.googleusercontent.com/_bMwkuo210r8/TZxsQcKYe4I/AAAAAAAAADM/q0aX1R8Ih7Q/s640/Documentation.png)

  * in the /shape\_analysis there are scripts/programs for
  1. find ROIs and visualize with [VTK](http://www.vtk.org/), select one and
  1. do surface extraction and visualize with [VMTK](http://www.vmtk.org)/[VTK](http://www.vtk.org/)
  1. do contour estimation with [OpenCV](http://opencv.willowgarage.com/wiki/) and visualize it with [VTK](http://www.vtk.org/)

![https://lh6.googleusercontent.com/_bMwkuo210r8/TZxva1fCIqI/AAAAAAAAADY/UKJ3ueKL7j0/s720/application-example-no-server.png](https://lh6.googleusercontent.com/_bMwkuo210r8/TZxva1fCIqI/AAAAAAAAADY/UKJ3ueKL7j0/s720/application-example-no-server.png)