# __author__ = 'Michael'
#  -*- coding: utf-8 -*-

from PIL import Image
import os
import numpy as np
from pylab import *
from math import *
import pca

SIFT = r"D:\ICBC\software\vlfeat-0.9.20\bin\win64\sift.exe"


def process_image(imagename, resultname, params="--edge-thresh 10 --peak-thresh 5"):
    """处理一副图像，然后将结果保存在文件中"""

    if imagename[-3:] != 'pgm':
        # 创建一个pgm文件
        im = Image.open(imagename).convert('L')
        im.save('tmp.pgm')
        imagetmp = 'tmp.pgm'
    else:
        imagetmp = imagename
    cmmd = str(SIFT+" "+imagetmp+" --output="+resultname+" "+params)
    os.system(cmmd)
    if imagetmp == 'tmp.pgm':
        os.remove("tmp.pgm")
    print 'processed', imagename, 'to', resultname


def read_features_from_file(filename):
    """读取特征属性值，然后将其以矩阵的形式返回"""

    f = np.loadtxt(filename)
    locs = f[:, :4]
    desc = f[:, 4:]
    return locs, desc   # 特征位置，描述子


def write_features_to_file(filename, locs, desc):
    """将特征位置和描述子保存到文件中"""

    np.savetxt(filename, np.hstack((locs, desc)))

def plot_features(im, locs, circle=False):
    """显示带有特征的图像
       输入：im（数组图像），locs(每个特征的行、列、尺度和朝向)"""

    def draw_circle(c, r):
        t = np.arange(0, 1.01, .01) * 2 * pi
        x = r * cos(t) + c[0]
        y = r * sin(t) + c[1]
        plot(x, y, 'b', linewidth=2)

    imshow(im)

    if circle:
        for p in locs:
            draw_circle(p[:2], p[2])
    else:
        plot(locs[:, 0], locs[:, 1], 'ob')
    axis('off')

def show_sift(image):
    im = np.array(Image.open(image).convert('L'))
    process_image(image, 'empire.sift')
    l1, d1 = read_features_from_file('empire.sift')
    os.remove('empire.sift')

    figure()
    gray()
    plot_features(im, l1) # , circle=True)
    show()

def pca_features(image):
    im = np.array(Image.open(image).convert('L'))
    process_image(image, 'empire.sift')
    features = np.loadtxt('empire.sift')
    os.remove('empire.sift')
    V, S, m = pca.pca(features)
    V = V[:50]
    features = array([dot(V, f-m) for f in features])
    np.savetxt('fea.txt', features)
    print 'done'




if __name__ == "__main__":
    image = r"D:\ICBC\corel\666.jpg"
    pca_features(image)
    # show_sift(image)
    # outfile = r"D:\ICBC\resluts\sift.txt"
    # # process_image(image, outfile)
    # filename = r"D:\ICBC\resluts\s.txt"
    # locs, desc = read_features_from_file(outfile)
    # write_features_to_file(filename, locs, desc)
