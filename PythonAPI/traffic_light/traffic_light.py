#!/usr/bin/env python
# coding=utf-8

# -----------------------------------------------------
# Written by Zhu Lingfeng on 2020/2/26.
# -----------------------------------------------------


def generate_tfl_categories():
    """
    Generate traffic light categories.
    :return: Generated categories.
    """
    light_colors = ["red", "green", "yellow"]
    light_types = ["", "straight", "left", "right", "turn"]  # "" for circle light
    bbox_sizes = ["max", "min"]  # max for whole light, min for sub-light

    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    num_values = [d1 + d2 for d1 in digits for d2 in digits] + digits

    none_number_classes = [lc + lt + bs for lc in light_colors for lt in light_types for bs in bbox_sizes]
    number_classes_without_value = [lc + "num" for lc in light_colors]

    # Temporary ignore label in the format of color+num_value
    classes = none_number_classes + number_classes_without_value
    return classes
