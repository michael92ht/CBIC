# -*- coding:utf-8 -*-
# __author__ = 'Michael'


import os
import shutil
from log import Logger
from normal.nor_predict import nor_test
from normal.nor_scenario import nor_train
from warehouse.store import batch_save, delete_db


# 设置log
logger = Logger(logname='result0.txt', loglevel=1, logger="meta.py").getlog()
DATA = r"D:\ICBC\data"


def remove_all_model(dbname, mode):
    work_place = os.path.join(DATA, mode)
    model_path = os.path.join(os.path.join(work_place, "model"), dbname)
    predict_path = os.path.join(work_place, "test")
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    logger.info("Remove model path: " + model_path)
    if os.path.exists(predict_path):
        for f in os.listdir(predict_path):
            os.remove(os.path.join(predict_path, f))
    logger.info("Remove predict path: " + predict_path)
    delete_db(dbname)
    logger.info("Remove datebase: " + dbname)


def normal_test(cat, types):
    logger.info("feature: gabor")
    image_folder = r"D:\ICBC\corel"
    batch_save(cat, image_folder)
    nor_train(cat, types)
    nor_test(cat)
    remove_all_model(cat, "normal")

if __name__ == "__main__":
    cat = "gabor"
    types = ["gabor"]
    normal_test(cat, types)

