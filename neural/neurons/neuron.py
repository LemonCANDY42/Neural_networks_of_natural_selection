# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 12:44
# @Author  : Kenny Zhou
# @FileName: neuron.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

from neural.BasicComputingComponents.functions import *
from enum import Enum, auto
from numba import jit
from numba import int32, float32  # import the types
from numba.experimental import jitclass
import random


class NeuronType(Enum):
	RELU = auto()
	SOFTMAX = auto()
	SIGMOID = auto()


class Neuron():
	"""
		神经元的实现
		zone结构在每次计算遍历到的时候执行
	"""

	def __init__(self, id, coordinates, type=NeuronType.RELU,create_weight="zero", load_weights=False):
		if load_weights:
			self.id = load_weights['id']
			self.coordinates = load_weights['coordinates']
			self.receptive_id_list = load_weights['receptive_id_list']
			self.output_id_list = load_weights['output_id_list']
			self.weights = load_weights['weights']
			self.type = load_weights['type']
			self.create_weight = load_weights['create_weight']
		else:
			self.id = id
			self.coordinates = coordinates
			# 树突接受的突触输入id
			self.receptive_id_list = []
			# 突触对接的树突输出id
			self.output_id_list = []
			self.output_list = []
			self.weights = {}
			self.type = type
			self.create_weight = create_weight

		# 在下一次计算前接到的输入(按顺序 element: key: id ,value: tensor)
		self.nerve_signals = []
		self.trigger = None

		if type is NeuronType.RELU:
			self.simplify_function = relu
		elif type is NeuronType.SIGMOID:
			self.simplify_function = sigmoid
		elif type is NeuronType.SOFTMAX:
			self.simplify_function = softmax
		else:
			self.simplify_function = relu

	def generate_weight(self):
		"""初始化生成权重"""
		if self.create_weight=="random":
			return random.uniform(-1, 1)
		else:
			return 0

	def receptive_append(self,id):
		"""添加输入神经元"""
		if isinstance(id, int):
			if id not in self.receptive_id_list:
				self.receptive_id_list.append(id)
			if id not in self.weights:
				self.weights[id] = self.generate_weight()
		elif isinstance(id, Neuron):
			if id.id not in self.receptive_id_list:
				self.receptive_id_list.append(id.id)
			if id.id not in self.weights:
				self.weights[id.id] = self.generate_weight()
		else:
			raise "不适用的参数类型"

	def receptive_remove(self,id):
		"""移除输入神经元"""
		if id in self.receptive_id_list:
			self.receptive_id_list.remove(id)
		if id not in self.weights:
			del self.weights[id]

	def output_append(self,neuron):
		"""添加输出神经元"""
		if neuron.id not in self.output_id_list:
			self.output_id_list.append(neuron.id)
		if neuron not in self.output_list:
			self.output_list.append(neuron)

	def output_remove(self,neuron):
		"""移除输出神经元"""
		if isinstance(neuron, Neuron):
			if neuron.id in self.output_id_list:
				self.output_id_list.remove(neuron.id)
			if neuron in self.output_list:
				self.output_list.remove(neuron)
		elif isinstance(neuron, int):
			if id in self.output_id_list:
				self.output_id_list.remove(id)
			if neuron in self.output_list:
				self.output_list.remove(neuron)
		else:
			raise "输入的神经元类型错误"

	def dendrites(self, id, tensor):
		"""树突"""
		# print("神经元：",self.id,"输入：",id, tensor)
		self.nerve_signals.append((id, tensor))

	def receptive_zone(self, id, tensor):
		"""
		 树突接受信号
		:param id:
		:type id:
		:param tensor:
		:type tensor:
		:return:
		:rtype:
		"""
		if id in self.receptive_id_list:
			self.dendrites(id, tensor)
		else:
			raise "不允许的神经连接"

	def trigger_zone(self):
		"""
			神经元计算触发信号，在网络管理器中统一触发
		:return:
		:rtype:
		"""
		Tensor = 0
		freeze_nerve_signals = self.nerve_signals.copy()
		for id, _tensor in freeze_nerve_signals:
			Tensor = self.simplify_function(_tensor, self.weights[id])
			self.weights[id] = (np.mean(Tensor) - np.std(Tensor) + self.weights[id])/2
		self.nerve_signals = []
		self.trigger = Tensor
		# print("神经元：", self.id, "输出：", Tensor)
		self.output_zone()

	def output_zone(self):
		"""
		突触输出
		:return:
		:rtype:
		"""
		if self.output_list:
			for neuron in self.output_list:
				neuron.receptive_zone(self.id,self.trigger)

	def __eq__(self, other):
		"""
		判断是否为相同神经元
		"""
		if isinstance(other, Neuron):
			return self.id == other.id
		else:
			return False

if __name__ == "__main__":
	import time
	input = np.array([[0,1,2,3], [4,5,6,7]])

	n1 = Neuron(id=1, coordinates=(0, 0))
	n2 = Neuron(id=2, coordinates=(1, 0))
	n3 = Neuron(id=3, coordinates=(1, 0))
	n4 = Neuron(id=4, coordinates=(2, 0),type=NeuronType.SIGMOID)

	# warm up
	n1.receptive_append(0)
	n1.dendrites(0, tensor=input)
	n1.trigger_zone()

	n1.output_append(n2)
	n2.receptive_append(n1)

	n1.output_append(n3)
	n3.receptive_append(n1)

	n2.output_append(n3)
	n3.receptive_append(n2)

	n3.output_append(n4)
	n4.receptive_append(n3)

	n2.output_append(n4)
	n4.receptive_append(n2)

	def trigge_neuron(tensor):
		n1.dendrites(0, tensor=tensor)
		n1.trigger_zone()
		n2.trigger_zone()
		n3.trigger_zone()
		n4.trigger_zone()
		return n4.trigger

	start = time.time()
	temp = input
	for i in range(10000):
		temp = trigge_neuron(temp)
	print("耗时:", time.time() - start)

	print(trigge_neuron(input))
