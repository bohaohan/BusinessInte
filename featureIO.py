
__author__ = 'bohaohan'
import cv2
import numpy as np

def pickle_keypoints(keypoints, descriptors, name, path):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave,
        point.class_id, descriptors[i], name, path)
        i += 1
        temp_array.append(temp)
    return temp_array

def unpickle_keypoints(array):
    keypoints = []
    descriptors = []
    names = []
    path = []
    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
        temp_descriptor = point[6]
        temp_name = point[7]
        temp_path = point[8]
        keypoints.append(temp_feature)
        descriptors.append(temp_descriptor)
        names.append(temp_name)
        path.append(temp_path)
    return keypoints, np.array(descriptors), names, path