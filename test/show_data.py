__author__ = 'Michael'
#  -*- coding: utf-8 -*-

# import numpy as np
import matplotlib.pyplot as plt
# from scenario.prepare import get_mat_label
# from scenario.single import matix_standev
# from warehouse.store import get_mat_label
# # from scenario.relief import relief_data
#
# types = ["color"]
#
#
# def show(label):
#     mat = get_mat_label(label[0], "color44", ["color"], [0, 50])
#     index = [i for i in range(1, 51)]
#     a, b = mat.shape
#     # res = matix_standev(mat)
#     flag = [i for i in range(1, b + 1)]
#     # res = dict(zip(flag, res))
#     for i in range(0, b):
#         x = mat[:, i]
#         plt.axis([-0.2, 1.2, -10, 60])
#         plt.xlabel("features value")
#         plt.ylabel("sample")
#         plt.title("features scatter plot")
#         plt.plot(x, index, 'ro')
#     mat = get_mat_label(label[1], "color44", ["color"], [0, 50])
#     index = [i for i in range(1, 51)]
#     a, b = mat.shape
#     # res = matix_standev(mat)
#     flag = [i for i in range(1, b + 1)]
#     # res = dict(zip(flag, res))
#     for i in range(0, b):
#         x = mat[:, i]
#         plt.axis([-0.2, 1.2, -10, 60])
#         plt.xlabel("features value")
#         plt.ylabel("sample")
#         plt.title("features scatter plot")
#         plt.plot(x, index, 'gx')
#     figname = r"d:/imd/" + chr(ord('b') + label[1]) + r".png"
#     plt.savefig(figname)
#     plt.close()
#     # print res
#     # print max(res.values())


# def show2(labels, types):
#     mata = get_mat_label(labels[0], types, [0, 100])
#     matb = get_mat_label(labels[1], types, [0, 100])
#     index = [i for i in range(1, 101)]
#     a, b = mata.shape
#     # for i in range(0, b):
#     #     x = mata[:, i]
#     #     y = matb[:, i]
#     #     plt.axis([-0.2, 1.2, -20, 220])
#     #     plt.xlabel("features value")
#     #     plt.ylabel("sample")
#     #     plt.title("features scatter plot")
#     #     plt.plot(x, index, 'ro')
#     #     plt.plot(y, index, 'go')
#     #     figname = r"d:/ims/" + chr(ord('a') + labels[0]) + chr(ord('a') + labels[1]) + str(i) + r".png"
#     #     plt.savefig(figname)
#     #     plt.close()
#     data = np.vstack([mata, matb])
#     # wei = relief_data(data, labels, 0.1, 0)
#     # flag = [i for i in range(0, b)]
#     # res = dict(zip(flag, wei))
#     # sorted(wei, reverse=False)
#     # return wei
#
#
RES = [[0.56, 0.80, 0.56, 0.40, 1, 0.56, 0.8, 1, 0.42, 0.46],
       [0.74, 0.66, 0.94, 0.38, 1, 0.1, 0.52, 0.9, 0.2, 0.38],
       [0.42, 0.26, 0.64, 0.8, 1, 0.08, 0.96, 0.16, 0.74, 0.58],
       [0.74, 0.68, 0.92, 0.86, 1, 0.4, 0.98, 0.98, 0.54, 0.72],
       [0.8, 0.74, 0.86, 0.82, 1, 0.54, 0.94, 0.96, 0.56, 0.72],
       [0.86, 0.94, 0.86, 0.72, 1, 0.92, 1, 0.96, 0.86, 0.76],
       [0.72, 0.84, 0.9, 0.3, 0.98, 0.32, 0.88, 0.96, 0.7, 0.32],
       [0.42, 0.22, 0.84, 0.96, 1, 0.14, 1, 0.16, 0.8, 0.56]]

rate = [63.6, 60.2, 55.6, 79.4, 81.6, 80.6, 79]

