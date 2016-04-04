# -*- coding:utf-8 -*-
# __author__ = 'Michael'

from __future__ import division
import numpy as np


# 定义范围函数，判断数值是否在该范围内(]
def in_range(number, left, right):
    return left < number <= right


# 经典72级非均匀量化模式，8*3*3
class HsvQua72:
    def __init__(self):
        pass

    mode = "Hsv Qua 72"

    @staticmethod
    def qua_h(h):     # 对h分量进行量化
        range_list = [12.5, 20.5, 37.5, 78, 100.5, 136, 142.5, 165]
        for index in range(0, len(range_list) - 1):
            if in_range(h, range_list[index], range_list[index + 1]):
                return index + 1
        return 0

    @staticmethod
    def qua_s(s):     # 对s分量进行量化
        range_list = [float(x * 255) for x in [0, 0.2, 0.7, 1]]
        for index in range(0, len(range_list) - 1):
            if in_range(s, range_list[index], range_list[index + 1]):
                return index
        return 0

    @staticmethod
    def qua_v(v):     # 对v分量进行量化
        range_list = [float(x * 255) for x in [0, 0.2, 0.7, 1]]
        for index in range(0, len(range_list) - 1):
            if in_range(v, range_list[index], range_list[index + 1]):
                return index
        return 0

    @staticmethod
    def calute(imdata):   # 计算量化后的图像数组
        width = imdata.shape[0]
        height = imdata.shape[1]
        qudata = np.zeros((width, height), np.uint8)
        for wid in range(0, width):
            for hei in range(0, height):
                h = HsvQua72.qua_h(imdata[wid, hei, 0])
                s = HsvQua72.qua_s(imdata[wid, hei, 1])
                v = HsvQua72.qua_v(imdata[wid, hei, 2])
                qudata[wid][hei] = 9 * h + 3 * s + v
        return qudata


# 20级非均匀量化模式，8*2+4
class HsvQua20:
    def __init__(self):
        pass

    mode = "Hsv Qua 20"

    @staticmethod
    def qua_h(h):     # 对h分量进行量化
        range_list = [10, 20, 37.5, 77.5, 95, 135, 147.5, 157.5]
        for index in range(0, len(range_list) - 1):
            if in_range(h, range_list[index], range_list[index + 1]):
                return index + 1
        return 0

    @staticmethod
    def qua_s(s):     # 对s分量进行量化
        range_list = [0.1, 0.65, 1]
        for index in range(0, len(range_list) - 1):
            if in_range(s, range_list[index], range_list[index + 1]):
                return index
        return 0

    @staticmethod
    def calute(imdata):   # 计算量化后的图像数组
        width = imdata.shape[0]
        height = imdata.shape[1]
        qudata = np.zeros((width, height), np.uint8)
        for wid in range(0, width):
            for hei in range(0, height):
                h, s, v = imdata[wid, hei]
                s /= 255
                v /= 255
                quaval = 0
                if 0 <= v <= 0.15:
                    quaval = 16
                elif 0 <= s <= 0.1:
                    if in_range(v, 0.15, 0.65):
                        quaval = 17
                    elif in_range(v, 0.65, 0.9):
                        quaval = 18
                    else:
                        quaval = 19
                else:
                    quaval = HsvQua20.qua_h(h) * 2 + HsvQua20.qua_s(s)
                qudata[wid][hei] = quaval
        return qudata


# 44级非均匀量化模式，8*3 + 8*2 + 4
class HsvQua44:
    def __init__(self):
        pass

    mode = "Hsv Qua 44"

    @staticmethod
    def qua_h(h):     # 对h分量进行量化
        # range_list = [10, 20, 37.5, 77.5, 95, 135, 147.5, 157.5]
        range_list = [12.5, 20.5, 37.5, 78, 100.5, 136, 142.5, 165]
        for index in range(0, len(range_list) - 1):
            if in_range(h, range_list[index], range_list[index + 1]):
                return index + 1
        return 0

    @staticmethod
    def qua_s(s, mode=0):     # 对s分量进行量化
        # sat_list = [[0.1, 0.2, 0.75, 1], [0.1, 0.65, 1]]
        sat_list = [[0.1, 0.3, 0.75, 1], [0.1, 0.65, 1]]
        cur_list = sat_list[mode]
        for index in range(0, len(cur_list) - 1):
            if in_range(s, cur_list[index], cur_list[index + 1]):
                return index
        return 0

    @staticmethod
    def calute(imdata):   # 计算量化后的图像数组
        width = imdata.shape[0]
        height = imdata.shape[1]
        qu_data = np.zeros((width, height), np.uint8)
        for wid in range(0, width):
            for hei in range(0, height):
                h, s, v = imdata[wid, hei]
                s /= 255
                v /= 255
                qua_val = 0
                if 0 <= v <= 0.15:
                    qua_val = 40
                elif 0 <= s <= 0.1:
                    if in_range(v, 0.15, 0.65):
                        qua_val = 41
                    elif in_range(v, 0.65, 0.9):
                        qua_val = 42
                    else:
                        qua_val = 43
                elif in_range(v, 0.5, 1):
                    qua_val = HsvQua44.qua_h(h) * 3 + HsvQua44.qua_s(s, 0)
                elif in_range(v, 0.15, 0.5):
                    qua_val = HsvQua44.qua_h(h) * 2 + HsvQua44.qua_s(s, 1) + 24
                qu_data[wid][hei] = qua_val
        return qu_data


