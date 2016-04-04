__author__ = 'Michael'
#  -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os


def read_features(filepath):
    index = 0
    with open(filepath, 'r') as f:
        for line in f.readlines():
            temp = []
            for num in line.split(" ")[1:]:
                fea = num.split(":")
                if fea != ["\n"] and fea != [""]:
                    temp.append(float(fea[1]))
            if index == 0:
                data = np.array(temp)
                index = 2
            else:
                data = np.vstack([data, temp])

    return data


def show(filename):
    im = os.path.basename(filename).split('.')[0]
    data = read_features(filename)
    length = data.shape[1]
    index = [i for i in range(1, 51)]
    flag = [i for i in range(1, length + 1)]
    for i in range(0, 50):
        x = data[i]
        plt.axis([-5, length + 5, -1.2, 1.2])
        plt.ylabel("features value")
        plt.xlabel("features index")
        plt.title(im)
        plt.plot(flag, x, 'rx')
    figname = r"d:/huang/" + im + r".png"
    plt.savefig(figname)
    plt.close()


if __name__ == "__main__":
    for imdata in os.listdir(r"D:\ICBC\train_data"):
        filename = os.path.join(r"D:\ICBC\train_data", imdata)
        show(filename)


