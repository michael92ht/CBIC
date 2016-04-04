# -*- coding:utf-8 -*-
# __author__ = 'Michael'


import cv2
from PCV.tools import rof
from pylab import *
from scipy import ndimage


def cvt(flag):
    return (1 - int(flag)) #* 255


def part_image(image_path):
    image = cv2.imread(image_path)
    width = image.shape[0]
    height = image.shape[1]
    bin_array = np.zeros((width, height), np.uint8)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    U, T = rof.denoise(img, img, tolerance=0.001)
    t = 0.8  # flower32_t0 threshold
    seg_im = U < t*U.max()
    for wid in range(0, width):
        for hei in range(0, height):
            bin_array[wid][hei] = cvt(seg_im[wid][hei]) * img[wid][hei]
    cv2.imshow("image", bin_array)
    cv2.waitKey(0)
    return bin_array


def get_hu_moments(image_path):
    # img = part_image(image_path)
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments)
    # print hu_moments
    features = [float(x) for x in hu_moments]
    return features
    # print features
    # cv2.imshow("image", img)
    # cv2.waitKey(0)


def sq(x):
    return x * x


# 计算离心率
def get_eccentricity(moments):
    a = moments['mu20']
    b = moments['mu02']
    c = moments['mu11']
    e = (a - sq(b) + 4 * sq(c)) / sq(a + b)
    return e


#  彩色图像 灰度图像 图像阀值处理 二值图像 图像尺寸归一化 提取 Hu
def get_hu(image_path):
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    rebinary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


    binary_img = cv2.resize(binary_img, (128, 128))
    rebinary_img = cv2.resize(rebinary_img, (128, 128))

    moments = cv2.moments(binary_img)
    hu_moments = cv2.HuMoments(moments)
    e = get_eccentricity(moments)
    hu = cv2.normalize(hu_moments)
    features = [float(x) for x in hu]
    features.append(e)

    moments = cv2.moments(rebinary_img)
    hu_moments = cv2.HuMoments(moments)
    e = get_eccentricity(moments)
    hu = cv2.normalize(hu_moments)
    features.extend([float(x) for x in hu])
    features.append(e)
    print features
    return features

def binary_img(canny):
    array = np.zeros(canny.shape, np.uint8)
    width = canny.shape[0]
    height = canny.shape[1]
    for i in range(1, width-1):
        for j in range(1, height-1):
            h = [canny[i-1][j-1],canny[i-1][j],canny[i-1][j+1],canny[i][j-1],canny[i][j+1],canny[i+1][j+1],canny[i+1][j-1],canny[i+1][j]]
            if 255 in h:
                array[i][j] = 255
    return array


def get_hu_features(image_path):
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(img, 50, 150)
    # cv2.imshow("s", canny)
    # cv2.waitKey(0)
    # print canny

    array = binary_img(canny)
    array = binary_img(array)



    cv2.imshow("s", array)
    cv2.waitKey(0)
    print canny
    # moments = cv2.moments(canny)
    # hu_moments = cv2.HuMoments(moments)
    # e = get_eccentricity(moments)
    # hu = cv2.normalize(hu_moments)
    # features = [float(x) for x in hu]
    # features.append(e)
    # # print features
    # return features


if __name__ == "__main__":
    image_path = r"D:\ICBC\corel\741.jpg"
    # get_hu_moments(image_path)
    part_image(image_path)
    # get_hu_features(image_path)
