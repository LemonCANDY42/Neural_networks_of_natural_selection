# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 12:44
# @Author  : Kenny Zhou
# @FileName: neuron.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import numpy as np

from neural.BasicComputingComponents.functions import *
from enum import Enum, auto
from numba import jit
from numba import int32, float32  # import the types
from numba.experimental import jitclass
import random
from analysis.time_tools import *

np.random.seed(42)

class NeuronType(Enum):
	RELU = auto()
	SOFTMAX = auto()
	SIGMOID = auto()


class Neuron():
	"""
		神经元的实现
		zone结构在每次计算遍历到的时候执行
	"""

	def __init__(self, id, coordinates=None, type=NeuronType.RELU,create_weight="N-d", load_weights=False,full_connections=10):
		if load_weights:
			self.id = load_weights['id']
			self.coordinates = load_weights['coordinates']
			self.receptive_list = load_weights['receptive_id_list']
			self.output_id_list = load_weights['output_id_list']
			self.weights = load_weights['weights']
			self.type = load_weights['type']
			self.create_weight = load_weights['create_weight']
			self.weights_shape = load_weights['weights_shape']
			self.weight = load_weights['weight']
			self.out_shape = load_weights['out_shape']
			self.in_shape = load_weights['in_shape']
			self.out_weight = load_weights['out_weight']
			self.full_connections = load_weights['full_connections']
		else:
			self.id = id
			self.coordinates = coordinates
			# 树突接受的突触输入id
			self.receptive_list = []
			# 突触对接的树突输出id
			self.output_id_list = []
			self.output_list = []
			self.weights = {}
			self.weight = None
			self.type = type
			self.create_weight = create_weight
			self.out_shape = None
			self.in_shape = None
			self.out_weight = None
			self.full_connections = full_connections

		# 在下一次计算前接到的输入(按顺序 element: key: id ,value: tensor)
		self.nerve_signals = []
		self.trigger = None
		self.locker = False


		if type is NeuronType.RELU:
			self.activation_function = relu
		elif type is NeuronType.SIGMOID:
			self.activation_function = sigmoid
		elif type is NeuronType.SOFTMAX:
			self.activation_function = softmax
		else:
			self.activation_function = relu

	def create_tensor(self,*shape):
		if self.create_weight == "N-d":
			return np.random.randn(*shape)
		elif self.create_weight == "one":
			return np.ones(shape)
		else:
			return np.random.random(shape)

	def broadcast_weight(self,input_shape=None,output_shape=None):
		"""广播更新权值"""
		pass

	@property
	def is_input(self):
		if len(self.receptive_list) == 1 and self.receptive_list[0] == 0:
			return True
		else:
			return False

	@property
	def is_output(self):
		if len(self.output_id_list) == 1 and self.output_id_list[0] == -1:
			return True
		else:
			return False

	def flatten_shape(self,neuron):
		# flatten
		size = None
		if self.in_shape:
			for i in self.in_shape[:-1]:
				if size is None:
					size = i
				else:
					size = size * i
			return size*len(neuron.output_id_list)
		else:
			return None

	def init_weight(self):

		if not self.is_output:
			in_shape = len(self.output_id_list)
		else:
			in_shape = self.out_shape[-1]
			# out_shape = self.out_shape

		if self.is_output:
			if len(self.out_shape) > 1:
				self.out_weight = self.create_tensor(*self.out_shape[:-1] ,1)
			else:
				self.out_weight = self.create_tensor(1)
			self.weight = self.create_tensor(self.full_connections,in_shape)
		else:
			self.weight = self.create_tensor(len(self.output_id_list), in_shape)

		for id in self.receptive_list:
			if isinstance(id, int):
				if id not in self.weights:
					self.weights[id] = self.generate_weights(id)
			else:
				if id.id not in self.weights:
					self.weights[id.id] = self.generate_weights(id)

	def generate_weights(self,neuron):
		"""初始化生成权重"""
		in_shape = None
		if isinstance(neuron, int):
			if neuron == 0:
				in_shape=self.in_shape[-1]
		else:
			if not self.is_output:
				in_shape = len(neuron.output_id_list)
			else:
				in_shape = self.flatten_shape(neuron) #neuron.out_shape[-1]
				return self.create_tensor(in_shape, self.full_connections)

		return self.create_tensor(in_shape, len(self.output_id_list))

	def receptive_append(self,id):
		"""添加输入神经元"""
		# if isinstance(id, int):
		if id not in self.receptive_list:
			self.receptive_list.append(id)

	def receptive_remove(self,id):
		"""移除输入神经元"""
		if id in self.receptive_list:
			self.receptive_list.remove(id)
		if id not in self.weights:
			del self.weights[id]

	def output_append(self,neuron):
		"""添加输出神经元"""
		if isinstance(neuron, int):
			if neuron == -1:
				self.output_id_list.append(neuron)
				self.output_list.append(None)
			else:
				raise "output append: 错误的参数"
		elif isinstance(neuron, Neuron):
			# if neuron.id<self.id:
			# 	raise "output append: 不能反向激活神经元！"
			if neuron.id not in self.output_id_list:
				self.output_id_list.append(neuron.id)
			if neuron not in self.output_list:
				self.output_list.append(neuron)
		else:
			raise "output append: 错误的神经元设置"

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

	def receptive_zone(self, neuron, tensor):
		"""
		 树突接受信号
		:param id:
		:type id:
		:param tensor:
		:type tensor:
		:return:
		:rtype:
		"""
		while self.locker:pass

		if neuron in self.receptive_list:
			self.dendrites(neuron.id, tensor)
		else:
			raise "不允许的神经连接"

	def trigger_zone(self):
		"""
			神经元计算触发信号，在网络管理器中统一触发
		:return:
		:rtype:
		"""
		self.locker = True
		Tensor = None
		# freeze_nerve_signals = self.nerve_signals.copy()
		if self.nerve_signals:
			for id, _tensor in self.nerve_signals:
				# print(f'神经元：{self.id}:',_tensor.shape,self.weights[id].shape,self.weight.shape)
				if self.is_output:
					# print(self.out_weight.shape,_tensor.flatten().dot(self.weights[id]).shape,self.weight.shape)
					tensor = self.out_weight @ (_tensor.ravel()[np.newaxis,:]@self.weights[id]@self.weight)
				else:
					tensor = _tensor @ self.weights[id] @ self.weight #
				if Tensor is None:
					Tensor = tensor
				else:
					Tensor += tensor
			Tensor = self.activation_function(Tensor)
			# self.weight = (np.mean(Tensor) - np.std(Tensor) + self.weight)/2
			self.weight = update_weight(self.weight, Tensor)
			self.nerve_signals = []
			self.trigger = Tensor
			# print("神经元：", self.id, "输出：", Tensor)
			self.output_zone()
		self.locker = False

	def output_zone(self):
		"""
		突触输出
		:return:
		:rtype:
		"""
		if not self.is_output:
			if self.output_list:
				for neuron in self.output_list:
					neuron.receptive_zone(self,self.trigger)
		else:
			return

	def __hash__(self):
		return hash(self.id)

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
	input = np.random.random((224,224,3))

	n1 = Neuron(id=1, coordinates=(0, 0))
	n2 = Neuron(id=2, coordinates=(1, 0))
	n3 = Neuron(id=3, coordinates=(1, 0))
	n4 = Neuron(id=4, coordinates=(2, 0),type=NeuronType.SOFTMAX)#,type=NeuronType.SIGMOID

	Ns = [n1,n2,n3,n4]

	# warm up
	# n1.dendrites(0, tensor=input)
	# n1.trigger_zone()
	n4.out_shape = (4,)
	n4.in_shape = input.shape
	n4.output_append(-1)

	n1.in_shape = input.shape
	n1.receptive_append(0)


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

	for n in Ns:
		n.init_weight()

	# @time_keep
	def trigge_neuron(tensor):
		n1.dendrites(0, tensor=tensor)
		n1.trigger_zone()
		n2.trigger_zone()
		n3.trigger_zone()
		n4.trigger_zone()
		return n4.trigger


	temp = trigge_neuron(input)

	start = time.time()
	temp = input
	for i in range(10):
		temp = trigge_neuron(input)
	print("耗时:", time.time() - start)

	print(trigge_neuron(input))#,input.shape,trigge_neuron(input).shape
