import math
import sys
import time
import torch

import torchvision.models.detection.mask_rcnn

from helper_functions.coco_utils import get_coco_api_from_dataset
from helper_functions.coco_eval import CocoEvaluator
import helper_functions.utils as utils




def train_one_epoch(model, optimizer, data_loader, data_loader_val, device, loss_vector, val_loss_vector, epoch, print_freq):
    model.train()
    metric_logger = utils.MetricLogger(delimiter="  ")
    metric_logger.add_meter('lr', utils.SmoothedValue(window_size=1, fmt='{value:.6f}'))
    header = 'Epoch: [{}]'.format(epoch)

    lr_scheduler = None
    if epoch == 0:
        warmup_factor = 1. / 1000
        warmup_iters = min(1000, len(data_loader) - 1)

        lr_scheduler = utils.warmup_lr_scheduler(optimizer, warmup_iters, warmup_factor)

    for images, targets in metric_logger.log_every(data_loader, print_freq, header):
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        loss_dict = model(images, targets)
        # print("model is: ", loss_dict)

        # Here we delete unneeded stuff:
        # del loss_dict["loss_objectness"]
        # del loss_dict["loss_rpn_box_reg"]
        # del loss_dict["loss_classifier"]
        # del loss_dict["loss_box_reg"]

        losses = sum(loss for loss in loss_dict.values())

        # reduce losses over all GPUs for logging purposes
        loss_dict_reduced = utils.reduce_dict(loss_dict)
        losses_reduced = sum(loss for loss in loss_dict_reduced.values())

        loss_value = losses_reduced.item()

        if not math.isfinite(loss_value):
            print("Loss is {}, stopping training".format(loss_value))
            print(loss_dict_reduced)
            sys.exit(1)

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        if lr_scheduler is not None:
            lr_scheduler.step()

        metric_logger.update(loss=losses_reduced, **loss_dict_reduced)
        metric_logger.update(lr=optimizer.param_groups[0]["lr"])

    loss_vector.append(metric_logger.meters["loss"].avg)
    print("\nAppending loss training.")

    #for validation set val:
    header2 = 'Validation:'
    for val_images, val_targets in metric_logger.log_every(data_loader_val, print_freq, header2):
        val_images = list(val_image.to(device) for val_image in val_images)
        val_targets = [{k2: v2.to(device) for k2, v2 in t2.items()} for t2 in val_targets]

        val_loss_dict = model(val_images, val_targets)
        # print("model is: ", loss_dict)

        # Here we delete unneeded stuff:
        # del loss_dict["loss_objectness"]
        # del val_loss_dict["loss_rpn_box_reg"]
        # del loss_dict["loss_classifier"]
        # del val_loss_dict["loss_box_reg"]

        val_losses = sum(loss for loss in val_loss_dict.values())

        # reduce losses over all GPUs for logging purposes
        val_loss_dict_reduced = utils.reduce_dict(val_loss_dict)
        val_losses_reduced = sum(val_loss for val_loss in val_loss_dict_reduced.values())
        metric_logger.update(loss=val_losses_reduced, **val_loss_dict_reduced)

    val_loss_vector.append(metric_logger.meters["loss"].avg)
    print("\nAppending loss validation.")

    return metric_logger


def _get_iou_types(model):
    model_without_ddp = model
    if isinstance(model, torch.nn.parallel.DistributedDataParallel):
        model_without_ddp = model.module
    iou_types = ["bbox"]
    if isinstance(model_without_ddp, torchvision.models.detection.MaskRCNN):
        iou_types.append("segm")
    if isinstance(model_without_ddp, torchvision.models.detection.KeypointRCNN):
        iou_types.append("keypoints")
    return iou_types


@torch.no_grad()
def evaluate(model, data_loader, device):
    n_threads = torch.get_num_threads()
    # FIXME remove this and make paste_masks_in_image run on the GPU
    torch.set_num_threads(1)
    cpu_device = torch.device("cpu")
    model.eval()
    metric_logger = utils.MetricLogger(delimiter="  ")
    header = 'Test:'

    coco = get_coco_api_from_dataset(data_loader.dataset)
    iou_types = _get_iou_types(model)
    coco_evaluator = CocoEvaluator(coco, iou_types)

    for images, targets in metric_logger.log_every(data_loader, 100, header):
        images = list(img.to(device) for img in images)

        torch.cuda.synchronize()
        model_time = time.time()
        outputs = model(images)

        outputs = [{k: v.to(cpu_device) for k, v in t.items()} for t in outputs]
        model_time = time.time() - model_time

        res = {target["image_id"].item(): output for target, output in zip(targets, outputs)}
        evaluator_time = time.time()
        coco_evaluator.update(res)
        evaluator_time = time.time() - evaluator_time
        metric_logger.update(model_time=model_time, evaluator_time=evaluator_time)

    # gather the stats from all processes
    metric_logger.synchronize_between_processes()
    print("Averaged stats:", metric_logger)
    coco_evaluator.synchronize_between_processes()

    # accumulate predictions from all images
    coco_evaluator.accumulate()
    coco_evaluator.summarize()
    torch.set_num_threads(n_threads)
    return coco_evaluator
