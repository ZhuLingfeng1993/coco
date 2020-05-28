#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/5/28.
# -----------------------------------------------------

import sys

sys.path.insert(0, sys.path[0] + '/..')

from pycocotools.coco import COCO
from traffic_light.traffic_light import generate_tfl_categories

train_annoFiles = [
    '/workspace/ShareData/data/city/tfl_tsr/coco/tsr-turnandright-20200302-coco-tr10/original/dataset/train/train.json',
    '/workspace/ShareData/data/city/tfl_tsr/coco/tsr-turnandright-20200120-coco-tr10/original/dataset/train/train.json',
    '/workspace/ShareData/data/city/tfl_tsr/coco/sr-turnandright-20200214-coco-tr10/original/dataset/train/train.json',
    '/workspace/ShareData/data/city/tfl_tsr/coco/tsr-turnandright-20200215-coco-tr10/original/dataset/train/train.json',
    '/workspace/ShareData/data/city/tfl_tsr/coco/tsr-yellowandarrow-20200309-coco-tr10/original/dataset/train/train.json',
]
test_annoFiles = [
    '/workspace/ShareData/data/city/tfl_tsr/coco/tsr-turnandright-0224-coco-tr10/original/dataset/train/train.json',
]
val_annoFiles = [
    '/media/lenovo/zlf_ubuntu_backup/data/city/tfl_tsr/tsr-turnandright-0224-tr8val2/original/dataset/val/val.json',
]

annoFiles = train_annoFiles

catNms = generate_tfl_categories(abbr=False, type=1)

catNameNumsAll = {}
for name in catNms:
    catNameNumsAll[name] = 0

totalNum = 0
for annoFile in annoFiles:
    cocoGt = COCO(annoFile)
    catIds = cocoGt.getCatIds(catNms)
    _, catNameNums = cocoGt.countCatNums(catIds)
    for name, num in catNameNums.items():
        totalNum += num
        if name in catNameNumsAll:
            catNameNumsAll[name] += num

key_sorted_count = sorted(catNameNumsAll.items(), key=lambda x: x[0])
value_sorted_count = sorted(catNameNumsAll.items(), key=lambda x: x[1],
                            reverse=True)

print("########  Category annotation numbers #######")
print("|{:<20}| {:<10}|".format('category', 'Numbers'))
print("|---------------|-------------------------------|")
print("|{:<20}| {:<10}|".format('total', totalNum))
for name, num in value_sorted_count:
    print("|{:<20}| {:<10}|".format(name, num))
