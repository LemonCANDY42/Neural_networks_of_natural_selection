# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 16:53
# @Author  : Kenny Zhou
# @FileName: nx_examples.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import matplotlib.pyplot as plt
import networkx as nx

import random
G = nx.gnp_random_graph(10,0.3)
for u,v,d in G.edges(data=True):
    d['weight'] = random.random()

edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())

pos = nx.spring_layout(G)
print(G, pos,edges,weights)
nx.draw(G, pos, node_color='b', edgelist=edges, edge_color=weights, width=10.0, edge_cmap=plt.cm.Blues)
# plt.savefig('edges.png')
plt.show()
