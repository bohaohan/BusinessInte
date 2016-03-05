# -*- coding: UTF-8 -*-
__author__ = 'bohaohan'
from fann2 import libfann
from pre_pro import *
connection_rate = 0.1
learning_rate = 0.1
num_input = 10000
num_hidden = 4
num_output = 102

desired_error = 0.0023
max_iterations = 100000
iterations_between_reports = 10

ann = libfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input, num_hidden, num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
# ann.set_activation_function_output(libfann.SIGMOID_STEPWISE)

ann.train_on_file("logo1.data", max_iterations, iterations_between_reports, desired_error)

ann.save("logo2.net")

# neural = libfann.neural_net()
# libfann.neural_net.create_from_file(neural, 'logo_do.net')
# arr = get_data('./test_img/Chevrolet雪佛兰.jpg')
# result = libfann.neural_net.run(neural, arr)
# print result, 'result'
