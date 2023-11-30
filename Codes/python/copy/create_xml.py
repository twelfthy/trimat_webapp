from PIL import Image, ImageDraw, ImageOps
import xml.etree.ElementTree as ET
import cv2
import numpy as np
import skimage
import xml.dom.minidom as md
import os

root_path = '/home/ogianoli/Code/cazzate/4_points_recognition/trainset'
subpath1 = '01_Images'
subpath2 = '02_Annotations'
path_extension_jpg = 'Image{:03d}.jpg'
path_extension_xml = 'File{:03d}.xml'
for k in range(51):
    filename = path_extension_jpg.format(k)
    print("\nfilename: ",filename)
    img_path = os.path.join(root_path, subpath1, filename)
    # Load the image
    img = Image.open(img_path)

    # Convert the image to HSV format
    hsv_img = img.convert("HSV")

    # Define the blue color range in HSV format
    lower_blue = (100, 155, 100)
    upper_blue = (190, 255, 255)
    threshold = 100

    # Threshold the image to create a binary mask of the blue pixels

    # print(hsv_img.getpixel((0,0)))
    w, h = hsv_img.size
    # print("size",w,h)
    numpy_array = np.array(hsv_img)

    for i in range(h-1):
        for j in range(w-1):
            pixel = numpy_array[i][j]
            if (pixel[0] > lower_blue[0] and pixel[1] > lower_blue[1] and pixel[2] > lower_blue[2] and pixel[0] < upper_blue[0] and pixel[1] < upper_blue[1] and pixel[2] < upper_blue[2]):
                numpy_array[i][j] = 255
            else: 
                numpy_array[i][j] = 0
    # Invert the mask to get the non-blue pixels
    blue_mask = Image.fromarray(numpy_array)
    blue_mask = blue_mask.convert("L")
    blue_mask.save('/home/ogianoli/Code/cazzate/4_points_recognition/trainset/03_Results/Mask.jpg')
    non_blue_mask = ImageOps.invert(blue_mask)
    binary_mask = non_blue_mask.point(lambda x: 255 if x > threshold else 0, mode='1')

    # Find the contours of the non-blue area
    contours = skimage.measure.find_contours(np.array(binary_mask), 0.5)
    min_row, min_col, max_row, max_col = binary_mask.getbbox()
    print("corners: ", min_row, min_col, max_row, max_col)

    # Draw the bounding box on the original image
    draw = ImageDraw.Draw(img)
    draw.rectangle((min_row, min_col, max_row, max_col), outline="green", width=2)
    img.save('/home/ogianoli/Code/cazzate/4_points_recognition/trainset/03_Results/Image_with_bbox.png')

    # Create the XML file
    root = ET.Element("annotation")
    folder = ET.SubElement(root, "folder")
    folder.text = "."
    filename = ET.SubElement(root, "filename")
    filename.text = "Image01.jpg"
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(img.size[0])
    height = ET.SubElement(size, "height")
    height.text = str(img.size[1])
    depth = ET.SubElement(size, "depth")
    depth.text = str(3)  # assuming RGB image
    xmin_value = min_row
    ymin_value = min_col
    xmax_value = max_row
    ymax_value = max_col
    object_ = ET.SubElement(root, "object")
    name = ET.SubElement(object_, "name")
    name.text = "non-blue area"
    bndbox = ET.SubElement(object_, "bndbox")
    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = str(xmin_value)
    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = str(ymin_value)
    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = str(xmax_value)
    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = str(ymax_value)
    # Save the XML file
    xml_filename = path_extension_xml.format(k)
    print("filename: ",xml_filename)
    xml_path = os.path.join(root_path, subpath2, xml_filename)
    ET.ElementTree(root).write(xml_path)