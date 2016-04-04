#  __author__ = 'Michael'
# -*- coding: utf-8 -*-
# 提取图像的纹理特征，使用LBP算子，将图像分为9部分，采用LBP旋转不变等价模式，共提取81维颜色特征

import numpy as np
import cv2
from log import Logger

logger = Logger(logname='log.txt', loglevel=1, logger="lbp.py").getlog()

# revolve_map为旋转不变模式的36种特征值从小到大进行序列化编号得到的字典

revolve_map = {0: 0, 1: 1, 3: 2, 5: 3, 7: 4, 9: 5, 11: 6, 13: 7, 15: 8, 17: 9, 19: 10, 21: 11, 23: 12,
               25: 13, 27: 14, 29: 15, 31: 16, 37: 17, 39: 18, 43: 19, 45: 20, 47: 21, 51: 22, 53: 23, 55: 24,
               59: 25, 61: 26, 63: 27, 85: 28, 87: 29, 91: 30, 95: 31, 111: 32, 119: 33, 127: 34, 255: 35}

#  uniform_map为等价模式的58种特征值从小到大进行序列化编号得到的字典
uniform_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 6: 5, 7: 6, 8: 7, 12: 8,
               14: 9, 15: 10, 16: 11, 24: 12, 28: 13, 30: 14, 31: 15, 32: 16,
               48: 17, 56: 18, 60: 19, 62: 20, 63: 21, 64: 22, 96: 23, 112: 24,
               120: 25, 124: 26, 126: 27, 127: 28, 128: 29, 129: 30, 131: 31, 135: 32,
               143: 33, 159: 34, 191: 35, 192: 36, 193: 37, 195: 38, 199: 39, 207: 40,
               223: 41, 224: 42, 225: 43, 227: 44, 231: 45, 239: 46, 240: 47, 241: 48,
               243: 49, 247: 50, 248: 51, 249: 52, 251: 53, 252: 54, 253: 55, 254: 56, 255: 57}


#  将图像载入，并转化为灰度图，获取图像灰度图的像素信息
def get_gray_image(image_path):
    logger.info("get gray image of " + image_path)
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


