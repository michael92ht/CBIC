# -*- coding:utf-8 -*-
# __author__ = 'Michael'

import os
from svmutil import *
import collections
from log import Logger

# 设置log
logger = Logger(logname='result.txt', loglevel=1, logger="result").getlog()

MODEL_PATH = r'D:\ImageProcess\data\normal\model'
PREDICT_PATH = r'D:\ImageProcess\data\normal\predict'
MODEL = [os.path.join(MODEL_PATH, x) for x in ["color_temp", "lbp_uniform", "gabor_test"]]


def classify(y, x, nmodel):
    res = []
    for m in os.listdir(nmodel):
        model_name = nmodel + '\\' + m
        print model_name
        model = svm_load_model(model_name)
        p_label, p_acc, p_val = svm_predict(y, x, model)
        res.extend(p_label)
    return collections.Counter(res).most_common(1)[0][0]


def predict_n(class_name, num=10):
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
        # print x[i], type(x[i])
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


def predict_classer(class_name, num=10):
    predict_file = os.path.join(PREDICT_PATH, class_name + r'_scale.txt')
    nmodel = os.path.join(MODEL_PATH, class_name)
    y, x = svm_read_problem(predict_file)
    count = 0
    total = len(y)
    res = []
    for i in range(0, total):
        tmp = []
        tmp.append(x[i])
        h = []
        h.append(y[i])
        label = classify(h, tmp, nmodel)
        res.append(label)
    return res


def predict_multi(class_name, num=10):
    predict_file = os.path.join(PREDICT_PATH, "mmm" + class_name + r'.txt')
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
        # print x[i], type(x[i])
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
    for err in error_list:
        rate.append(float(err)/float(50))
    logger.info("rate list: " + str(rate))
    return float(count)


def classifier():
    count = 0
    for i in range(0, 3):
        prefile = os.path.join(PREDICT_PATH, str(i) + "scale.txt")
        y, x = svm_read_problem(prefile)
        total = len(y)
        for j in range(0, total):
            tmp = []
            tmp.append(x[j])
            h = []
            h.append(y[j])
            label = classify(h, tmp, MODEL[i])
            if label == y[j]:
                count += 1
    res = "rate: " + str(count) + " " + str(400) + " " + str(float(count)/float(400)*100) + r'%'
    print res


if __name__ == "__main__":
    # s = 0
    # for el in ["color", "lbp", "gabor"]:
    #     s += predict_multi(el)
    # print float(s)/float(360)
    # classifier()
    class_name = r'color72'
    predict_n(class_name)
    # res = predict_classer(class_name, 3)
    # print res