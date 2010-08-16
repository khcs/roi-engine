

from Slicer import slicer
import pylab


# Yes, I've loaded the data in the Slicer
nodes = slicer.ListVolumeNodes()


# Yes, they are the volume names saved
image_3d_origin = nodes['05608611']
image_3d_label = nodes['05608611-label']
image_3d_srg_segment = nodes['Robust Statistics Segmentation Volume']


# Convert the volumes to the Numpy arrays
image_3d_origin_data = image_3d_origin.GetImageData().ToArray()
image_3d_label_data = image_3d_label.GetImageData().ToArray()
image_3d_srg_segment_data = image_3d_srg_segment.GetImageData().ToArray()


# Get some ideas about how the arrays look like
print('size(image_3d_origin_data):', image_3d_origin_data.shape)
print('size(image_3d_label):', image_3d_label.shape)
print('size(image_3d_segment):', image_3d_srg_segment.shape)

print('type(image_3d_origin_data):', image_3d_origin_data.dtype)
print('type(image_3d_label):', image_3d_label.dtype)
print('type(image_3d_segment):', image_3d_srg_segment.dtype)


# Do an automatic watershed segmentation and compare

