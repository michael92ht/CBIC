__author__ = 'Michael'# -*- coding:utf-8 -*-
# __author__ = 'Michael'

from numpy import *


def L2dist(p1, p2):
    return sqrt(sum((p1 - p2) ** 2))


class KnnClassifier(object):

    def __init__(self, labels, samples):
        """使用训练数据初始化分类器"""

        self.labels = labels
        self.samples = samples

    def classify(self, point, k=3):
        """在训练数据上采用k近邻分类，并返回标记"""

        # 计算所有训练数据点的距离
        dist = array([L2dist(point, s) for s in self.samples])

        # 对它们进行排序
        ndx = dist.argsort()

        # 用字典存储k近邻
        votes = {}
        for i in range(k):
            label = self.labels[ndx[i]]
            votes.setdefault(label, 0)
            votes[label] += 1

        return max(votes)
