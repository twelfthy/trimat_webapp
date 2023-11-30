import xml.etree.ElementTree as etree

def get_bndbox(path):

    # Parse the XML file
    xml_file = etree.parse(path)

    # Get the root element
    root = xml_file.getroot()

    # Find the bounding box element
    bbox_elem = root.find(".//bndbox")

    # Extract the bounding box coordinates
    xmin = bbox_elem.findtext("xmin")
    ymin = bbox_elem.findtext("ymin")
    xmax = bbox_elem.findtext("xmax")
    ymax = bbox_elem.findtext("ymax")

    bndbox = ((xmin, ymin), (xmax, ymax))

    # Print the coordinates
    print("Bounding box: ({}, {}, {}, {})".format(xmin, ymin, xmax, ymax))
    return bndbox
