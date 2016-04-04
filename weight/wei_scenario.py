# __author__ = 'Michael'
#  -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import os
import shutil
from warehouse.store import get_mat_label
from relief import get_weighted_features

TEMP_PATH = r'D:\ICBC\data\weight\temp'
PREDICT_PATH = r'D:\ICBC\data\weight\test'
MODEL_PATH = r'D:\ICBC\data\weight\model'
EASY = r'D:\ImageProcess\svmtools\easy.py'
SCALE = r"D:\ICBC\software\libsvm-3.20\windows\svm-scale.exe"


# 将得到的一个{ 图像分类标志,图像特征 }写入指定文件
def write_svm_data(filename, label, features):
    for line in features:
        flag = [i for i in range(1, len(line)+1)]
        context = dict(zip(flag, line))
        with open(filename, 'a') as f:
            f.write(str(label)+' ')
            for key in context.keys():
                f.write(str(key))
                f.write(':')
                f.write(str(float(context[key])) + ' ')
            f.write('\n')


# 将预测数据进行缩放处理
def scale_data(predict_file, scale_file):
    if os.path.exists(scale_file):
        os.remove(scale_file)
    comd = SCALE + ' ' + predict_file + r'>' + scale_file
    os.system(comd)
    os.remove(predict_file)
    print "created ", scale_file


# 为多分类训练模型准备指定分类的测试文件
def create_predict(cat, dbname, label, tps):
    print "processing label: ", label
    predict_file = cat + r'_predict' + r'.txt'
    predict_file = os.path.join(PREDICT_PATH, predict_file)
    features = get_mat_label(label, dbname, tps, (50, 100))
    write_svm_data(predict_file, label, features)
    print "finished create predict file."


# 为两个不同的分类的图像特征，分别创建训练文件（前50）与测试文件（后50）
def create_data_2_label(cat, dbname, weight_db, labels, tps):
    left_label, right_label = labels[0], labels[1]
    print "processing: label ", left_label, " and ", right_label
    train_file = cat + r"_train_" + str(left_label) + str(right_label)+r'.txt'
    train_file = os.path.join(TEMP_PATH, train_file)
    if os.path.exists(train_file):
        os.remove(train_file)
    left_train = get_mat_label(left_label, dbname, tps, (0, 50))
    right_train = get_mat_label(right_label, dbname, tps, (0, 50))
    mat = np.vstack([left_train, right_train])
    data = get_weighted_features(weight_db, mat, labels)
    # data = get_weight_features(weight_db, left_train, right_train, labels)
    left_train = data[:50]
    right_train = data[50:]
    write_svm_data(train_file, right_label, right_train)
    write_svm_data(train_file, left_label, left_train)


# 为多分类创建总的测试文件,并使用svm—scale进行数据缩放
def auto_create_predict(cat, dbname, weight_db, types=["color", "lbp", "gabor"]):
    print "prepare for predict file."
    for i in range(0, 10):
        for j in range(i+1, 10):
            test_file = os.path.join(PREDICT_PATH, cat + r'_predict' + str(i) + str(j) + r'.txt')
            for index in range(0, 10):
                mat = get_mat_label(index, dbname, types, (50, 100))
                data = get_weighted_features(weight_db, mat, (i, j))
                # data = get_weight_features(weight_db, mat[:50], mat[50:],(i, j))
                write_svm_data(test_file, index, data)
            scale_file = os.path.join(PREDICT_PATH, cat + r'_scale' + str(i) + str(j) + r'.txt')
            scale_data(test_file, scale_file)


# 为多分类创建所有的准备以及测试文件
def auto_create_all(cat, dbname, weight_db, tps):
    for i in range(0, 10):
        for j in range(i+1, 10):
            create_data_2_label(cat, dbname, weight_db, (i, j), tps)


# 为多分类创建分类模型
def create_model(cat_name, num=10):
    print "prepare train and predict data."
    cur_place = os.getcwd()
    work_place = os.path.join(MODEL_PATH, cat_name)
    if os.path.exists(work_place):
        shutil.rmtree(work_place)
    os.makedirs(work_place)
    os.chdir(work_place)
    for i in range(0, num):
        for j in range(i+1, num):
            train_file = os.path.join(TEMP_PATH, cat_name + r"_train_" + str(i) + str(j) + r'.txt')
            com = EASY + ' ' + train_file + ' ' + train_file
            os.system(com)

    print "clearing useless data."
    for f in os.listdir(work_place):
        if not f.endswith('model'):
            os.remove(work_place + '\\' + f)

    for f in os.listdir(TEMP_PATH):
        os.remove(os.path.join(TEMP_PATH, f))
    os.chdir(cur_place)
    print "create model for all class done!"


def wei_train(cat_name, dbname, weight_db, types):
    auto_create_all(cat_name, dbname, weight_db, types)
    create_model(cat_name)
    auto_create_predict(cat_name, dbname, weight_db, types)


if __name__ == "__main__":
    types = ["color", "lbp", "gabor"]
    wei_train("ch15", "ht", "weight15", types)
