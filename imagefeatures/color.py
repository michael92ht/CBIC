# __author__ = 'Michael'
# -*- coding: utf-8 -*-

import os
import cv2
from matplotlib import pyplot as plt
from pandas import DataFrame
from log import Logger
from imagefeatures.hsv import *

logger = Logger(logname='log.txt', loglevel=1, logger="color.py").getlog()
COLOR_NUM = [36, 72, 20, 44, 76]
HSVQUA = [HsvQua36, HsvQua72, HsvQua20, HsvQua44, HsvQuaTest]


# 打开图片，并转化为HSV颜色空间
def get_hsv(path):
    if not os.path.exists(path):
        logger.error(path + " is not exist!")
        return
    try:
        image = cv2.imread(path)
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        logger.info("get image hsv color space." + path)
        return image_hsv
    except Exception, e:
        logger.error("Can't get image hsv space color data from " + path)
        logger.error(e)


# 获取图像数据中央与背景区域的掩码
def get_partion_mask(imdata):
    (h, w) = imdata.shape[:2]
    (cX, cY) = (int(w * 0.5), int(h * 0.5))
    segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]
    (axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
    centerMask = np.zeros(imdata.shape[:2], dtype="uint8")
    cv2.ellipse(centerMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
    backgroudMask = np.zeros(imdata.shape[:2], dtype="uint8")
    cv2.rectangle(backgroudMask, (0, 0), (w, h), 255, -1)
    backgroudMask = cv2.subtract(backgroudMask, centerMask)
    logger.info("get centerMask and backgroudMask of the image")
    return centerMask, backgroudMask


# 获取图像RGB空间的三阶颜色矩
def moments_features(path):
    if not os.path.exists(path):
        logger.error(path + " is not exist!")
        return
    im = cv2.imread(path)
    [b, g, r] = cv2.split(im)
    moments = []
    for n in [b, g, r]:
        df = DataFrame(np.array(n.flatten()))
        moments.extend(float(x) for x in [df.mean()[0], df.std()[0], df.skew()[0]])
    return moments


# 显示量化后的图像颜色统计直方图
def show_histogram(data, mode=0, col='r'):
    bins = COLOR_NUM[mode]
    hist = cv2.calcHist(data, [0], None, [bins], [0, bins])
    hist = cv2.normalize(hist, norm_type=cv2.NORM_L1).flatten()
    plt.plot(hist, color=col)
    plt.xlim([0, bins])
    plt.show()


# 定义使用的颜色量化方式得到量化后的颜色
def get_qua(imdata, mode=0):
    cur_mode = HSVQUA[mode]
    logger.info("current image qua mode: " + cur_mode.mode)
    qua_im = cur_mode().calute(imdata)
    return qua_im


# 定义使用的颜色量化方式得到特征向量,模式默认为0，掩码为无，可使用掩码获取指定区域的颜色特征
def global_features(image_path, mode=3, mask=None):
    imdata = get_hsv(image_path)
    qua_im = get_qua(imdata, mode)
    bins = COLOR_NUM[mode]
    hist = cv2.calcHist([qua_im], [0], mask, [bins], [0, bins])
    hist = cv2.normalize(hist).flatten()
    # plt.plot(hist, color='r')
    # plt.xlim([0, bins])
    # plt.show()
    features = [float(x) for x in hist]
    logger.info("get image color features!")
    return features
    # return qua_im


# 获取中央区域和背景区域的特征向量
def get_segment_features(path):
    imdata = get_hsv(path)
    center, backgroud = get_partion_mask(imdata)
    features = global_features(imdata, 2, backgroud)
    features.extend(global_features(imdata, 2, center))
    logger.info("get center and backgroud features!" + path)
    return features


# 获取图像的全局颜色特征及颜色矩结合的特征向量
def get_merge_color(path):
    features = moments_features(path)
    features.extend(global_features(path))
    return features


color_list = ['r', 'g', 'b']
def show_features(image_folder, mode=3, mask=None):
    image_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if 'jpg' in f]
    index = 0
    for image_path in image_list:
        imdata = get_hsv(image_path)
        qua_im = get_qua(imdata, mode)
        bins = COLOR_NUM[mode]
        hist = cv2.calcHist([qua_im], [0], mask, [bins], [0, bins])
        hist = cv2.normalize(hist).flatten()
        plt.plot(hist, color=color_list[index])
        plt.xlim([0, bins])
        index += 1
    plt.show()
        # features = [float(x) for x in hist]
        # logger.info("get image color features!")
    # return features


if __name__ == "__main__":
    image_folder = r"D:\ICBC\test"
    # image_path = r"D:\ICBC\test\2.jpg"
    image_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if 'jpg' in f]
    import time
    start = time.clock()
    for image_path in image_list:
        features = global_features(image_path, 3)
    end = time.clock()
    print "read: %f s" % (end - start)
    # for i in range(0, 4):
    # features = global_features(image_path, 1)
    # show_histogram(features, 1, col='r')
    # print features, len(features), sum(features)
