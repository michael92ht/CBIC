#  __author__ = 'Michael'
# -*- coding: utf-8 -*-
# 提取图像的纹理特征，使用多尺度多方向的Gabor变换，取滤波后图像的均值与方差作为图像的纹理特征

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
    kernel_size = 21
    sig = 5                               # igma 带宽，取常数5
    gm = 1.0                              # gamma 空间纵横比，一般取1
    ps = 0.0                              # psi 相位，一般取0

    features = []
    for i in range(0, u):
        for j in range(0, v):
            lm = i * (kernel_size - 3) / (u - 1) + 3      # 尺度取[3, 21]内等分的数据
            th = j * np.pi / v                            # 方向取[0, pi）内等分的角度
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

