import numpy as np
import matplotlib
import scipy.io
from PIL import Image, ImageDraw


def read_notes(notes_path, num_objs, labels, bndboxes):

    image_mat = scipy.io.loadmat(notes_path, simplify_cells=True)

    # extract the landmark data
    landmark_data_spine = image_mat['savedfile']['frontal']['coordinates']['spine']
    labels_data_spine = image_mat['savedfile']['frontal']['list']['spine']

    for x in range(18):
        # function for vertebra number:
        vertebra = x*4 + 2
        # set the labels:
        # labels.append(labels_data_spine[vertebra][6:8])
        labels.append(x+1)
        # print(labels)
        # set the coordinates of the box:
        x_min = min(landmark_data_spine[vertebra][0], landmark_data_spine[vertebra+2][0])
        y_min = min(landmark_data_spine[vertebra][1], landmark_data_spine[vertebra+1][1])
        x_max = max(landmark_data_spine[vertebra+1][0], landmark_data_spine[vertebra+3][0])
        y_max = max(landmark_data_spine[vertebra+2][1], landmark_data_spine[vertebra+3][1])

        bbox_coordinates = [x_min, y_min, x_max, y_max]
        bndboxes.append(bbox_coordinates)
        # print(bndboxes)

        # point_1 = (landmark_data_spine[vertebra][0], landmark_data_spine[vertebra][1])
        # point_2 = (landmark_data_spine[vertebra+1][0], landmark_data_spine[vertebra+1][1])
        # point_3 = (landmark_data_spine[vertebra+2][0], landmark_data_spine[vertebra+2][1])
        # point_4 = (landmark_data_spine[vertebra+3][0], landmark_data_spine[vertebra+3][1])
        # bbox_coordinates = [point_1, point_2, point_4, point_3]
        # bndboxes.append(bbox_coordinates)
        # update object count:
        num_objs += 1