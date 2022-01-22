# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 12:01
# @Author  : Kenny Zhou
# @FileName: network_base.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import networkx as nx

class NetworkBase:
	"""
		网络的基本模块
	"""

	def __init__(self):
		self.G = nx.DiGraph()
		self.pos = {}
		self.description = ""
		self.indexs = []
		self.last_index = 0

	def init_network(self):
		for n in self.G.nodes:
			n.init_weight()

	def add_channel(self,on,to):
		self.G.add_edge(on, to)
		nodes = list(self.G.nodes)
		on.output_append(to)
		to.receptive_append(on)

	def create_graph(self):
		#网络创建
		pass

	def _build(self):
		self.last_index=self.indexs[-1]
		self.neurons = list(self.G.nodes)