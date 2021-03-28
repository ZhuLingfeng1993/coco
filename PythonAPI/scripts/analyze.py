#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2021/3/28.
# -----------------------------------------------------
import sys
from pycocotools.coco_analyze import COCOAnalyze, my_plot

annFile = sys.argv[1]

coco = COCOAnalyze(annFile)

# get all cats
catNms = 'all'
catIds = coco.getCatIds()

# get specific cats
# catNms = ['yin_hua_qing_xie']
# catIds = coco.getCatIds(catNms=catNms)

widths = coco.getBBoxWidths(catIds=catIds)
my_plot(data=widths, label=catNms, name='widths')

aspect_ratios = coco.getBBoxAspectRatios(catIds=catIds)
my_plot(data=aspect_ratios, label=catNms, name='aspect_ratios')
