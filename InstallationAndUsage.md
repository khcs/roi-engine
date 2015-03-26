# Installation #

## Dependencies ##

Currently there are ridiculously many dependencies you need to install first. It will be reduced in the future. Currently the web-version uses [MATLAB](http://www.mathworks.com/products/matlab/) for some image manipulation, but it was used for fast implementation and will be independent of it pretty soon.

  * The main implementation language is [Python](http://www.python.org/) (was tested on 2.6)
  * The web server is powered by [CherryPy](http://www.cherrypy.org/)
  * [Genshi](http://genshi.edgewall.org/) for web templates.
  * [Numpy](http://numpy.scipy.org/) and [Scipy](http://www.scipy.org/) for some numerical operations.
  * [PyDicom](http://code.google.com/p/pydicom/) for [DICOM](http://en.wikipedia.org/wiki/DICOM) file handling.
  * [OpenCV](http://opencv.willowgarage.com/wiki/) for additional image processing and geometric analysis.
  * [PIL](http://www.pythonware.com/products/pil/) for converting [Numpy](http://numpy.scipy.org/) array (obtained from [PyDicom](http://code.google.com/p/pydicom/)) to [OpenCV](http://opencv.willowgarage.com/wiki/) format and vice versa.
  * [Pylab](http://sourceforge.net/projects/pylab/), [lxml](http://lxml.de/), [pymorph](http://www.mmorph.com/pymorph/), [mahotas](http://pypi.python.org/pypi/mahotas) Python packages for segmentation, XML handling, etc.
  * [VTK](http://www.vtk.org/), [ITK](http://www.itk.org/), [VMTK](http://www.vmtk.org/) for some medical image processing and visualizing.
  * [CMake](http://www.cmake.org/) to build some of them above.
  * [Sphinx](http://sphinx.pocoo.org/) for building documentation pages.
  * [Apache Tomcat](http://tomcat.apache.org/) to host the documentation pages.
  * [MATLAB](http://www.mathworks.com/products/matlab/) (yeah, I know. putting an expensive commercial software here makes the whole thing quite lame. though currently [MATLAB](http://www.mathworks.com/products/matlab/) doesn't do anything fancy or important, but just basic image manipulation. it was only used for fast implementation. can be replaced by pretty much anything - e.g. [OpenCV](http://opencv.willowgarage.com/wiki/), [PIL](http://www.pythonware.com/products/pil/), ...)


## Install ##

  * no need to install. just run the Python script.
  * to host the documentation server:
  1. set $TOMCAT shell variable pointing to the directory where your [Apache Tomcat](http://tomcat.apache.org/) is locating.
  1. then
```
$ cd /doc/sphinx
$ ./my-build-script
```


## Usage ##

  * to run the search-engine web-server:
```
$ cd /src/webserver
$ python starter.py
```
  1. then connect to 'your-local-ip-address':9090 using a web-browser.

  * to use without web server and see the result with [VTK](http://www.vtk.org/) & interact with shell:
  1. read the documents & codes and run the corresponding python scripts...