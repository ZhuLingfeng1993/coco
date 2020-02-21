#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/2/21.
# -----------------------------------------------------
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

annType = ['segm', 'bbox', 'keypoints']
annType = annType[1]  # specify type here
prefix = 'person_keypoints' if annType == 'keypoints' else 'instances'
print 'Running demo for *%s* results.' % (annType)

# initialize COCO ground truth api
annFile = 'test_set.json'
cocoGt = COCO(annFile)
# initialize COCO detections api
resFile = 'test_set_results.json'
cocoDt = cocoGt.loadRes(resFile)
# running evaluation
cocoEval = COCOeval(cocoGt, cocoDt, annType)
# cocoEval.params.imgIds  = imgIds

cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize(per_category=True, final_pr=False)

# cocoEval.params.catIds = cocoGt.getCatIds(catNms=["cat1"])
# cocoEval.evaluate()
# cocoEval.accumulate()
# cocoEval.summarize(final_pr=True)
#
# cocoEval.params.catIds = cocoGt.getCatIds(catNms=["cat2"])
# cocoEval.evaluate()
# cocoEval.accumulate()
# cocoEval.summarize(final_pr=True)
