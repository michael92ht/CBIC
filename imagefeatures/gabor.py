#  __author__ = 'Michael'
# -*- coding: utf-8 -*-
# 提取图像的纹理特征，使用4尺度6方向的Gabor变换，取变换后的图像灰度值的均值与方差，共提取4*6*2 = 48 维颜色特征

import numpy as np
import cv2
from log import Logger

logger = Logger(logname='log.txt', loglevel=1, logger="gabor.py").getlog()


def gabor_features(image, u=4, v=6):
    logger.info("get gabor imagefeatures for image: " + image)
    image = cv2.imread(image, 1)
    src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    src_f = np.array(src, dtype=np.float32)
    src_f /= 255.
    # us = [7, 12, 17, 21]                  # 4种尺度
    # vs = [0, 22.5,]        # 6个方向
    kernel_size = 21
    sig = 5                               # igma 带宽，取常数5
    gm = 1.0                              # gamma 空间纵横比，一般取1
    ps = 0.0                              # psi 相位，一般取0
    # lm = 1
    # th = 0

    features = []
    for i in range(0, u):
        for j in range(0, v):
            lm = i * (kernel_size - 3) / (u - 1) + 3
            th = j * np.pi / v
            kernel = cv2.getGaborKernel((kernel_size, kernel_size),
                                       sig, th, lm, gm, ps)
            dest = cv2.filter2D(src_f, cv2.CV_32F, kernel)
            features.append(float(np.mean(dest)))
            features.append(float(np.var(dest)))
    logger.info("get the imagefeatures of the image by " + str(u) + " scales and " + str(v) + " direction")
    return features

if __name__ == "__main__":
   image_path = r"D:\ICBC\corel\100.jpg"
   features = gabor_features(image_path)
   print features, len(features)

