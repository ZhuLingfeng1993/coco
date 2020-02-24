# COCO

## 官方文档

官网很难访问, 可以下载 [github代码](https://github.com/cocodataset/cocodataset.github.io), 从而快速浏览网页内容

## Detection Evaluation

详见官方文档和代码注释

部分评价参数说明：

- evaluation parameters中的"recThrs": [0:.01:1] R=101 recall thresholds for evaluation

  这些recalls用于对precisions进行采样，从而计算AP，原理与11点插值类似，不过默认情况下取的点更多

- Average Recall (AR): AR is the maximum recall given a fixed number of detections per image

  在evaluation parameters"maxDets": [1 10 100] M=3 thresholds on max detections per image下，将检测的所有结果当做positive时，得到的Recall

## Dataset

### Images

2014 Train images [83K/13GB]
2014 Val images [41K/6GB]
2014 Test images [41K/6GB]
2015 Test images [81K/12GB]
2017 Train images [118K/18GB]
2017 Val images [5K/1GB]
2017 Test images [41K/6GB]
2017 Unlabeled images [123K/19GB]

### Annotations

2014 Train/Val annotations [241MB]
2014 Testing Image info [1MB]
2015 Testing Image info [2MB]
2017 Train/Val annotations [241MB]
2017 Stuff Train/Val annotations [1.1GB]
2017 Panoptic Train/Val annotations [821MB]
2017 Testing Image info [1MB]
2017 Unlabeled Image info [4MB]

### note zlf

train/val数据是完全公开的, 具体划分其实是可以自行决定的, weiliu的minival应该是从2014的val中提取了5K, 而2017的val就是5K

test数据是不公开annotation的, 是放在官方服务器上, 需要提交网络才能测试的, 但有images以及说明哪些是test数据的image_info_test文件

### note on offical website

Note that the 2017 train/val data includes the same images as the 2014 train/val data just organized differently, so there is no benefit of using 2014 training data for the 2017 competition.

we note that 2017 dev / challenge splits contain the same images as the 2015 dev / challenge splits so results across years are directly comparable.

**Test-Dev:**

The test-dev split is the default test data for testing under general circumstances. Results in papers should generally be reported on test-dev to allow for fair public comparison. 

**Test-Challenge:**

The test-challenge split is used for COCO challenges hosted on a yearly basis. Results are revealed during the relevant workshop (typically at ECCV or ICCV). 

The images belonging to each split are defined in image_info_test-dev2017 (for test-dev) and image_info_test2017 (for combined test-dev and test-challenge).

**2015 Test Set Splits**

This test set was used for 2015 and 2016 detection and keypoint challenges. *It is no longer used and the evaluation servers are closed*.