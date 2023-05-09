"""
COPRA联邦化读图类

@author: Lfa
update: 2022/9/26
"""

import networkx as nx
import numpy as np
from collections import defaultdict
from intersect.tools import IntersectTools

class COPRA_Read_Data():
    def read_graph_from_file(self, file_name, seed_node):
        print('read_graph:' + file_name)
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
        data = np.loadtxt(file_name, str, delimiter=' ')
        A = {}
        for attr in data:
            A.update({attr[0]: attr[1:len(attr)]})
        return A