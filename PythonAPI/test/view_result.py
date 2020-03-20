#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/3/1.
# -----------------------------------------------------

import sys

sys.path.insert(0, sys.path[0] + '/..')
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import numpy as np
# import skimage.io as io
from PIL import Image

# initialize COCO ground truth api
annFile = 'test_set.json'
cocoGt = COCO(annFile)
# initialize COCO detections api
resFile = 'test_set_results.json'
cocoDt = cocoGt.loadRes(resFile)
# visualization settings
confidence_threshold = 0

fig = plt.figure(figsize=[15, 10])
imgIds = sorted(cocoGt.getImgIds())
print(len(imgIds))

while True:
    # randomly pick one image
    imgId = imgIds[np.random.randint(len(imgIds))]
    print(imgId)
    img = cocoGt.loadImgs(imgId)[0]
    # I = io.imread(img['file_name'])
    # print(I.shape)
    I = Image.open(img['file_name'])
    print(img['file_name'])

    # visualize high confidence detections
    plt.imshow(I)
    plt.axis('off')
    annIds = cocoDt.getAnnIds(imgIds=imgId)
    anns = cocoDt.loadAnns(annIds)
    fanns = []
    for ann in anns:
        if ann['score'] > confidence_threshold:
            fanns.append(ann)
    cocoDt.showAnns(fanns, draw_bbox=True)
    plt.show()
