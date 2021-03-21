#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/3/20.
# -----------------------------------------------------
import sys

sys.path.insert(0, sys.path[0] + '/..')

import os
from pycocotools.coco import COCO
import numpy as np
# import skimage.io as io
from PIL import Image
import matplotlib.pyplot as plt


def visualize_dataset(imageDir, annFile):
    coco = COCO(annFile)
    # Compute area if area is not set in annotations.
    coco.computeArea()

    # display coco categories and supercategories
    cats = coco.loadCats(coco.getCatIds())
    nms = [cat['name'] for cat in cats]
    print('coco categories: \n{}\n'.format(' '.join(nms)))
    super_nms = set([cat['supercategory'] for cat in cats])
    print('coco supercategories: \n{}\n'.format(' '.join(super_nms)))

    # get all images containing given categories, select one at random
    catIds = coco.getCatIds(catNms=nms)
    print(len(catIds))
    imgIds = coco.getImgIdsUnion(catIds=catIds)
    # imgIds = coco.getImgIdsUnion(catIds=coco.getCatIds());
    # imgIds = coco.getImgIds(catIds=catIds);
    # imgIds= coco.getImgIds();
    imgIds = sorted(imgIds)
    print(len(imgIds))

    # show image and annotations
    while True:
        # randomly pick one image
        imgId = imgIds[np.random.randint(len(imgIds))]
        print(imgId)
        img = coco.loadImgs(imgId)[0]
        # I = io.imread(img['file_name'])
        # print(I.shape)
        # I = io.imread('%s/images/%s/%s'%(dataDir,dataType,img['file_name']))
        # I = io.imread("{}".format(img['file_name']))
        print(img['file_name'])
        print(os.path.join(imageDir, img['file_name']))

        I = Image.open(os.path.join(imageDir, img['file_name']))
        print(img['file_name'])

        # load and display instance annotations
        plt.imshow(I)
        plt.axis('off')
        annIds = coco.getAnnIds(imgIds=imgId, catIds=catIds)
        print(annIds)
        anns = coco.loadAnns(annIds)
        coco.showAnns(anns, draw_bbox=True)
        # plt.show()
        plt.draw()  # need to use draw() instead of show() when use waitforbutttonpress()
        while not plt.waitforbuttonpress():
            continue
        plt.clf()

        # key = -1
        # def on_press(event):
        #     print('press', event.key)
        #     sys.stdout.flush()
        #     key = event.key
        # fig, ax = plt.subplots()
        # fig.canvas.mpl_connect('key_press_event', on_press)
        # while key != 32:
        #     print(key)
        #     continue


if __name__ == '__main__':
    print('Usage: visualize.py image_dir anno_file')
    # initialize coco ground truth api
    imageDir = sys.argv[1]
    annFile = sys.argv[2]
    visualize_dataset(imageDir, annFile)
