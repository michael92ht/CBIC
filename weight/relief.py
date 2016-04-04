# -*- coding:utf-8 -*-
# __author__ = 'Michael'


import numpy as np
from warehouse.store import DB, get_mat_label
from log import Logger
logger = Logger(logname='log.txt', loglevel=1, logger="weight.py").getlog()


weight = [[1, 1, 1], [1, 1, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 1, 0], [1, 1, 1], [1, 0, 1]]
# weight = [[1, 1, 0], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 0, 1], [1, 0, 1]]
para = [44, 59, 48]
# weight = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 1, 0], [1, 1, 1], [1, 1, 1]]
# 78.2% weight = [[1, 1, 1], [1, 1, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 1, 0], [1, 1, 1], [1, 1, 1]]


def calute_weight(labels):
    i, j = labels[0], labels[1]
    h = []
    wei = []
    for index in range(0, 3):
        h.append(weight[i][index] * weight[j][index])
    for m in range(0, 3):
        wei.extend([h[m]] * para[m])
    if sum(wei) <= 60:
        wei = [1] * 151
    return wei


def write_weight(weight_name):
    db = DB(weight_name)
    for i in range(0, 10):
        for j in range(i+1, 10):
            labels = (i, j)
            label = str(i) + str(j)
            logger.info("process " + label + "  single weight to db!")
            weight = calute_weight(labels)
            db.insert_data({"label": label, "weight": weight})
    logger.info("process all single weight to db!")


def get_weighted_features(weight_db, mat, labels):
    left_label, right_label = labels[0], labels[1]
    wei = DB(weight_db)
    weight = wei.find_one({"label": str(left_label)+str(right_label)})["weight"]
    row, column = mat.shape
    print column
    tmat = []
    wei = []
    for i in range(0, column):
        if weight[i] - 0 > 0.0001:
            x = mat[:, i]
            tmat.append(x)
            wei.append(weight[i])
    tmat = np.array(tmat).T
    data = tmat * wei
    return data


if __name__ == '__main__':
    # print calute_weight(0, 1)
    write_weight("weight15")