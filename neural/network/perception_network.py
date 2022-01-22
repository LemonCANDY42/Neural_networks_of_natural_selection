# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 13:03
# @Author  : Kenny Zhou
# @FileName: perception_network.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import networkx as nx
from neural.neurons.neuron import Neuron
from neural.network.network_base import NetworkBase

class PerceptionMoudule(NetworkBase):
	def __init__(self,index=1):
		super(PerceptionMoudule, self).__init__()
		self.start_index = index
		self.indexs = list(range(index,index+9))
		self.create_graph()
		self.description = "感知网络"
		self._build()

	def create_graph(self):
		for _index,i in enumerate(self.indexs):
			n = Neuron(id=i)
			self.G.add_node(n)
			# self.pos[_index] = (_index,0)
		nodes = list(self.G.nodes)
		# 前向
		self.add_channel(nodes[0], nodes[3])
		self.add_channel(nodes[1], nodes[4])
		self.add_channel(nodes[2], nodes[5])
		self.add_channel(nodes[3], nodes[6])
		self.add_channel(nodes[3], nodes[7])
		self.add_channel(nodes[4], nodes[6])
		self.add_channel(nodes[5], nodes[7])
		self.add_channel(nodes[6], nodes[8])
		self.add_channel(nodes[7], nodes[8])

		self.add_channel(nodes[4], nodes[7])
		self.add_channel(nodes[5], nodes[6])
		self.add_channel(nodes[3], nodes[5])
		self.add_channel(nodes[3], nodes[4])
		self.add_channel(nodes[4], nodes[5])

		# 反馈
		self.add_channel(nodes[8], nodes[0])
		self.add_channel(nodes[8], nodes[1])
		self.add_channel(nodes[8], nodes[2])


if __name__ == "__main__":
	import matplotlib.pyplot as plt
	M = PerceptionMoudule()

	# 重新绘制label
	G = nx.convert_node_labels_to_integers(M.G, first_label=M.start_index, ordering='default', label_attribute=None)
	pos = nx.random_layout(G)

	nx.draw(G, with_labels=True, font_weight='bold')
	# plt.savefig('edges.png')
	plt.show()