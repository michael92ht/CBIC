# -*- coding:utf-8 -*-
# __author__ = 'Michael'

import logging

logdir = r"D:\ICBC\data\logs"
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Logger:
    def __init__(self, logname, loglevel, logger):
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        logname = logdir + r"\\" + logname
        fh = logging.FileHandler(logname)
        fh.setLevel(loglevel)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)

        # 定义handler的输出格式
        formatter = format
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

