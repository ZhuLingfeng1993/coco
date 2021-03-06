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
print('given cat names: {}'.format(cat_names))
catIds = coco.getCatIds(catNms=cat_names)
print(len(catIds))
annIds = coco.getAnnIds(catIds=catIds)
anns = coco.loadAnns(annIds)

# get category dict data
cat_num_dict = {}
cat_aspect_ratios_dict = {}  # aspect_ratio = width/height
cat_areas_dict = {}
cat_bbox_dict = {}
all_bboxes = []
for anno in anns:
    catId = anno['category_id']
    bbox = anno['bbox']
    all_bboxes.append(bbox)
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
# get all bbox info
# all_bboxes = np.array(all_bboxes)
# all_x = all_bboxes[:, 0]  # x_left
# all_y = all_bboxes[:, 1]  # y_top
# all_widths = all_bboxes[:, 2]
# all_heights = all_bboxes[:, 3]
# all_x_centers = all_x + all_widths / 2
# all_y_centers = all_y + all_heights / 2
# all_x_rights = all_x + all_widths
# all_y_bottoms = all_y + all_heights
#
# # bbox的上下左右的坐标分布
# image_width = 1920
# image_height = 1208
# left_ids = all_x_centers < image_width / 2
# right_ids = all_x_centers >= image_width / 2
# print(all_x.shape)
# print(all_x_rights.shape)
# all_x_sides = np.hstack((all_x[left_ids], all_x_rights[right_ids]))
# top_ids = all_y_centers < image_height / 2
# bottom_ids = all_y_centers >= image_height / 2
# all_y_sides = np.hstack((all_y[top_ids], all_y_bottoms[bottom_ids]))


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


def my_plot2d(data1, data2, name1='', name2='', contour=False, data_range=None,
              update_kwargs=None):
    kwargs = {'density': False}
    if update_kwargs is not None:
        kwargs.update(update_kwargs)
    h, xedges, yedges, _ = plt.hist2d(data1, data2, range=data_range, **kwargs)
    plt.grid(which='both')

    # show image with text annotation
    # h=h/np.sum(h)*100
    # plt.clf()
    # # plt.figure(figsize=(10, 10))
    # plt.imshow(h)
    # for i in range(len(yedges)-1):
    #     for j in range(len(xedges)-1):
    #         text = plt.text(j, i, h[i, j],
    #                         ha="center", va="center", color="w")

    plt.colorbar()
    plt.xlabel(name1)
    plt.ylabel(name2)
    plt.title(name1 + '_and_' + name2)
    # plt.legend(patches, label, loc='upper right')
    plt.minorticks_on()
    plt.show()
    plt.savefig("{}.jpg".format(name1 + '_and_' + name2))

    if contour:
        plt.clf()
        h = h / np.sum(h) * 100
        plt.clf()
        cs = plt.contour(np.transpose(h))
        plt.xlabel(name1)
        plt.ylabel(name2)
        plt.title(name1 + '_and_' + name2 + '_contour')
        plt.clabel(cs, inline=1)
        plt.show()
        plt.savefig("{}.jpg".format(name1 + '_and_' + name2 + '_contour'))


# plt.clf()
# update_kwargs = {'density': True, 'cumulative': True}
# my_plot(all_x_sides, 'all', name='x_sides_all_cum', range=None,
#         update_kwargs=update_kwargs)
# plt.clf()
# update_kwargs = {'density': True, 'cumulative': True}
# my_plot(all_y_sides, 'all', name='y_sides_all_cum', range=None,
#         update_kwargs=update_kwargs)

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

from matplotlib import colors  # for colors.LogNorm()

'''
plt.clf()
update_kwargs = {'bins': 25}
# update_kwargs = {'norm': colors.LogNorm()}
my_plot2d(all_x_centers, all_widths, name1='all_x_centers', name2='all_widths',
          data_range=[[0, 500], [0, 200]], update_kwargs=update_kwargs)
plt.clf()
update_kwargs = {'bins': 25}
# update_kwargs = {'norm': colors.LogNorm()}
my_plot2d(all_y_centers, all_widths, name1='all_y_centers', name2='all_widths',
          data_range=None, update_kwargs=update_kwargs)
plt.clf()
update_kwargs = {'bins': 25}
# update_kwargs = {'norm': colors.LogNorm()}
my_plot2d(all_x_centers, all_y_centers, name1='all_x_centers',
          name2='all_y_centers',
          data_range=None, update_kwargs=update_kwargs)

plt.clf()
update_kwargs = {}
my_plot(all_x_centers, 'all', name='all_x_centers', range=None,
        update_kwargs=update_kwargs)
plt.clf()
update_kwargs = {'density': True, 'cumulative': True}
my_plot(all_x_centers, 'all', name='x_center_all_cum', range=None,
        update_kwargs=update_kwargs)
plt.clf()
update_kwargs = {}
my_plot(all_y_centers, 'all', name='all_y_centers', range=None,
        update_kwargs=update_kwargs)
plt.clf()
update_kwargs = {'density': True, 'cumulative': True}
my_plot(all_y_centers, 'all', name='y_center_all_cum', range=None,
        update_kwargs=update_kwargs)
'''

plt.clf()
update_kwargs = {}
my_plot(all_widths, 'all', name='all_widths', range=None,
        update_kwargs=update_kwargs)
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
plt.clf()
my_plot(all_heights, 'all', name='all_heights', range=None,
        update_kwargs=update_kwargs)
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
