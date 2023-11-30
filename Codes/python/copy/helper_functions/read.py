import xml.etree.ElementTree as ET
import time


def read_notes(notes_path, num_objs, labels, bndboxes):
    tree = ET.parse(notes_path)
    # print(notes_path)
    root = tree.getroot()
    labels.append(1)
    # Extract the bounding box coordinates
    x_min = int(root.find('object/bndbox/xmin').text)
    y_min = int(root.find('object/bndbox/ymin').text)
    x_max = int(root.find('object/bndbox/xmax').text)
    y_max = int(root.find('object/bndbox/ymax').text)

    # Print the bounding box coordinates
    bbox_coordinates = [x_min, y_min, x_max, y_max]
    # print(f'Bounding box: ({bbox_coordinates})')
    bndboxes.append(bbox_coordinates)
    # num_objs += 1
    time.sleep(0.1)