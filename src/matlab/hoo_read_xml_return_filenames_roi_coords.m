function [directory_location, filenames, roi_coords_x, roi_coords_y] = ...
    hoo_read_xml_return_filenames_roi_coords(xml_file)


% Load my Java class for manipulating the XML files
parseResultManipulator = ParseDICOM.ManipulateDICOMparseResult;

directory_location_java = parseResultManipulator.readFromXML_directory_location(xml_file, 1);
directory_location = char(directory_location_java);

filenames_java = parseResultManipulator.readFromXML(xml_file, 1);
filenames = char(filenames_java);

roi_coords_java = parseResultManipulator.readFromXML_roi_coordinates(xml_file, 1);
for i=1:length(roi_coords_java)
    roi_coords(i,:) = char(roi_coords_java(i));
    roi_coords_strreadable = strrep(char(roi_coords_java(i)), '(', ' ');
    roi_coords_strreadable = strrep(roi_coords_strreadable, ')', ' ');
    roi_coords_strreadable = strrep(roi_coords_strreadable, ',', ' ');
    [x(i,:), y(i,:)] = strread(roi_coords_strreadable, '%f %f');
end

roi_coords_x = x;
roi_coords_y = y;