# 36级非均匀量化模式，8*4 + 4
class HsvQua36:
    def __init__(self):
        pass

    mode = "Hsv Qua 36"

    @staticmethod
    def qua_h(h):     # 对h分量进行量化
        range_list = [10, 20, 37.5, 77.5, 95, 135, 147.5, 157.5]
        for index in range(0, len(range_list) - 1):
            if in_range(h, range_list[index], range_list[index + 1]):
                return index + 1
        return 0

    @staticmethod
    def qua_s(s, mode=0):     # 对s分量进行量化
        sat_list = [0.1, 0.7, 1]
        cur_list = sat_list[mode]
        for index in range(0, len(cur_list) - 1):
            if in_range(s, cur_list[index], cur_list[index + 1]):
                return index
        return 0

    @staticmethod
    def calute(imdata):   # 计算量化后的图像数组
        width = imdata.shape[0]
        height = imdata.shape[1]
        qu_data = np.zeros((width, height), np.uint8)
        for wid in range(0, width):
            for hei in range(0, height):
                h, s, v = imdata[wid, hei]
                s /= 255
                v /= 255
                qua_val = 0
                if 0 <= v <= 0.15:
                    qua_val = 32
                elif 0 <= s <= 0.1:
                    if in_range(v, 0.15, 0.65):
                        qua_val = 33
                    elif in_range(v, 0.65, 0.9):
                        qua_val = 34
                    else:
                        qua_val = 35
                elif in_range(v, 0.6, 1):
                    qua_val = HsvQua44.qua_h(h) * 2 + HsvQua44.qua_s(s, 1)
                elif in_range(v, 0.15, 0.6):
                    qua_val = HsvQua44.qua_h(h) * 2 + HsvQua44.qua_s(s, 1) + 16
                qu_data[wid][hei] = qua_val
        return qu_data


# 测试用模型
class HsvQuaTest:
    def __init__(self):
        pass

    mode = "Hsv Qua test"

    @staticmethod
    def qua_h(h):     # 对h分量进行量化
        range_list = [10, 20, 37.5, 77.5, 95, 135, 147.5, 157.5]
        for index in range(0, len(range_list) - 1):
            if in_range(h, range_list[index], range_list[index + 1]):
                return index + 1
        return 0

    @staticmethod
    def qua_s(s):     # 对s分量进行量化
        range_list = [float(x * 255) for x in [0, 0.4, 0.7, 1]]
        for index in range(0, len(range_list) - 1):
            if in_range(s, range_list[index], range_list[index + 1]):
                return index
        return 0

    @staticmethod
    def qua_v(v):     # 对v分量进行量化
        range_list = [float(x * 255) for x in [0.1, 0.35, 0.7, 1]]
        for index in range(0, len(range_list) - 1):
            if in_range(v, range_list[index], range_list[index + 1]):
                return index
        return 0

    @staticmethod
    def calute(imdata):   # 计算量化后的图像数组
        width = imdata.shape[0]
        height = imdata.shape[1]
        qudata = np.zeros((width, height), np.uint8)
        for wid in range(0, width):
            for hei in range(0, height):
                h, s, v = imdata[wid, hei]
                qua_val = 0
                if v <= 25.5:
                    qua_val = 72
                elif s <= 25.5:
                    if in_range(v, 0.15 * 255, 0.65 * 255):
                        qua_val = 73
                    elif in_range(v, 0.65 * 255, 0.9 * 255):
                        qua_val = 74
                    else:
                        qua_val = 75
                else:
                    qua_val = 9 * HsvQuaTest.qua_h(h) + HsvQuaTest.qua_s(s) * 3 + HsvQuaTest.qua_v(v)
                qudata[wid][hei] = qua_val
        return qudata

if __name__ == "__main__":
    print HsvQuaTest.mode
    pass

