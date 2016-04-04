# -*- coding:utf-8 -*-
# __author__ = 'Michael'


from scenario.single import single_weight
import numpy as np
from warehouse.store import DB, get_mat_label
from log import Logger
from relief import relief_weight
logger = Logger(logname='log.txt', loglevel=1, logger="weight.py").getlog()
import matplotlib.pyplot as plt


def get_weight(dbname, types, labels):
    left_train = get_mat_label(labels[0], dbname, types, [0, 50])
    right_train = get_mat_label(labels[1], dbname, types, [0, 50])
    length = len(left_train[0, :])
    h = []
    for i in range(0, length):
        a = np.average(left_train[:, i])
        b = np.average(right_train[:, i])
        h.append(1 if a > b else -1)
    ht = np.vstack([left_train, right_train])
    weight = relief_weight(ht, labels, -0.01)
    wa = []
    for i in range(0, length):
        flag = weight[i] * h[i]
        # print flag
        if flag > 0:
            wa.append(21)
        elif flag < 0:
            wa.append(12)
        else:
            wa.append(0)
    return wa


def write_relief_weight(cat_name, basedb, types):
    db = DB(cat_name)
    for i in range(0, 10):
        for j in range(i+1, 10):
            labels = (i, j)
            label = str(i) + str(j)
            logger.info("process " + label + "  single weight to db!")
            weight = get_weight(basedb, types, labels)
            db.insert_data({"label": label, "weight": weight})
    logger.info("process all single weight to db!")



# def get_weight(dbname, types, labels):
#     left_train = get_mat_label(labels[0], dbname, types, [0, 50])
#     right_train = get_mat_label(labels[1], dbname, types, [0, 50])
#     # left_single = single_weight(left_train, 0.1)
#     # right_single = single_weight(right_train, 0.1)
#     #
#     # single = []
#     # for i in range(0, len(left_single)):
#     #     single.append(left_single[i] * right_single[i])
#     # ht = np.vstack([left_train, right_train])
#     # ht *= single
#     # weight = relief_weight(ht, labels, 0)
#     # wei = []
#     # for j in range(0, len(weight)):
#     #     wei.append(single[j] * weight[j])
#     ht = np.vstack([left_train, right_train])
#     weight = relief_weight(ht, labels, -0.01)
#     left_train *= weight
#     right_train *= weight
#     left_single = single_weight(left_train, 0.15)
#     right_single = single_weight(right_train, 0.15)
#     single = []
#     for i in range(0, len(left_single)):
#         single.append(left_single[i] * right_single[i] * weight[i])
#     wei = single
#     return wei



# def get_weighted_features(dbname, types, label):
#     train = get_mat_label(label, dbname, types, [0, 50])
#     res = single_weight(train, 1)
#     b = len(res)
#     flag = [i for i in range(0, b)]
#     # res = dict(zip(flag, res))
#     plt.axis([0.0, 0.1, -20, 120])
#     plt.xlabel("features value")
#     plt.ylabel("sample")
#     plt.title("features scatter plot")
#     plt.plot(res, flag, 'ro')
#     figname = r"d:/ims/" + chr(ord('a') + label) + r".png"
#     plt.savefig(figname)
#     plt.close()
#     # print res
#     print max(res)
#
#
# def show_features(dbname, types, label):
#     mat = get_mat_label(label, dbname, types, [0, 50])
#     index = [i for i in range(1, 51)]
#     a, b = mat.shape
#     res = single_weight(mat, 1)
#     flag = [i for i in range(1, b + 1)]
#     res = dict(zip(flag, res))
#     for i in range(0, b):
#         x = mat[:, i]
#         plt.axis([-0.2, 1.2, -10, 60])
#         plt.xlabel("features value")
#         plt.ylabel("sample")
#         plt.title("features scatter plot")
#         plt.plot(x, index, 'ro')
#         n = res[i + 1] * 10000
#         figname = r"d:/ims/" + chr(ord('a') + label) + str(n) + r".png"
#         plt.savefig(figname)
#         plt.close()
#     print res
#     print max(res.values())


if __name__ == '__main__':
    # wei = DB("weight")
    # left_weight = wei.find_one({"label": str(0)})["weight"]
    # print left_weight
    # write_single_weight(0.3)
    # print get_weight("color72", ["color"], (0, 1))
    write_relief_weight("ddd", "data", ["color", "lbp", "gabor"])
