#coding:utf-8
__author__ = 'bohaohan'
import cv2
import matplotlib.pyplot as plt

from skimage import data
from skimage.filters import threshold_otsu, threshold_adaptive
import numpy as np

# image = data.page()
image = cv2.imread("./img2/AstonMartin阿斯顿马丁_4.jpg", 0)
global_thresh = threshold_otsu(image)
binary_global = image > global_thresh

block_size = 40
binary_adaptive = threshold_adaptive(image, block_size, offset=10)

fig, axes = plt.subplots(nrows=3, figsize=(7, 8))
ax0, ax1, ax2 = axes
plt.gray()

ax0.imshow(image)
ax0.set_title('Image')

ax1.imshow(binary_global)
ax1.set_title('Global thresholding')

ax2.imshow(binary_adaptive)
ax2.set_title('Adaptive thresholding')

# print binary_adaptive
arrary = np.asarray(binary_adaptive, dtype="int")
for i in range(len(arrary)):
    for j in range(len(arrary[0])):
        if arrary[i][j] == 1:
            arrary[i][j] = 255
        else:
            arrary[i][j] = 0
print arrary
cv2.imwrite('test.jpg', arrary)
for ax in axes:
    ax.axis('off')

# plt.show()