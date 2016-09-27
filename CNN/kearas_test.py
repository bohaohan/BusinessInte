from __future__ import absolute_import
from __future__ import print_function
# -*- coding: UTF-8 -*-
__author__ = 'bohaohan'

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from SIFT.data import *
from SIFT.pre_pro import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


data, label = load_data()
# print (data.shape(0), 'samples')
# label 4 classes
label = np_utils.to_categorical(label, 4)
# print (data)
###############
# start CNN model
###############

# generate model
model = Sequential()

# 1st 4 core size 5*5
# model.add(input())
model.add(Convolution2D(4, 5, 5, border_mode='valid', input_shape=(1, 100, 100)))
model.add(Activation('tanh'))
# model.add(Dropout(0.5))

model.add(Convolution2D(8, 3, 3, border_mode='valid'))
model.add(Activation('tanh'))
model.add(MaxPooling2D(poolsize=(2, 2)))


model.add(Convolution2D(16, 3, 3, border_mode='valid'))
model.add(Activation('tanh'))
model.add(MaxPooling2D(poolsize=(2, 2)))


model.add(Flatten())
model.add(Dense(16*4*4, 128, init='normal'))
model.add(Activation('tanh'))


model.add(Dense(128, 4, init='normal'))
model.add(Activation('softmax'))

#############
# start training
sgd = SGD(l2=0.0, lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, class_mode="categorical")


model.fit(data, label, batch_size=100, nb_epoch=10, shuffle=True, verbose=1, show_accuracy=True, validation_split=0.2)
test_data = get_data("./test_img/1.jpg")
print (model.predict_classes(test_data), 'result !!!!!!!!!!!!')