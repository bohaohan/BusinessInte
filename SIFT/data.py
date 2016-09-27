# -*- coding: UTF-8 -*-
__author__ = 'bohaohan'
import os
# from passage.models import RNN
from PIL import Image
# from detect import *
from SIFT.pre_pro import *
logos = ['Acura讴歌','Armani阿玛尼','AstonMartin阿斯顿马丁','Audi奥迪','Balenciaga巴黎世家',
         'Bally巴利','Bentley宾利','Benz奔驰','BMW宝马','CK卡文克莱','Coach蔻驰','Ferrari法拉利',
         'GUCCI古驰','LV路易威登','Piaget伯爵','Porsche保时捷','Rollsroyce劳斯莱斯','Titoni梅花',
         'Volvo沃尔沃','YSL圣罗兰']


def get_logo_index(name):
    return logos.index(name)


def get_name(name):
    if '_' in name:
        return name[:name.index('_')]
    else:
        return name


def load_data():

    data = np.empty((103, 1, 50, 50), dtype="float32")
    label = np.empty((103,), dtype="uint8")
    imgs = os.listdir("./collect_bi_32")
    for i in range(104):
        if i > 0:

            arr = get_data_new("./collect_bi_32/" + imgs[i])
            name = imgs[i][:imgs[i].index(".")]

            name = get_name(name)

            index = get_logo_index(name)
            data[i-1, :, :, :] = arr
            label[i-1] = index

    print 'get data success'
    return data, label

def load_n():
    data = []
    label = []
    imgs = os.listdir("./collect_bi_32")
    for i in range(len(imgs)):
        if i > 0:
            arr1 = np.asarray(Image.open('./collect_bi_32/' + imgs[i]))
            arr = [1 for x in range(50) for y in range(50)]
            for k in range(len(arr1)):
                for j in range(len(arr1[0])):
                    if arr1[k][j] == 0:
                        arr[k*50 + j] = -1
                    else:
                        arr[k*50 + j] = 1
            name = imgs[i][:imgs[i].index(".")]
            # print arr
            name = get_name(name)
            # print name
            index = get_logo_index(name)
            data.append(arr)
            # label[i-1] = index
            label.append(index)

    print 'get data success'
    print data[1][1]
    return data, label

if __name__ == '__main__':

    arr = get_data_new("./collect_bi_32/Acura讴歌_0.jpg")
    # print arr
    for i in arr:
        print i
