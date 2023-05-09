# -*- coding: utf-8 -*-
# @Time    : 2019/12/16
# @Author  : yz
# @Version : 1.0

import networkx as nx
import numpy as np
from collections import defaultdict
# from intersect_mp.tools import IntersectTools
from intersect.tools import IntersectTools

class COPRA_Load_Data():
    def read_graph_from_file(self, file_name,seed_node):
        print('read_graph:'+file_name)
        graph = nx.read_edgelist(file_name)
        # graph = self.assign_labels(label_assign_scheme,graph)
        if seed_node == 'off':
        # 初始化使所有节点的标签为其自身并对其加密
            for node, data in graph.nodes(True):
                dict = defaultdict(float)
                dict[IntersectTools.hash(node)] = 1
                data['label'] = dict
        return graph
    
    def read_attr_from_file(self, file_name):
        data = np.loadtxt(file_name, str, delimiter = ' ')
        A={}
        for attr in data:
            A.update({attr[0]:attr[1:len(attr)]})
        return A

    # def assign_labels(self,scheme,G):
    #     graph = G
    #     # if scheme[0] == 'high degree':
    #     #取出对应比例的的点作为种子节点
    #     num = len(graph.nodes())
    #     seed_num = int(num * scheme)
    #     print(seed_num)
    #     degree = list(graph.degree())
    #     degree.sort(key = lambda degree:degree[1],reverse = True)
    #     seed_list = degree[0:seed_num]
    #     seed = [x[0] for x in seed_list]
    #     # print(seed)
    #     for node, data in graph.nodes(True):
    #     #赋予种子节点标签
    #         if node in seed:
    #             dict = defaultdict(float)
    #             dict[IntersectTools.hash(node)] = 1
    #             data['label'] = dict
    #     #根据规则赋予其他节点标签
    #         if node not in seed:
    #             neighbor_index = graph.neighbors(node)
    #             seed_index = set(seed) & set(neighbor_index)
    #             if len(seed_index):
    #                 seed_choice = random.choice(list(seed_index))
    #             else:
    #                 seed_choice = random.choice(seed)
    #             dict = defaultdict(float)
    #             dict[IntersectTools.hash(seed_choice)] = 1
    #             data['label'] = dict
    #         # print(graph.nodes(node))
    #     return graph