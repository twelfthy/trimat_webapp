# PyTorch model and training necessities
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Image datasets and image manipulation
import torchvision
import torchvision.transforms as transforms

# Image display
import matplotlib.pyplot as plt
import numpy as np

# PyTorch TensorBoard support
from torch.utils.tensorboard import SummaryWriter



writer = SummaryWriter('/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/5_points_recognition/runs')

# Write scalar data to TensorBoard log dir
writer.add_scalar("lossgayz",3, 1)
writer.add_scalar("two", 2, 2)
writer.flush()
writer.close()