#  图像的LBP原始特征计算算法：将图像指定位置的像素与周围8个像素比较
#  比中心像素大的点赋值为1，比中心像素小的赋值为2，返回得到的二进制序列
def calute_basic_lbp(image_array, i, j):
    binary_list = []
    if image_array[i-1, j-1] > image_array[i, j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    if image_array[i-1, j] > image_array[i, j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    if image_array[i-1,j+1] > image_array[i,j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    if image_array[i, j-1] > image_array[i,j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    if image_array[i, j+1] > image_array[i, j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    if image_array[i+1, j-1] > image_array[i, j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    if image_array[i+1, j] > image_array[i, j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    if image_array[i+1, j+1] > image_array[i, j]:
        binary_list.append(1)
    else:
        binary_list.append(0)
    return binary_list


#  获取二进制序列进行不断环形旋转得到新的二进制序列的最小十进制值
def get_min_for_revolve(arr):
    values = []
    circle = arr
    circle.extend(arr)
    for i in range(0, 8):
        j = 0
        arr_sum = 0
        bit_num = 0
        while j < 8:
            arr_sum += circle[i+j] << bit_num
            bit_num += 1
            j += 1
        values.append(arr_sum)
    return min(values)


#  获取值r的二进制中1的位数
def calc_sum(r):
    num = 0
    while r:
        r &= (r-1)
        num += 1
    return num


#  获取图像的LBP原始模式
def basic(image_path):
    gary_array = get_gray_image(image_path)
    basic_array = np.zeros(gary_array.shape, np.uint8)
    width = gary_array.shape[0]
    height = gary_array.shape[1]
    for i in range(1, width-1):
        for j in range(1, height-1):
            arr_sum = calute_basic_lbp(gary_array, i, j)
            bit_num = 0
            result = 0
            for s in arr_sum:
                result += s << bit_num
                bit_num += 1
            basic_array[i, j] = result
    logger.info("get basic lbp array of current image.")
    return basic_array


# 获取图像的LBP旋转不变模式特征
def revolve(image_path):
    image_array = get_gray_image(image_path)
    revolve_array = np.zeros(image_array.shape, np.uint8)
    width = image_array.shape[0]
    height = image_array.shape[1]
    for i in range(1, width-1):
        for j in range(1, height-1):
            sum = calute_basic_lbp(image_array, i, j)
            revolve_key = get_min_for_revolve(sum)
            revolve_array[i, j] = revolve_map[revolve_key]
    logger.info("get revolve lbp array of current image.")
    return revolve_array


# 获取图像的LBP统一模式
def uniform(basic_array):
    uniform_array = np.zeros(basic_array.shape, np.uint8)
    width = basic_array.shape[0]
    height = basic_array.shape[1]

    for i in range(1, width-1):
        for j in range(1, height-1):
             k = basic_array[i, j] << 1
             if k > 255:
                 k = k - 255
             xor = basic_array[i,j]^k
             num = calc_sum(xor)
             if num <= 2:
                 uniform_array[i, j] = uniform_map[basic_array[i, j]]
             else:
                 uniform_array[i, j] = 58
    logger.info("get uniform lbp array of current image.")
    return uniform_array


# 获取图像的LBP旋转不变统一模式
def uniform_revolve(basic_array):
    uniform_revolve_array = np.zeros(basic_array.shape, np.uint8)
    width = basic_array.shape[0]
    height = basic_array.shape[1]
    for i in range(1, width-1):
        for j in range(1, height-1):
                k = basic_array[i, j] << 1
                if k > 255:
                    k -= 255
                xor = basic_array[i, j] ^ k
                num = calc_sum(xor)
                if num <= 2:
                    uniform_revolve_array[i, j] = calc_sum(basic_array[i, j])
                else:
                    uniform_revolve_array[i, j] = 9
    logger.info("get uniform revolve lbp array of current image.")
    return uniform_revolve_array


# 获取图像LBP特征的统计直方图作为特征向量返回
def histogram(image_array, bins=59):
    hist = cv2.calcHist([image_array], [0], None, [bins], [0, bins])
    features = [float(x) for x in cv2.normalize(hist).flatten()]
    return features


# 获取图像原始LBP特征
def basic_features(image_path):
    basic_array = basic(image_path)
    logger.info("get basic lbp imagefeatures of current image.")
    return histogram(basic_array, 256)


# 获取图像LBP旋转不变模式特征
def revolve_features(image_path):
    revolve_array = revolve(image_path)
    logger.info("get revolve lbp imagefeatures of current image.")
    return histogram(revolve_array, 36)


# 获取图像LBP统一模式特征
def uniform_features(image_path):
    basic_array = basic(image_path)
    uniform_array = uniform(basic_array)
    logger.info("get uniform lbp imagefeatures of current image.")
    return histogram(uniform_array, 59)


# 获取图像LBP旋转不变统一模式特征
def uniform_revolve_features(image_path):
    basic_array = basic(image_path)
    uniform_revolve_array = uniform_revolve(basic_array)
    logger.info("get uniform revolve lbp imagefeatures of current image.")
    return histogram(uniform_revolve_array, 9)


#  将图像划分为n等份
def part_n_image(image_path, n):
    arr = basic(image_path)
    i = 0
    size = len(arr)
    part_image = []
    while i < n:
        left = i * size / n
        right = (i + 1) * size / n
        part_image.append(arr[left:right])
        i += 1
    logger.info("cut the image: " + image_path + " to  " + str(n) + r" parts")
    return part_image


#  获取图像分块的LBP旋转不变等价模式特征值
def blocks_features(image_path, blocks=4):
    part_image = part_n_image(image_path, blocks)
    features = list()
    for part in part_image:
        temp = histogram(uniform_revolve(part), 9)
        features.extend(temp)
    logger.info("get " + str(blocks) + r" parts of the image imagefeatures.")
    return features


def get_gabor_lbp(dest):
    basic_array = np.zeros(dest.shape, np.uint8)
    width = dest.shape[0]
    height = dest.shape[1]
    for i in range(1, width-1):
        for j in range(1, height-1):
            arr_sum = calute_basic_lbp(dest, i, j)
            bit_num = 0
            result = 0
            for s in arr_sum:
                result += s << bit_num
                bit_num += 1
            basic_array[i, j] = result
    uniform_revolve_array = uniform_revolve(basic_array)
    logger.info("get uniform revolve lbp imagefeatures of current image.")
    return histogram(uniform_revolve_array, 9)



if __name__ == "__main__":
   image_path = r"D:\ICBC\corel\999.jpg"
   # features = uniform_features(image_path)
   features = blocks_features(image_path)
   print features, len(features)