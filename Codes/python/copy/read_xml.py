import xml.etree.ElementTree as ET

file_name = '/home/ogianoli/Code/cazzate/4_points_recognition/trainset/02_Annotations/File0{}.xml'
# Parse the XML file
for i in range(51):
    new_file_name = file_name.format(f"{i:02d}")

    tree = ET.parse(new_file_name)
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