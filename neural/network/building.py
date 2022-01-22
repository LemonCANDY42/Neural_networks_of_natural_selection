# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 13:19
# @Author  : Kenny Zhou
# @FileName: building.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import networkx as nx
from neural.neurons.neuron import Neuron,NeuronType
from neural.network.network_base import NetworkBase
from neural.network.memory_mini_module import MemoryMini
from neural.network.perception_network import PerceptionMoudule
import numpy as np

class BuildingNetwork(NetworkBase):
	def __init__(self,index=1,description="",input_shape=None,output_shape=None):
		super(BuildingNetwork, self).__init__()
		self.start_index = index
		self.indexs = []
		self.description = description
		self.networks = []
		self.input_shape = input_shape
		self.output_shape = output_shape

		self.define_network()

		self.init_network()

	def define_network(self):
		self.def_input()

		M = MemoryMini(index=self.last_index+1)
		self.network_append(M)

		n0 = Neuron(id=self.last_index + 1)
		self.add_node(n0)

		M_nodes = list(M.G.nodes)
		self.add_channel(M_nodes[3], n0)

		P = PerceptionMoudule(index=self.last_index + 1)
		self.network_append(P)
		P_nodes = list(P.G.nodes)

		self.add_channel(n0, P_nodes[3])
		self.add_channel(n0, P_nodes[8])

		self.def_output()

		self.add_channel(self.nodes[0], M_nodes[0])
		self.add_channel(self.nodes[0], P_nodes[0])
		self.add_channel(self.nodes[0], P_nodes[1])
		self.add_channel(self.nodes[0], P_nodes[2])

		self.add_channel(P_nodes[-1],self.nodes[-1])

	@property
	def nodes(self) -> [Neuron]:
		return list(self.G.nodes)

	def def_input(self):
		# 定义输入
		input_n = Neuron(id=self.start_index)
		input_n.in_shape = self.input_shape
		input_n.receptive_append(0)

		self.add_node(input_n,description="input")

	def def_output(self):
		# 定义输出
		output_n = Neuron(id=self.last_index + 1,type=NeuronType.SOFTMAX)
		output_n.out_shape = self.output_shape
		output_n.in_shape = self.input_shape
		output_n.output_append(-1)

		self.add_node(output_n,description="output")

	def network_append(self,network:NetworkBase):
		self.G.add_nodes_from(network.G.nodes)
		self.G.add_edges_from(network.G.edges)
		self.networks.append(network)
		self._cal_lastIndex()

	def add_node(self,n,**kwards):
		self.G.add_node(n,**kwards)
		self._cal_lastIndex()

	def _cal_lastIndex(self):
		all_indexs = 0
		for n in self.networks:
			all_indexs+=len(n.G.nodes)
		self.last_index = len(self.G.nodes) + all_indexs

	def activation(self,tensor):
		self.nodes[0].dendrites(0, tensor=tensor)
		for n in self.nodes:
			n.trigger_zone()
		return self.nodes[-1].trigger

	def reward_punishment(self,factor):
		for n in self.nodes:
			n.punishment(factor)

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	import math
	import random
	M = BuildingNetwork(input_shape=(1,5),output_shape=(1,4))

	# 重新绘制label
	G = nx.convert_node_labels_to_integers(M.G, first_label=M.start_index, ordering='default', label_attribute=None)
	pos = nx.random_layout(G)

	nx.draw(G, with_labels=True, font_weight='bold')
	# plt.savefig('edges.png')
	plt.show()

	input = np.random.randint(2,size=(1, 5))
	input = np.array([[1,0,0,0,226]])

	output = None
	for i in range(10):
		output = M.activation(input)
		res = random.uniform(0.5, 2)
		M.reward_punishment(res)
	print(input,output,np.argmax(output, axis=1),M.nodes[-2].trigger)
