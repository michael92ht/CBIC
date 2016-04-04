# __author__ = 'Michael'
#  -*- coding: utf-8 -*-
#  主要包括图像特征的数据库操作

from pylab import *
import pymongo
from multiprocessing import Pool
import os
from log import Logger
from imagefeatures import color, lbp, gabor, gaborlbp


logger = Logger(logname='log.txt', loglevel=1, logger="store.py").getlog()


# mongodb 类
class DB:
    def __init__(self, dbname):
        try:
            self.client = pymongo.MongoClient()
            logger.info("Open database.......")
            self.use(dbname)
        except e:
            logger.error("Can\'t open database!")

    def __del__(self):
        self.client.close()

    # 使用数据库,返回collection
    def use(self, dbname):
        logger.info("opening datebase :" + dbname)
        self.db = self.client[dbname]
        self.collection = self.db.my_collection
        return self.collection

    # 更新数据库某项
    def update_data(self, data, setdata):
        if type(data) is not dict or type(setdata) is not dict:
            logger.error('the type of update and data isn\'t dict')
        else:
            self.collection.update(data, {'$set': setdata})

    # 删除数据库某项
    def remove_data(self, data):
        if type(data) is not dict:
            logger.error('the type of update and data isn\'t dict')
        else:
            self.collection.remove(data)

    # 插入某项到数据库
    def insert_data(self, data):
        if type(data) is not dict:
            logger.error('the type of update and data isn\'t dict')
        else:
            self.collection.insert(data)

    # 查询
    def find(self, query={}):
        if type(query) is not dict:
            logger.error('the type of update and data isn\'t dict')
        else:
            try:
                if not self.collection:
                    logger.error("Don\'t assign the collection!")
                else:
                    res = self.collection.find(query)
                    logger.info('find the data:' + str(query))
                    return res
            except e:
                logger.error(e)

    def find_one(self, query={}):
        try:
            return self.find(query)[0]
        except e:
            logger.error(e)


# 删除指定数据库
def delete_db(dbname):
    client = pymongo.MongoClient()
    if dbname in client.database_names():
        client.drop_database(dbname)
        logger.info("Remove datebase :" + dbname)
    else:
        logger.error("The datebase :" + dbname + " is not exist!")


# 将矩阵归一化
def norm(x):
    maxval = max(x)
    minval = min(x)
    denval = maxval - minval
    y = []
    if denval == 0:
        y = [1.0] * len(x)
    else:
        for val in x:
            newval = float(val - minval) / denval
            y.append(newval)
    return y


# 获取图像的所有特征
def image_features(image_path):
    logger.info("get features of image: " + image_path)
    features = {"gabor": gabor.gabor_features(image_path)}
    # features = {"lbp": lbp.uniform_features(image_path)}
    # features = {"gabor": gaborlbp.gabor_features(image_path, ht[0], ht[1])}
    # features = {"color": color.global_features(image_path, 1)}
    # features.update({"color": color.global_features(image_path, 1)})
    # features.update({"lbp": lbp.uniform_features(image_path)})
    # features.update({"gabor": gabor.gabor_features(image_path)})
    return features


#  存储 { 分类标记，训练库索引，特征值 } 到数据库
def save_2_db(dbname, image_path, features):
    index = int(os.path.basename(image_path).split('.')[0])
    post = {"label": int(index / 100), "index": index}
    post.update(features)
    logger.info("Insert the data of image: " + image_path + " to " + dbname)
    db = DB(dbname)
    db.insert_data(post)


# 获取图像特征并存储到数据库
def save_features((dbname, image_path)):
    features = image_features(image_path)
    logger.info("processing: " + image_path)
    save_2_db(dbname, image_path, features)


# 从图像文件夹中获得图像列表
def images_from_folder(image_folder):
    logger.info("Get image list of " + image_folder)
    return [os.path.join(image_folder, f) for f in os.listdir(image_folder) if 'jpg' in f]


# 批量将图像特征库中的图像提取其特征到指定数据库
def batch_save(dbname, image_folder):
    logger.info("Begin batch save image features of folder: " + image_folder + " to " + dbname)
    image_list = images_from_folder(image_folder)
    save_list = [(dbname, image) for image in image_list]
    pool = Pool()
    pool.map(save_features, save_list)
    pool.close()
    pool.join()


# 合并两个数据库到新的数据库
def merge_2db(db_one, db_two, db_new):
    left = DB(db_one).collection
    right = DB(db_two).collection
    newdb = DB(db_new).collection
    posts = list(left.find().sort('index', pymongo.ASCENDING))
    for pos in posts:
        label = pos['label']
        index = pos['index']
        color = pos["color"]
        gabor = pos["gabor"]
        lbp = right.find_one({"index": index})['lbp']
        newdb.insert({"index": index, "label": label, "color": color, "lbp": lbp, "gabor": gabor})
        # gabor = pos["gabor"]
        # lbp = pos['lbp']
        # color = right.find_one({"index": index})['colorlbp']
        # newdb.insert({"index": index, "label": label, "color": color, "lbp": lbp, "gabor": gabor})


# 更新数据库的新数据
def bulid_from_db(db_one, db_two):
    left = DB(db_one).collection
    right = DB(db_two).collection
    posts = list(right.find().sort('index', pymongo.ASCENDING))
    for pos in posts:
        if not pos.has_key("color"):
            index = pos["index"]
            # color = pos['color']
            # lbp = pos['lbp']
            gabor = pos['gabor']
            label = pos['label']
            # left.insert({"index": index, "label": label, "color": color, "lbp": lbp, "gabor": gabor})
            left.insert({"index": index, "label": label, "gabor": gabor})

# 更新数据库的新数据
def modify_db(db_name):
    db = DB(db_name)
    posts = list(db.find().sort('index', pymongo.ASCENDING))
    for pos in posts:
        db.update_data({"index": pos["index"]}, {"label": int(pos["label"])})


# 从数据库中选择使用的图像特征模式
def get_features(post, types):
    features = []
    for tp in types:
        features.extend(post[tp])
    return features


# 根据标记值取得指定范围内的数据
def get_mat_label(label, db_name, tps, pair):
    db = DB(db_name)
    posts = list(db.find({"label": label}).sort('index', pymongo.ASCENDING))
    left, right = pair[0], pair[1]
    features = get_features(posts[left], tps)
    for index in range(left+1, right):
        features = np.vstack([features, get_features(posts[index], tps)])
    return features


if __name__ == "__main__":
    # merge_2db("ht", "gabor32", "data")
    # image_folder = r"D:\ICBC\corel"
    # dbname = "gabor"
    # batch_save(dbname, image_folder)
    # bulid_from_db("test", "images")
    merge_2db("temp", "lbp", "ht")
    print "-------------------finshed!------------------------"

