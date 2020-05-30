#!/usr/bin/env python
# coding=utf-8

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/2/26.
# -----------------------------------------------------

import json


def create_label_map_file(labels, outfile_path):
    with open(outfile_path, 'w') as f:
        for i, label in enumerate(labels):
            name = '  name: "' + str(label) + '"'
            label_id = '  id: ' + str(i)
            display_name = '  display_name: "' + str(label) + '"'
            classes = ('item {', name, label_id, display_name, '}')
            for j in range(len(classes)):
                f.writelines(classes[j])
                f.writelines('\n')

def create_fg_label_map_file(labels, outfile_path):
    with open(outfile_path, 'w') as f:
        for i, label in enumerate(labels):
            name = '  name: "' + str(label) + '"'
            label_id = '  id: ' + str(min(i, 1))
            classes = ('item {', name, label_id, '}')
            for j in range(len(classes)):
                f.writelines(classes[j])
                f.writelines('\n')


def create_json_label_map_file(labels, outfile_path):
    label_map = {i: label for i, label in enumerate(labels)}
    # label_map = {}
    # for i, label in enumerate(labels):
    #     label_map[i] = label
    with open(outfile_path, 'w') as f:
        json.dump(label_map, f, indent=2)


def generate_tfl_categories(abbr=False, type=0):
    """
    Generate traffic light categories.
    :return: Generated categories.
    """
    light_colors = ["red", "green", "yellow"]
    light_types = ["", "straight", "left", "right", "turn"]  # "" for circle light
    # bbox_sizes = ["max", "min"]  # max for whole light, min for sub-light
    bbox_sizes = ["max"]

    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    num_values = [d1 + d2 for d1 in digits for d2 in digits] + digits

    classes = []
    if not abbr:
        classes.append('background')
        none_number_classes = [lc + lt + bs for lc in light_colors for lt in light_types for bs in bbox_sizes]
        number_classes_without_value = [lc + "num" for lc in light_colors]
    else:
        classes.append('bg')
        light_types[0] = "c"
        # none_number_classes = [lc[0] + lt[0] + bs for lc in light_colors for lt in light_types for bs in bbox_sizes]
        none_number_classes = [lc[0] + lt[0] for lc in light_colors for lt in light_types]
        number_classes_without_value = [lc[0] + "n" for lc in light_colors]

    # Temporary ignore label in the format of color+num_value
    if type == 0:
        classes.extend(none_number_classes)
    elif type == 1:
        classes.extend(none_number_classes + number_classes_without_value)
    return classes


if __name__ == '__main__':
    classes = generate_tfl_categories(abbr=False)
    print(classes)
    create_label_map_file(classes, './tfl_none_num_max_label_map.pbtxt')
    create_json_label_map_file(classes, './tfl_none_num_max_label_map.json')
    classes = generate_tfl_categories(abbr=True)
    create_json_label_map_file(classes, './tfl_none_num_max_abbr_label_map.json')

    classes = generate_tfl_categories(abbr=False, type=1)
    print(classes)
    create_fg_label_map_file(classes, './tfl_fg_max_label_map.pbtxt')
    create_label_map_file(classes, './tfl_max_label_map.pbtxt')
    classes = generate_tfl_categories(abbr=True, type=1)
    create_json_label_map_file(classes, './tfl_max_abbr_label_map.json')
