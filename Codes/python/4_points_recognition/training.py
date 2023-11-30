# Sample code from the TorchVision 0.3 Object Detection Finetuning Tutorial
# http://pytorch.org/tutorials/intermediate/torchvision_tutorial.html

import os
import numpy as np
import matplotlib.pyplot as plt
import torch
from PIL import Image, ImageDraw

import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
# from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

from helper_functions.engine import train_one_epoch, evaluate
import helper_functions.utils as utils
import helper_functions.transforms as T
from helper_functions.read import read_notes

from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter('/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/4_points_recognition/runs')


class Points_Dataset(object):
    def __init__(self, root, transforms):
        self.root = root
        self.transforms = transforms
        self.imgs = list(sorted(os.listdir(os.path.join(root, "01_Images"))))
        self.notes = list(sorted(os.listdir(os.path.join(root, "02_Annotations"))))

    def __getitem__(self, idx):
        # load images and masks
        img_path = os.path.join(self.root, "01_Images", self.imgs[idx])
        # print(img_path)
        notes_path = os.path.join(self.root, "02_Annotations", self.notes[idx])
        # mask_path = os.path.join(self.root, "PedMasks", self.masks[idx])
        img = Image.open(img_path).convert("RGB")
        
        # get bounding box coordinates:
        num_objs = 1
        labels = []         # ["", "", ""]
        bndboxes = []       # {[x_min, y_min, x_max, y_max],
                            #  [x_min, y_min, x_max, y_max]}

        read_notes(notes_path, num_objs, labels, bndboxes)
        # print("the number of objects is: ",num_objs)
        # print(labels)
        labels = torch.tensor(labels)
        bndboxes = torch.as_tensor(bndboxes, dtype=torch.float32)
        image_id = torch.tensor([idx])
        area = (bndboxes[:, 3] - bndboxes[:, 1]) * (bndboxes[:, 2] - bndboxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)
        target = {}
        target["boxes"] = bndboxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd
        

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)

def get_model_instance_segmentation(num_classes):
    # load an instance segmentation model pre-trained pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)

    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)


def main():
    torch.set_num_threads(1)
    # train on the GPU or on the CPU, if a GPU is not available
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(device)
    # our dataset has four classes: - background and 18 vertebras
    num_classes = 2
    # use our dataset and defined transformations
    dataset = Points_Dataset('/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/4_points_recognition/trainset', get_transform(train=True))
    dataset_validation = Points_Dataset('/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/4_points_recognition/testset', get_transform(train=False))
    # define training and validation data loaders
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=True, num_workers=4,
        collate_fn=utils.collate_fn)
    data_loader_validation = torch.utils.data.DataLoader(
        dataset_validation, batch_size=1, shuffle=False, num_workers=4,
        collate_fn=utils.collate_fn)
    # get the model using our helper function
    model = get_model_instance_segmentation(num_classes)
    # move model to the right device
    model.to(device)
    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.002,
                                momentum=0.9, weight_decay=0.005) 
    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=3,
                                                   gamma=0.1) # decreases the lr
    # let's train it for 10 epochs
    num_epochs = 5
    loss_vector = []
    val_loss_vector = []
    passes = 0
    # print("model is: ", model)
    for epoch in range(num_epochs):
        # train for one epoch, printing every 10 iterations
        train_one_epoch(model, optimizer, data_loader, data_loader_validation, device, loss_vector, val_loss_vector, epoch, print_freq=10)
        for i in range(1):
            # print(loss_vector[passes])
            writer.add_scalars("losses",
                                {'training loss': loss_vector[passes],
                                'validation loss': val_loss_vector[passes]},
                                passes)
            plt.scatter(passes, loss_vector[passes], color='red', s=100, marker='s')
            passes += 1
        # update the learning rate
        lr_scheduler.step()
        # evaluate on the test dataset
        # evaluate(model, data_loader_validation, device=device)

    plt.title('Loss Function', fontsize=16, fontweight='bold', fontfamily='serif', color='green')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.savefig('/home/ogianoli/Code/eos-landmark-detection/LMD/PLOTS/loss_plot.png')

    print("That's it for training. Now lets test. \n")

    torch.save(model.state_dict(), '/home/ogianoli/Code/eos-landmark-detection/LMD/model_weights.pth')


if __name__ == "__main__":
    main()
    