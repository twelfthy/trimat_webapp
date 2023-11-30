import xml.etree.ElementTree as ET

file_name = '/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/4_points_recognition/testset/02_Annotations/File000.xml'
# Parse the XML file
tree = ET.parse(file_name)
root = tree.getroot()

# Extract the bounding box coordinates
x_min = int(root.find('object/bndbox/xmin').text)
y_min = int(root.find('object/bndbox/ymin').text)
x_max = int(root.find('object/bndbox/xmax').text)
y_max = int(root.find('object/bndbox/ymax').text)

# Print the bounding box coordinates
bbox_coordinates = [x_min, y_min, x_max, y_max]
print(f'Bounding box: ({bbox_coordinates})')


# bndboxes.append(bbox_coordinates)