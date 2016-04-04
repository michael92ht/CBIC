import cv2
import numpy as np
from matplotlib import pyplot as plt
import copy


def in_range(number, left, right):
    return left < number <= right


def h_value(h):
    if h <= 10 or in_range(h, 158, 180):
        return 0.0
    elif in_range(h, 10, 20):
        return 1.0
    elif in_range(h, 20, 37.5):
        return 2.0
    elif in_range(h, 37.5, 78):
        return 3.0
    elif in_range(h, 78, 95):
        return 4.0
    elif in_range(h, 95, 135):
        return 5.0
    elif in_range(h, 135, 148):
        return 6.0
    elif in_range(h, 148, 158):
        return 7.0


def s_value(s):
    if s == 0 or in_range(s, 0, 256 * 0.2):
        return 0.0
    elif in_range(s, 256 * 0.2, 256 * 0.7):
        return 1.0
    elif in_range(s, 256 * 0.7, 256):
        return 2.0


def v_value(v):
    if v == 0 or in_range(v, 0, 256 * 0.2):
        return 0.0
    elif in_range(v, 256 * 0.2, 256 * 0.7):
        return 1.0
    elif in_range(v, 256 * 0.7, 256):
        return 2.0


def get_rgb(image_path):
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hist_color = ['r', 'g', 'b']
    for i in range(0, 3):
        hist = cv2.calcHist([img], [i], None, [257], [0, 256])
        hist = cv2.normalize(hist, norm_type=cv2.NORM_L1).flatten()
        plt.plot(hist, color=hist_color[i])
        plt.xlim([0, 256])
        plt.show()


def get_hsv(image_path):
    image = cv2.imread(r'D:\ICBC\corel\693.jpg')
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist_color = ['r', 'g', 'b']
    hist = cv2.calcHist([img], [0], None, [180], [0, 180])
    hist = cv2.normalize(hist, norm_type=cv2.NORM_L1).flatten()
    plt.plot(hist, color=hist_color[0])
    plt.xlim([0, 180])
    plt.show()
    for i in range(1, 3):
        hist = cv2.calcHist([img], [i], None, [257], [0, 256])
        hist = cv2.normalize(hist, norm_type=cv2.NORM_L1).flatten()
        plt.plot(hist, color=hist_color[i])
        plt.xlim([0, 256])
        plt.show()

def get_3d_color(image_path):
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # hist = cv2.calcHist([image], [0, 1, 2], None, (8, 3, 3), [0, 180, 0, 256, 0, 256])
    # hist = cv2.normalize(hist).flatten()
    # plt.plot(hist, color='g')
    # plt.xlim([0, 72])

    im = np.array(img)
    temp = copy.deepcopy(im)
    ht = copy.deepcopy(im)

    width = im.shape[0]
    height = im.shape[1]

    for w in range(0, width):
        for h in range(0, height):
            temp[w, h, 0] = h_value(im[w, h, 0])
            temp[w, h, 1] = s_value(im[w, h, 1])
            temp[w, h, 2] = v_value(im[w, h, 2])
            ht[w, h, 0] = im[w, h, 0]/22.5
            ht[w, h, 1] = im[w, h, 1]/(256/3)
            ht[w, h, 2] = im[w, h, 2]/(256/3)

    hist = cv2.calcHist([temp], [0, 1, 2], None, (8, 3, 3), [0, 7, 0, 2, 0, 2])
    hist = [float(x) for x in cv2.normalize(hist, norm_type=cv2.NORM_L1).flatten()]
    plt.plot(hist, color='r')
    plt.xlim([0, 72])
    his = cv2.calcHist([ht], [0, 1, 2], None, (8, 3, 3), [0, 7, 0, 2, 0, 2])
    his = [float(x) for x in cv2.normalize(his, norm_type=cv2.NORM_L1).flatten()]
    plt.plot(his, color='g')
    plt.xlim([0, 72])
    plt.show()


def get_weight_array(image_path):
    image = cv2.imread(image_path)
    im = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    width = im.shape[0]
    height = im.shape[1]
    weight_array = np.zeros((width, height), np.uint8)
    # imagefeatures = []
    for w in range(0, width):
        for h in range(0, height):
            weight_array[w][h] = 9 * h_value(im[w, h, 0]) + 3 * s_value(im[w, h, 1]) + v_value(im[w, h, 2])
    return weight_array
    # hist = cv2.calcHist([weight_array], [0], None, [72], [0, 71])
    # hist = [float(x) for x in cv2.normalize(hist, norm_type=cv2.NORM_L1).flatten()]
    # plt.plot(hist, color='r')
    # plt.xlim([0, 72])
    # plt.show()


def histogram(image, mask=None):
    hist = cv2.calcHist([image], [0], mask, [72], [0, 71])
    hist = cv2.normalize(hist, norm_type=cv2.NORM_L1).flatten()
    plt.plot(hist, color='g')
    plt.xlim([0, 72])
    plt.show()


def get_partion_color(image_path):
    img = get_weight_array(image_path)
    (h, w) = img.shape[:2]
    (cX, cY) = (int(w * 0.5), int(h * 0.5))
    (axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
    ellipMask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
    cornerMask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(cornerMask, (0, 0), (w, h), 255, -1)
    cornerMask = cv2.subtract(cornerMask, ellipMask)
    histogram(img, ellipMask)
    histogram(img, cornerMask)


if __name__ == "__main__":
    image_path = r'D:\ICBC\corel\693.jpg'
    # get_rgb(image_path)
    # get_hsv(image_path)
    # get_3d_color(image_path)
    # get_weight_array(image_path)
    get_partion_color(image_path)