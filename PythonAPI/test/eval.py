#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/2/21.
# -----------------------------------------------------
import sys

sys.path.insert(0, sys.path[0] + '/..')
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

annType = ['segm', 'bbox', 'keypoints']
annType = annType[1]  # specify type here
prefix = 'person_keypoints' if annType == 'keypoints' else 'instances'
print('Running demo for *%s* results.'.format(annType))

# initialize COCO ground truth api
annFile = 'test_set.json'
cocoGt = COCO(annFile)
# Compute area if area is not set in annotations.
cocoGt.computeArea()
# initialize COCO detections api
resFile = 'test_set_results.json'
cocoDt = cocoGt.loadRes(resFile)
# running evaluation
cocoEval = COCOeval(cocoGt, cocoDt, annType)
# cocoEval.params.imgIds  = imgIds
# area_seq = [400, 800, 1200, 1600, 2000, 1e10]
# area_rng = [[0,area_seq[-1]]]
# for i in range(len(area_seq))
# cocoEval.params.areaRng = [[0 ** 2, 10e5 ** 2], [0 ** 2, 32 ** 2],
#                            [32 ** 2, 64 ** 2],
#                            [64 ** 2, 96 ** 2],
#                            [96 ** 2, 1e5 ** 2]]
# cocoEval.params.areaRngLbl = ['all', 'small', 'sm', 'medium', 'large']
# area_seq = [32**2, 96**2]
area_seq = [400, 800]
cocoEval.params.areaRng = [[0 ** 2, 10e5 ** 2], [0 ** 2, area_seq[0]],
                           [area_seq[0], area_seq[1]],
                           [area_seq[1], 1e5 ** 2]]
cocoEval.params.areaRngLbl = ['all', 's_' + str(area_seq[0]), 'medium',
                              'l_' + str(area_seq[1])]
cocoEval.params.iouThrSpec = 0.5
cocoEval.params.scoreThrs = [0.01, 0.05, 0.1, 0.2, 0.5]

cocoEval.evaluate()
cocoEval.accumulate()
# cocoEval.summarize(per_category=True, final_pr=True)
cocoEval.summarize(per_category=True, final_pr=False)

cocoGt.printCatNums()

cocoEval.computePR()
# cocoEval.params.catIds = cocoGt.getCatIds(catNms=["cat1"])
# cocoEval.evaluate()
# cocoEval.accumulate()
# cocoEval.summarize(final_pr=True)
#
# cocoEval.params.catIds = cocoGt.getCatIds(catNms=["cat2"])
# cocoEval.evaluate()
# cocoEval.accumulate()
# cocoEval.summarize(final_pr=True)
