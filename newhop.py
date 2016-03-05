# -*- coding: utf-8 -*-
"""
Example of use Hopfield Recurrent network
=========================================

Task: Recognition of letters

"""

import numpy as np
import neurolab as nl

# N E R O
target =  [[1,0,0,0,1,
           1,1,0,0,1,
           1,0,1,0,1,
           1,0,0,1,1,
           1,0,0,0,1],
          [1,1,1,1,1,
           1,0,0,0,0,
           1,1,1,1,1,
           1,0,0,0,0,
           1,1,1,1,1],
          [1,1,1,1,0,
           1,0,0,0,1,
           1,1,1,1,0,
           1,0,0,1,0,
           1,0,0,0,1],
          [0,1,1,1,0,
           1,0,0,0,1,
           1,0,0,0,1,
           1,0,0,0,1,
           0,1,1,1,0]]

chars = ['N', 'E', 'R', 'O']
target = np.asfarray(target)
target[target == 0] = -1

# Create and train network
net = nl.net.newhop(target)

output = net.sim(target)
print("Test on train samples:")
# for i in range(len(target)):
#     print(chars[i], (output[i] == target[i]).all())

print("\nTest on defaced N:")
test =np.asfarray([1,0,0,1,0,
                   1,1,0,1,0,
                   1,1,0,1,0,
                   1,0,1,1,0,
                   1,0,0,1,0])
test[test==0] = -1
out = net.sim([test])
# print out
def sum(a, b):
    same = 0
    for i in range(25):
        if a[i] == b[i]:
            same += 1
        else:
            continue
    return same
# print out[0] in target
print out[0] in target
# print target
# print out
# print target[2]
# print out[0] is target[2]
# print same(out[0], target[2])
# print out[0][1] == target[2][1]
for i in target:
    re = sum(out[0], i)
    print re
print ((out[0] == target[3]).all(), 'Sim. steps',len(net.layers[0].outs))