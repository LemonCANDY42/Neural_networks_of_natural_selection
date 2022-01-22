# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 11:26
# @Author  : Kenny Zhou
# @FileName: Memory_MiniModule.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import networkx as nx
from neural.neurons.neuron import Neuron
from network_base import NetworkBase

class MemoryMini(NetworkBase):
	def __init__(self,index=1):
		super(MemoryMini, self).__init__()
		self.start_index = index
		self.indexs = range(index,index+4)
		self.create_graph()
		self.init_network()

	def create_graph(self):
		for _index,i in enumerate(self.indexs):
			n = Neuron(id=i)
			self.G.add_node(n)
			# self.pos[_index] = (_index,0)
		nodes = list(self.G.nodes)
		# 前向
		self.add_channel(nodes[0], nodes[1])
		self.add_channel(nodes[1], nodes[2])
		self.add_channel(nodes[2], nodes[3])

		# 反馈
		self.add_channel(nodes[2], nodes[1])
		self.add_channel(nodes[3], nodes[1])

		# 初级传递
		self.add_channel(nodes[0], nodes[3])

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	M = MemoryMini()

	# 重新绘制label
	G = nx.convert_node_labels_to_integers(M.G, first_label=M.start_index, ordering='default', label_attribute=None)
	pos = nx.random_layout(G)

	nx.draw(G, with_labels=True, font_weight='bold')
	# plt.savefig('edges.png')
	plt.show()

