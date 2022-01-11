# -*- coding: utf-8 -*-
# @Time    : 2022/1/11 11:46
# @Author  : Kenny Zhou
# @FileName: contour.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import numpy as np
import math
class Contour:
	"""
		生成等高图
	"""
	def __init__(self,object_map:np.ndarray):
		self.object_map = object_map
		self._goal = (np.where(self.object_map == 1)[0][0], np.where(self.object_map == 1)[1][0])
		self.map = np.zeros_like(self.object_map,dtype=np.uint8)
		# 进位
		self.radius = math.ceil(np.sqrt(self.map.shape[0]**2 + self.map.shape[1]**2))
		self.create_contour()

	def create_contour(self):
		it = np.nditer(self.map, flags=['multi_index'],op_flags=['readwrite'])
		while not it.finished:
			# print(it[0], it.multi_index)
			it[0] = self.overflow(np.round(self.eucli_dist(self._goal,it.multi_index)/ self.radius * 255))
			it.iternext()

	# 计算两点之间的距离
	def eucli_dist(self,A, B):
		# return np.sqrt(sum(np.power((A - B), 2)))
		return math.sqrt(sum([(a - b)**2 for (a,b) in zip(A,B)]))

	# 计算两点之间的距离
	def overflow(self,A):
		# return np.sqrt(sum(np.power((A - B), 2)))
		if A>255:
			return 255
		return A
