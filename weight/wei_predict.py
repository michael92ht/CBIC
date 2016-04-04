# -*- coding:utf-8 -*-
# __author__ = 'Michael'


import os
from svmutil import *
import collections
from log import Logger
import numpy as np

# 设置log
logger = Logger(logname='result.txt', loglevel=1, logger="result").getlog()

MODEL_PATH = r'D:\ICBC\data\weight\model'
PREDICT_PATH = r'D:\ICBC\data\weight\test'


def classify(y, x, model_name):
    total = len(y)
    res = []
    for i in range(0, total):
        t = []
        t.append(x[i])
        h = []
        h.append(y[i])
        model = svm_load_model(model_name)
        p_label, p_acc, p_val = svm_predict(h, t, model)
        res.append(p_label[0])
    return res


def wei_test(class_name):
    result = []
    for i in range(0, 10):
        for j in range(i+1, 10):
            label = str(i) + str(j)
            predict_file = os.path.join(PREDICT_PATH, class_name + r'_scale' + label + r".txt")
            model_name = os.path.join(MODEL_PATH + "\\" + class_name, class_name + r'_train_' + label + r".txt.model")
            y, x = svm_read_problem(predict_file)
            res = classify(y, x, model_name)
            result.append(res)
    h = result[0]
    for i in range(1, 45):
        h = np.vstack([h, result[i]])
    column = h.shape[1]
    r = []
    for i in range(0, column):
        x = h[:, i]
        r.append(collections.Counter(x).most_common(1)[0][0])
    flag = []
    correct_list = {}
    for num in range(0, 10):
        flag.extend([num] * 50)
        correct_list[num] = 0
    count = 0
    for index in range(0, 500):
        if r[index] == flag[index]:
            correct_list[flag[index]] += 1
            count += 1
    logger.info("class name: " + class_name)
    res = "rate: " + str(count) + " " + str(float(count)/float(500)*100) + r'%'
    logger.info(res)
    rate = []
    for cor in correct_list.values():
        rate.append(float(cor)/float(50) * 100)
    logger.info("rate list: " + str(rate))


if __name__ == "__main__":
    class_name = r'ch15'

    wei_test(class_name)
