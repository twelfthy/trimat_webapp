import torch
from training import Points_Dataset, get_transform, get_model_instance_segmentation
import torch
from PIL import Image, ImageDraw
import cv2
import random
from create_prediction import create_prediction, three_in_1

treshold = 0.3


# CONSTANTS:
# results path:
imgSaveDir = '/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/copy/Results/result_image.png'
bboxes_imageDir = '/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/copy/Results/results'

# setting DEVICE:
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)
# defining the MODEL:
num_classes = 2
model = get_model_instance_segmentation(num_classes)
model.load_state_dict(torch.load('/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/copy/model_weights.pth', map_location=torch.device('cpu')))
model.to(device)
# put the model in evaluation mode
model.eval()
# defining the DATASET:
dataset_test = Points_Dataset('/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/copy/trainset', get_transform(train=False))
# pick one image from the test set
# random_number = [random.randint(0,50), random.randint(0,50), random.randint(0,50)]
# print("images selected: ", random_number[0],", ", random_number[1],", ", random_number[2])
# use the following 3 lines if using the big given testset.
# img1, _ = dataset_test[random_number[0]]
# img2, _ = dataset_test[random_number[1]]
# img3, _ = dataset_test[random_number[2]]
# use the following 3 lines if using the custom testset.
img1, _ = dataset_test[7]
print(type(img1))
# img2, _ = dataset_test[1]
# img3, _ = dataset_test[2]
# create a PREDICTION
create_prediction(device, model, img1, bboxes_imageDir, treshold).save(bboxes_imageDir + '1' + '.png')
# create_prediction(device, model, img2, bboxes_imageDir, treshold).save(bboxes_imageDir + '2' + '.png')
# create_prediction(device, model, img3, bboxes_imageDir, treshold).save(bboxes_imageDir + '3' + '.png')
print(img1.size())
# size1 = [img1.size()[2], img1.size()[1]]
# size2 = [img2.size()[2], img1.size()[1]]
# size3 = [img3.size()[2], img1.size()[1]]
img1 = create_prediction(device, model, img1, bboxes_imageDir, treshold)
# img2 = create_prediction(device, model, img2, bboxes_imageDir, treshold)
# img3 = create_prediction(device, model, img3, bboxes_imageDir, treshold)
# three_in_1(img1, img2, img3, bboxes_imageDir, size1, size2, size3)
# with torch.no_grad():
#     pred = model([img1.to(device)])
#     print("model(images): ", pred)