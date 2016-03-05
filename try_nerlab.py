# -*- coding: utf-8 -*-
import cPickle

__author__ = 'bohaohan'

"""
Example of use Hopfield Recurrent network
=========================================

Task: Recognition of letters

"""

import numpy as np
import neurolab as nl
from data import *
# N E R O
data, label = load_n()
target = np.asfarray(data)
target[target == 0] = -1
print len(target)
def train():
    # target =  [[1,0,0,0,1,
    #            1,1,0,0,1,
    #            1,0,1,0,1,
    #            1,0,0,1,1,
    #            1,0,0,0,1],
    #           [1,1,1,1,1,
    #            1,0,0,0,0,
    #            1,1,1,1,1,
    #            1,0,0,0,0,
    #            1,1,1,1,1],
    #           [1,1,1,1,0,
    #            1,0,0,0,1,
    #            1,1,1,1,0,
    #            1,0,0,1,0,
    #            1,0,0,0,1],
    #           [0,1,1,1,0,
    #            1,0,0,0,1,
    #            1,0,0,0,1,
    #            1,0,0,0,1,
    #            0,1,1,1,0]]

    chars = ['N', 'E', 'R', 'O']
    print 'create and train!'
    # Create and train network
    net = nl.net.newhop(target)
    print 'success!'
    cPickle.dump(net, open("./net1.pkl", "wb"))
    print 'save success!'
# output = net.sim(target)
# print("Test on train samples:")
# for i in range(len(target)):
#     print(chars[i], (output[i] == target[i]).all())
def predict(path, net):
    def same(a, b):
        same = 0
        for i in range(len(a)):
            if a[i] == b[i]:
                same += 1
            else:
                continue
        return same
    # print("\nTest on defaced Audi:")
    # # test =np.asfarray([0,0,0,0,0,
    # #                    1,1,0,0,1,
    # #                    1,1,0,0,1,
    # #                    1,0,1,1,1,
    # #                    0,0,0,1,1])
    print 'test'
    test_data = get_data_test(path)
    name = path[path.rfind("/") + 1:path.rfind(".")]
    print name
    # print arr
    name = get_name(name)
    index = get_logo_index(name)
    print index
    # test = np.asfarray(test_data)
    # test[test == 0] = -1
    test = np.asfarray([test_data])
    out = net.sim(test)
    result = []
    for i in range(104):
        re = same(out[0], target[i])
        result.append({'index': label[i],
                       'same': re})
    result.sort(reverse=True, key=lambda x: x['same'])
    if result[0]['index'] == index:
        print 'true'
        return 1
    else:
        print 'false'
        return 0
    # print label
# print ((out[0] == target[0]).all(), 'Sim. steps',len(net.layers[0].outs))
if __name__ == '__main__':
    net = cPickle.load(open("PKL/net2.pkl", "rb"))
    imgs = os.listdir("./collect_bi_32")
    images = []
    for img in imgs:
        if 'DS_Store' not in img:
            images.append("./collect_bi_32/" + img)
    import random
    random.shuffle(images)
    print images
    result = 0
    for i in range(50):
        result += predict(images[i], net)
    print result, 'correct'
    print float(result)/50, 'accurency'