#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/28
# @Author  : Kun Guo
# @Version : 1.0

import networkx as nx
import matplotlib.pyplot as plt
import csv

#读入边集
G = nx.read_edgelist(r'parking.txt')
partition=dict()
#读入社区划分结果
with open('parking_re3.txt', "r")as f:
    f_csv = csv.reader(f)
    i = 1
    for row in f_csv:
        idx = row[0].strip().split(' ')
        for id in idx:
            partition[id] = i
        i=i+1

#选择社区编号
        
# ch=[52,145,150,102]
ch =[1,2,3,4]
ntd = []
for node in partition.keys():
    if partition[node] not in ch:
        ntd.append(node)
for node in ntd:
    partition.pop(node)
for node in partition.keys():
    if partition[node] == ch[0]:
        partition[node] = 0
    elif partition[node] == ch[1]:
        partition[node] = 1
    elif partition[node] == ch[2]:
        partition[node] = 3
    else:
        partition[node] = 2
        
H = G.copy()
H.remove_nodes_from(v for v in G if v not in partition.keys())
G = H

#seed可以自由选择
pos = nx.spring_layout(G, iterations=10, seed = 10001)  # compute graph layout
# plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
plt.axis('off')

nx.draw_networkx_nodes(G, pos, nodelist=partition.keys(), node_size=50, cmap=plt.cm.RdYlBu, alpha = 0.8,
                       node_color=list(partition.values()))

plt.show()
plt.savefig('figure 111.pdf', format='pdf',bbox_inches='tight')