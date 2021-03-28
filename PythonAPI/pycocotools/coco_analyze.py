#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2021/3/28.
# -----------------------------------------------------

from pycocotools.coco import COCO, _isArrayLike
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


def my_plot(data, label, name='', range=None, update_kwargs=None, save=False):
    kwargs = {'stacked': True, 'fill': True, 'cumulative': False,
              'density': False, 'bins': 30}
    if update_kwargs is not None:
        kwargs.update(update_kwargs)
    # _, _, patches = plt.hist(data, bins=bins, range=range, **kwargs)
    plt.hist(data, label=label, range=range, **kwargs)
    plt.xlabel(name)
    plt.title("histogram statistic")
    # plt.legend(patches, label, loc='upper right')
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='both')
    plt.show()
    if save and name != '':
        save_name = '{}_{}.jpg'.format(label, name)
        print("save ")
        plt.savefig(save_name)


class COCOAnalyze(COCO):
    def __init__(self, annotation_file=None):
        """
        Constructor of Microsoft COCO analyze class for analyze annotations.
        :param annotation_file (str): location of annotation file
        """
        # COCO.__init__(annotation_file)
        super(__class__, self).__init__(annotation_file)
        # bboxes, widths, heights, x_center, y_centerareas, aspect_ratios,
        self.createCatToBBoxesIndex()

    def createCatToBBoxesIndex(self):
        print('creating catToBBoxes index...')
        catToBBoxes = defaultdict(list)
        for catId in self.getCatIds():
            annIds = self.getAnnIds(catIds=catId)
            anns = self.loadAnns(annIds)
            for anno in anns:
                catToBBoxes[catId].append(anno['bbox'])
        self.catToBBoxes = catToBBoxes
        print('catToBBoxes index created!')

    def getBBoxes(self, catIds=[]):
        """
        Get bboxes of given cat ids.
        Args:
            catIds (int array):
        Returns:
            bboxes: numpy array of bboxes.
        """
        catIds = catIds if _isArrayLike(catIds) else [catIds]
        bboxes = []
        if len(catIds) == 0:
            catIds = self.getCatIds()
        for id in catIds:
            bboxes.extend(self.catToBBoxes[id])
        return np.array(bboxes)

    def getBBoxLeftX(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 0]

    def getBBoxTopY(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 1]

    def getBBoxWidths(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 2]

    def getBBoxHeights(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 3]

    def getBBoxAspectRatios(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 2] / bboxes[:, 3]

    def getBBoxAreas(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 2] * bboxes[:, 3]

    def getBBoxCenterX(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 0] + bboxes[:, 2] / 2

    def getBBoxCenterY(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 1] + bboxes[:, 3] / 2

    def getBBoxRightX(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 0] + bboxes[:, 2]

    def getBBoxBottomY(self, catIds=[]):
        bboxes = self.getBBoxes(catIds=catIds)
        return bboxes[:, 1] + bboxes[:, 3]
