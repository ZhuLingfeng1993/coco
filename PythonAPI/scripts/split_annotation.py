#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2021/3/27.
# -----------------------------------------------------
import sys
import json

sys.path.insert(0, sys.path[0] + '/..')

import os
from pycocotools.coco import COCO

annFile = sys.argv[1]
ratios = [0.6, 0.2, 0.2]
subsets_names = ['train', 'val', 'test']

coco = COCO(annFile)
# Compute area if area is not set in annotations.
coco.computeArea()

# display coco categories and supercategories
cats = coco.loadCats(coco.getCatIds())
print("image num all: {}".format(len(coco.getImgIds())))

json_subsets = coco.splitAnno(coco.getCatIds(), ratios)

output_dir = os.path.dirname(annFile)
for name, json_dict in zip(subsets_names, json_subsets):
    print("image num {}: {}".format(name, len(json_dict['images'])))
    json_file = os.path.join(output_dir, name + ".json")
    # os.makedirs(os.path.dirname(json_file), exist_ok=True)
    assert not os.path.exists(json_file)
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_dict, ensure_ascii=False, indent=2))
