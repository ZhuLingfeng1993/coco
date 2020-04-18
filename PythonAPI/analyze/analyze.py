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
cat_num_dict = {}
cat_aspect_ratios_dict = {}  # aspect_ratio = width/height
cat_areas_dict = {}
cat_bbox_dict = {}
for anno in anns:
    catId = anno['category_id']
    bbox = anno['bbox']
    if catId not in cat_num_dict:
        cat_num_dict[catId] = 1
        cat_aspect_ratios_dict[catId] = []
        cat_areas_dict[catId] = []
        cat_bbox_dict[catId] = []
    else:
        cat_num_dict[catId] = cat_num_dict[catId] + 1
    cat_aspect_ratios_dict[catId].append(float(bbox[2]) / bbox[3])
    cat_areas_dict[catId].append(anno['area'])
    cat_bbox_dict[catId].append(bbox)

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
cat_names = []
areas_seq = []
aspect_ratios_seq = []
widths_seq = []
heights_seq = []
x_centers_seq = []
y_centers_seq = []
for catId in cat_num_dict:
    cat_names.append(coco.getCatName(catId))
    areas = np.array(cat_areas_dict[catId])
    areas_seq.append(areas)
    aspect_ratios = np.array(cat_aspect_ratios_dict[catId])
    aspect_ratios_seq.append(aspect_ratios)
    widths = np.array(cat_bbox_dict[catId])[:, 2]
    widths_seq.append(widths)
    heights = np.array(cat_bbox_dict[catId])[:, 3]
    heights_seq.append(heights)
    x_centers = np.array(cat_bbox_dict[catId])[:, 0] + np.array(
        cat_bbox_dict[catId])[:, 2] / 2
    x_centers_seq.append(x_centers)
    y_centers = np.array(cat_bbox_dict[catId])[:, 1] + np.array(
        cat_bbox_dict[catId])[:, 3] / 2
    y_centers_seq.append(y_centers)
all_areas = np.concatenate(areas_seq)
all_aspect_ratios = np.concatenate(aspect_ratios_seq)
all_widths = np.concatenate(widths_seq)
all_heights = np.concatenate(heights_seq)
all_x_centers = np.concatenate(x_centers_seq)
all_y_centers = np.concatenate(y_centers_seq)


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


def my_plot2d(data1, data2, name1='', name2='', range=None, update_kwargs=None):
    kwargs = {'density': False}
    if update_kwargs is not None:
        kwargs.update(update_kwargs)
    # _, _, patches = plt.hist(data, bins=bins, range=range, **kwargs)
    plt.hist2d(data1, data2, range=range, **kwargs)
    plt.xlabel(name1)
    plt.ylabel(name2)
    # plt.legend(patches, label, loc='upper right')
    plt.minorticks_on()
    plt.grid(which='both')
    plt.colorbar()
    plt.show()
    plt.savefig("{}.jpg".format(name1 + '_and_' + name2))


# plot
# plt.clf()
# update_kwargs = {'log': True}
# my_plot(areas_seq, cat_names, name='area_logy', range=None,
#         update_kwargs=update_kwargs)

# plt.clf()
# plt.semilogx()
# my_plot(areas_seq, cat_names, name='area_logxy', bins=30, range=None,
#         update_kwargs=update_kwargs)

# plt.clf()
# my_plot(areas_seq, cat_names, name='area_range_logy', range=(0, 10000),
#         update_kwargs=update_kwargs)
#
# plt.clf()
# update_kwargs = {'density': True, 'cumulative': True}
# my_plot(all_areas, 'all', name='area_all_cum', range=None,
#         update_kwargs=update_kwargs)
from matplotlib import colors

# # We can increase the number of bins on each axis
# axs[0].hist2d(x, y, bins=40)
#
# # As well as define normalization of the colors
# h2 = axs[1].hist2d(x, y, bins=40, norm=colors.LogNorm())
#
# # We can also define custom numbers of bins for each axis
# axs[2].hist2d(x, y, bins=(80, 10), norm=colors.LogNorm())
# plt.colorbar()

plt.clf()
# update_kwargs = {'bins':(25,50)}
update_kwargs = {}
my_plot2d(all_x_centers, all_widths, name1='all_x_centers', name2='all_widths',
          range=[[0, 500], [0, 200]], update_kwargs=update_kwargs)
plt.clf()
update_kwargs = {}
my_plot2d(all_y_centers, all_widths, name1='all_y_centers', name2='all_widths',
          range=None, update_kwargs=update_kwargs)

plt.clf()
update_kwargs = {}
my_plot(all_x_centers, 'all', name='all_x_centers', range=None,
        update_kwargs=update_kwargs)
plt.clf()
update_kwargs = {}
my_plot(all_y_centers, 'all', name='all_y_centers', range=None,
        update_kwargs=update_kwargs)

# plt.clf()
# update_kwargs = {}
# my_plot(all_widths, 'all', name='all_widths', range=None,
#         update_kwargs=update_kwargs)
#
# plt.clf()
# my_plot(all_widths, 'all', name='all_widths_range', range=(0, 400),
#         update_kwargs=update_kwargs)
#
# plt.clf()
# update_kwargs = {'density': True, 'cumulative': True}
# my_plot(all_widths, 'all', name='width_all_cum', range=None,
#         update_kwargs=update_kwargs)
#
# plt.clf()
# my_plot(all_heights, 'all', name='all_heights', range=None,
#         update_kwargs=update_kwargs)
#
# plt.clf()
# my_plot(all_heights, 'all', name='all_heights_range', range=(0, 10000),
#         update_kwargs=update_kwargs)
#
# plt.clf()
# update_kwargs = {'density': True, 'cumulative': True}
# my_plot(all_heights, 'all', name='height_all_cum', range=None,
#         update_kwargs=update_kwargs)

# plt.clf()
# my_plot(all_areas, 'all', name='area_all_cum', bins=30, range=(0, 10000),
#         update_kwargs=update_kwargs)

# plt.clf()
# plt.semilogy()
# my_plot(aspect_ratios_seq, cat_names, name='aspect_ratio_logy',
#         range=None)
#
# plt.clf()
# plt.semilogy()
# my_plot(aspect_ratios_seq, cat_names, name='aspect_ratio_range_logy',
#         range=(0, 4))

# plt.clf()
# update_kwargs = {'density': True, 'cumulative': True}
# my_plot(all_aspect_ratios, 'all', name='aspect_ratio_all_cum', bins=30,
#         range=None, update_kwargs=update_kwargs)
