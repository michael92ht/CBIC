# -*- coding:utf-8 -*-
# __author__ = 'Michael'


import os
from svmutil import *
import collections
from log import Logger


# 设置log
logger = Logger(logname='result0.txt', loglevel=1, logger="nor_predict.py").getlog()


MODEL_PATH = r'D:\ICBC\data\normal\model'
PREDICT_PATH = r'D:\ICBC\data\normal\test'


def classify(y, x, nmodel):
    res = []
    for m in os.listdir(nmodel):
        model_name = nmodel + '\\' + m
        print model_name
        model = svm_load_model(model_name)
        p_label, p_acc, p_val = svm_predict(y, x, model)
        res.extend(p_label)
    return collections.Counter(res).most_common(1)[0][0]


def nor_test(class_name, num=10):
    predict_file = os.path.join(PREDICT_PATH, class_name + r'_scale.txt')
    nmodel = os.path.join(MODEL_PATH, class_name)
    y, x = svm_read_problem(predict_file)
    count = 0
    total = len(y)
    error_list = {}
    for i in range(0, num):
        error_list[i] = 0
    for i in range(0, total):
        tmp = []
        tmp.append(x[i])
        h = []
        h.append(y[i])
        label = classify(h, tmp, nmodel)
        if label == y[i]:
            count += 1
        else:
            error_list[y[i]] += 1
    logger.info("class name: " + class_name)
    res = "rate: " + str(count) + " " + str(total) + " " + str(float(count)/float(total)*100) + r'%'
    logger.info(res)
    rate = []
    for err in error_list.values():
        rate.append(float(50 - err)/float(50) * 100)
    logger.info("rate list: " + str(rate))
    return float(count)


if __name__ == "__main__":
    class_name = r'lbp'
    nor_test(class_name)
