#coding:utf-8

'''
    GPU run command:
        THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python cnn.py
    CPU run command:
        python cnn.py
'''
#导入各种用到的模块组件
from __future__ import absolute_import
from __future__ import print_function
import os
# from six.moves import range
import cPickle
from SIFT.pre_pro import *
model = cPickle.load(open("PKL/final_model1.pkl", "rb"))


def predict(path):
    name = path[path.rfind("/") + 1:path.rfind(".")]
    # print arr
    name = get_name(name)
    index = get_logo_index(name)
    print ('test', name)
    test_data = get_data_new(path)

    data = np.empty((1, 1, 50, 50), dtype="float32")
    data[0, :, :, :] = test_data
    data /= 255

    result = model.predict_proba(data, verbose=1)

    r_name = logos[int(model.predict_classes(data)[0])]
    print (result, r_name, 'result')

    if name == r_name:
        return 1
    else:
        return 0


def evala(num):

    imgs = os.listdir("./test_img3")
    images = []

    for img in imgs:
        if 'DS_Store' not in img:
            images.append("./test_img3/" + img)
    import random
    random.shuffle(images)

    result = 0
    for i in range(num):
        result += predict_new(images[i])

    print (result, 'correct')
    print (float(result)/num, 'accurency')


def predict_new(imagePath):

    print (imagePath)

    imagePath.encode('utf-8')
    imagename = imagePath[imagePath.rfind("/") + 1:]
    imagename = get_name(imagename)

    img = cv2.imread(imagePath, 0)
    binary_adaptive = threshold_adaptive(img, 40, offset=10)
    arrary = np.asarray(binary_adaptive, dtype="float32")

    for i in range(len(arrary)):
        for j in range(len(arrary[0])):
            if arrary[i][j] == 1:
                arrary[i][j] = 255
            else:
                arrary[i][j] = 0

    height = len(arrary)
    width = len(arrary[0])

    if height > width:
        ratio = 50/float(height)
    else:
        ratio = 50/float(width)

    # print ratio
    arrary = cv2.resize(arrary, None, fx=ratio, fy=ratio)
    height = len(arrary)
    width = len(arrary[0])
    a = np.empty((50, 50), dtype="float32")

    for i in range(50):
        for j in range(50):
            a[i][j] = 255

    for i in range(height):
        for j in range(width):
            a[i][j] = arrary[i][j]

    data = np.empty((1, 1, 50, 50), dtype="float32")
    data[0, :, :, :] = a
    data /= 255
    result = model.predict_proba(data, verbose=1)

    r_name = logos[int(model.predict_classes(data)[0])]
    print (result, r_name, 'result')
    if imagename == r_name:
        print ('true')
        return 1
    else:
        return 0


if __name__ == '__main__':
    evala(42)