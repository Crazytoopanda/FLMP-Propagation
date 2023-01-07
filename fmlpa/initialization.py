# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:11:45 2020

@author: asus
"""

from collections import defaultdict
# from intersect_mp.tools import IntersectTools
from intersect.tools import IntersectTools
import random

class initialization():    
    def assign_labels(scheme,graph):
        if scheme == 'high degree':
            #取出对应比例的的点作为种子节点
            num = len(graph.nodes())
            seed_num = num * scheme[1]
            degree = graph.degree()
            degree.sort(key = lambda degree:degree[1])
            seed_list = degree[0:seed_num]
            seed = [x[1] for x in seed_list]
            for node, data in graph.nodes(True):
            #赋予种子节点标签
                if node in seed:
                    dict = defaultdict(float)
                    dict[IntersectTools.hash(node)] = 1
                    data['label'] = dict
            #根据规则赋予其他节点标签
                if node not in seed:
                    neighbor_index = graph.neighbors(node)
                    seed_index = set(seed) & set(neighbor_index)
                    if seed_index == None:
                        seed_choice = random.choice(seed)
                    else:
                        seed_choice = random.choice(list(seed_index))
                    dict = defaultdict(float)
                    dict[IntersectTools.hash(seed_choice)] = 1
                    data['label'] = dict
                print(graph.nodes(node))
        return graph
        
        
        
        
        
        
        
        
        
        
        
        