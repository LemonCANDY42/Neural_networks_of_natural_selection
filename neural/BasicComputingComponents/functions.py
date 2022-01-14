# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 14:27
# @Author  : Kenny Zhou
# @FileName: functions.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import numpy as np
from numba import jit
from numba import cuda


# sigmoid function
@jit(nopython=True)
def sigmoid(X,weights=0):
	return 1 / (1 + np.exp(-X))


# softmax function
@jit(nopython=True)
def softmax(X,weights=0):
	expo = np.exp(X)
	expo_sum = np.sum(np.exp(X))
	return expo / expo_sum


# ReLu function
@jit(nopython=True)
def relu(X,weights=0):
	return np.maximum(weights, X)


if __name__ == "__main__":
	mmatrix = np.array([[-2,1, 2, 3], [-2,4, 5, 6]])
	output = relu(mmatrix)
	print(output)