COL = [r"--xg", r"--xy", r"--xb", r"-or"]


def show_integrated():
    index = [i for i in range(1, 11)]
    plt.axis([-1, 11, -0.1, 1.1])
    plt.xlabel("classes")
    plt.ylabel("accuracy rate")
    plt.title("Accuracy constrast figure")
    plot0 = plt.plot(index, RES[0], COL[0], label="color44")[0]
    plot1 = plt.plot(index, RES[1], COL[1], label="lbp")[0]
    plot2 = plt.plot(index, RES[2], COL[2], label="gabor")[0]
    plot3 = plt.plot(index, RES[3], COL[3], label="integrated")[0]
    plt.legend(handles=[plot0, plot1, plot2, plot3], loc=3, numpoints=1)
    # plt.legend([plot0, plot1, plot2, plot3], ("color", "lbp", "gabor", "merge"), numpoints=3)
    figname = r"d:/ims/" + r"res.png"
    plt.savefig(figname)
    plt.close()


# def show_weighted():
#     index = [i for i in range(1, 11)]
#     plt.axis([-1, 11, 0, 1.1])
#     plt.xlabel("classes")
#     plt.ylabel("accuracy rate")
#     plt.title("Accuracy constrast figure")
#     plot0 = plt.plot(index, RES[1], COL[3], label="test_data_huang")[0]
#     plot1 = plt.plot(index, RES[5], COL[0], label="train_data_huang")[0]
#     plt.legend(handles=[plot0, plot1], loc=3, numpoints=1)
#     # plt.legend([plot0, plot1, plot2, plot3], ("color", "lbp", "gabor", "merge"), numpoints=3)
#     figname = r"d:/ims/" + r"lbphuang.png"
#     plt.savefig(figname)
#     plt.close()
#
#
# def show_r():
#     index = [i for i in range(1, 11)]
#     plt.axis([-1, 11, 0.2, 1.1])
#     plt.xlabel("classes")
#     plt.ylabel("accuracy rate")
#     plt.title("Accuracy constrast figure")
#     plot0 = plt.plot(index, RES[5], COL[0], label="weighted r=0.001")[0]
#     plot2 = plt.plot(index, RES[6], COL[2], label="weighted r=0")[0]
#     plot1 = plt.plot(index, RES[4], COL[3], label="weighted r=0.0001")[0]
#     # plot3 = plt.plot(index, RES[3], COL[0], label="integrated")[0]
#     plt.legend(handles=[plot0, plot1, plot2], loc=3, numpoints=1)
#     # plt.legend([plot0, plot1, plot2, plot3], ("color", "lbp", "gabor", "merge"), numpoints=3)
#     figname = r"d:/ims/" + r"resdt.png"
#     plt.savefig(figname)
#     plt.close()


def show_weighted():
    index = [i for i in range(1, 11)]
    plt.axis([-1, 11, 0, 1.1])
    plt.xlabel("classes")
    plt.ylabel("accuracy rate")
    plt.title("Accuracy constrast figure")
    plot0 = plt.plot(index, RES[0], COL[3], label="test_data_huang")[0]
    plot1 = plt.plot(index, RES[1], COL[3], label="test_data_huang")[0]
    plot2 = plt.plot(index, RES[2], COL[3], label="test_data_huang")[0]
    plot3 = plt.plot(index, RES[5], COL[0], label="train_data_huang")[0]
    plot4 = plt.plot(index, RES[6], COL[0], label="train_data_huang")[0]
    plot5 = plt.plot(index, RES[7], COL[0], label="train_data_huang")[0]
    plt.legend(handles=[plot2, plot5], loc=3, numpoints=1)
    # plt.legend([plot0, plot1, plot2, plot3], ("color", "lbp", "gabor", "merge"), numpoints=3)
    figname = r"d:/imd/" + r"huang.png"
    plt.savefig(figname)
    plt.close()

if __name__ == "__main__":
    # show_integrated()
    show_weighted()

