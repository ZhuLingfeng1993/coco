#!/usr/bin/env python

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/3/20.
# -----------------------------------------------------
from pycocotools.coco import COCO
import numpy as np
import matplotlib.pyplot as plt
import sys

# initialize coco ground truth api
# dataDir='/workspace/coco2017'
# dataType='val2017'
# annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
# annFile = '../data/instances_val2017_100.json'
annFile = sys.argv[1]
# annFile = '../test/voc2007_train.json'
coco = COCO(annFile)
# Compute area if area is not set in annotations.
coco.computeArea()

# display coco categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
print('coco categories: \n{}\n'.format(' '.join(nms)))
# super_nms = set([cat['supercategory'] for cat in cats])
# print('coco supercategories: \n{}'.format(' '.join(super_nms)))

# get all annotations containing given categories
cat_names = ['person', 'bicycle', 'car', 'chair']
catIds = coco.getCatIds(catNms=cat_names)
print(len(catIds))
annIds = coco.getAnnIds(catIds=catIds)
anns = coco.loadAnns(annIds)

# get category dict data
cat_aspect_ratios_dict = {}  # aspect_ratio = width/height
cat_areas_dict = {}
cat_num_dict = {}
for anno in anns:
    catId = anno['category_id']
    bbox = anno['bbox']
    if catId not in cat_num_dict:
        cat_num_dict[catId] = 1
        cat_aspect_ratios_dict[catId] = []
        cat_areas_dict[catId] = []
    else:
        cat_num_dict[catId] = cat_num_dict[catId] + 1
    cat_aspect_ratios_dict[catId].append(float(bbox[2]) / bbox[3])
    cat_areas_dict[catId].append(anno['area'])

# get category object number statistics
all_num = 0
sorted_cat_num_dict = sorted(cat_num_dict.items(), key=lambda x: x[1],
                             reverse=True)
print('############ category objects number:')
for catId, num in sorted_cat_num_dict:
    cat_name = coco.getCatName(catId)
    all_num += num
    print("{}: {}".format(cat_name, num))
print('all objects number: {}'.format(all_num))

# prepare data to plot
areas_seq = []
aspect_ratios_seq = []
cat_names = []
for catId in cat_num_dict:
    cat_names.append(coco.getCatName(catId))
    areas = np.array(cat_areas_dict[catId])
    areas_seq.append(areas)
    aspect_ratios = np.array(cat_aspect_ratios_dict[catId])
    aspect_ratios_seq.append(aspect_ratios)
all_areas = np.concatenate(areas_seq)
all_aspect_ratios = np.concatenate(aspect_ratios_seq)


def my_plot(data, label, name='', range=None, update_kwargs=None):
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
    plt.savefig("{}.jpg".format(name))


# plot
plt.clf()
update_kwargs = {'log': True}
my_plot(areas_seq, cat_names, name='area_logy', range=None,
        update_kwargs=update_kwargs)

# plt.clf()
# plt.semilogx()
# my_plot(areas_seq, cat_names, name='area_logxy', bins=30, range=None,
#         update_kwargs=update_kwargs)

plt.clf()
my_plot(areas_seq, cat_names, name='area_range_logy', range=(0, 10000),
        update_kwargs=update_kwargs)

plt.clf()
update_kwargs = {'density': True, 'cumulative': True}
my_plot(all_areas, 'all', name='area_all_cum', range=None,
        update_kwargs=update_kwargs)

# plt.clf()
# my_plot(all_areas, 'all', name='area_all_cum', bins=30, range=(0, 10000),
#         update_kwargs=update_kwargs)

plt.clf()
plt.semilogy()
my_plot(aspect_ratios_seq, cat_names, name='aspect_ratio_logy',
        range=None)

plt.clf()
plt.semilogy()
my_plot(aspect_ratios_seq, cat_names, name='aspect_ratio_range_logy',
        range=(0, 4))

# plt.clf()
# update_kwargs = {'density': True, 'cumulative': True}
# my_plot(all_aspect_ratios, 'all', name='aspect_ratio_all_cum', bins=30,
#         range=None, update_kwargs=update_kwargs)
