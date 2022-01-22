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
def sigmoid(X):
	return 1 / (1 + np.exp(-X))


# softmax function
@jit(nopython=True)
def softmax(a):
	"""Compute the softmax in a numerically stable way."""
	c = np.max(a)
	exp_a = np.exp(a - c)
	sum_exp_a = np.sum(exp_a)
	y = exp_a / sum_exp_a
	return y


# ReLu function
@jit(nopython=True)
def relu(X):
	return np.maximum(0, X)

@jit(nopython=True)
def update_weight(W,tensor):
	return W#(np.mean(tensor) - np.std(tensor) + W) / 2

if __name__ == "__main__":
	mmatrix = np.array([[-2,1, 2, 3], [-2,4, 5, 6]])
	output = relu(mmatrix)
	print(output)
