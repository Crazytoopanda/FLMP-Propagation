# -*- encoding = "utf-8" -*_
"""
COPRA算法，依赖Leaderrank函数

Created on Sat Sept 10 23:00:00 2022
@author lfa
"""

import time
from collections import defaultdict
import EQ
import networkx as nx
from LeaderRank import leader_rank
import onmi

class COPRA :

    def read_graph(self, edgelist_file:str) -> nx.Graph:
        graph = nx.read_edgelist(edgelist_file)
        for node, data in graph.nodes(True):
            dict = defaultdict(float)
            dict[node] = 1.0
            data["label"] = dict.copy()
        return graph

    def normalize(self, graph:nx.Graph) -> nx.Graph:
        for node, data in graph.nodes(data=True):
            tempdict = defaultdict(float )
            degree = graph.degree[node]
            for neighbor in graph.neighbors(node):
                for neig_node, neig_data in graph.nodes[neighbor]["label"].items():
                    tempdict[neig_node] += neig_data / degree
            data["label"] = tempdict.copy()
        return graph

    def propagation(self, graph:nx.Graph, priority_vertice:list, v:int) \
            -> (nx.Graph, list):
        """
        标签传播主算法

        :param graph: 图存在标签
        :param priority_vertice: 图传播顺序
        :param v: 阈值系数
        :return: 列表，其中每个作为社区
        """
        labeldict = dict()

        # 先进行每个节点的标签归一化
        graph = self.normalize(graph)
        # labeldict 是字典，key为每个节点，value是标签情况（其中也是字典）
        for node, data in graph.nodes(data=True) :
            labeldict[node] = data["label"]

        for node in priority_vertice:

            sum_node_label = graph.nodes[node]["label"].copy()

            max_label_value = max(sum_node_label.values())
            #
            if max_label_value < 1.0 / v:
                labeldict[node].clear()
                for label in sum_node_label.keys():
                    if max_label_value == sum_node_label[label]:
                        labeldict[node] = {label: 1.0}
                        break
            else :
                sumAverage = 0.0
                for key, value in labeldict[node].copy().items():
                    if abs(max_label_value - value) > 0.00005:
                        sumAverage += value
                        labeldict[node].pop(key)
                for key, value in labeldict[node].items():
                    labeldict[node][key] = value/(1-sumAverage)

        # 重新为图"label"赋值
        for key, value in labeldict.items():
            graph.nodes[key]["label"] = value.copy()
        return graph, labeldict

    def get_communities(self, labeldict:dict):
        community = defaultdict(lambda: set())
        for keyi, valuei in labeldict.items():
            for keyj, valuej in valuei.items():
                # community[keyj].add(int(keyi))
                community[keyj].add(keyi)
        return community

    def sort_graph_neighbor(self, graph):
        temp_list = list(nx.degree(graph))
        temp_list = sorted(temp_list, key=lambda x:x[1], reverse=False)
        return [i[0] for i in temp_list]

    def i_label_propagation(self, graph: nx.Graph, v, write_path, real_path) \
            -> nx.Graph:

        """
        : 添加了leaderrank函数的标签传播算法

        :param graph: nx.Graph类型，社区情况
        :param v: int类型，表示社区数量
        :param time_iterate: int类型，迭代次数默认为5次
        :return:
        """
        # 存在leaderrank传播
        # inf, time_iterate = list(leader_rank(graph).items()), 0
        # priority_vertice = sorted(inf, key=lambda x: x[1], reverse=True)

        # 无leaderrank，随机传播
        priority_vertice, time_iterate = list(graph.nodes), 0
        # random.shuffle(priority_vertice)
        priority_vertice = [i[0] for i in sorted(leader_rank(graph).items(), \
                                                 key=lambda x:x[1], reverse=True)]

        # 以节点的度最高排序
        # priority_vertice = self.sort_graph_neighbor(graph)
        min_communities = None
        communities = None
        while True:
            time_iterate += 1
            # for nodei in [i[0] for i in priority_vertice]:
            graph, labellist = self.propagation(graph, priority_vertice, v)

            # graph, retry = self.post_processing(graph)

            communities = self.get_communities(labellist)
            cur_communities = communities.copy()
            for com in cur_communities.keys():
                cur_communities[com] = len(cur_communities[com])
            print("此时社区数量:", str(len(cur_communities)))
            if time_iterate > 30 or (not self.communities_changed \
                        (cur_communities, min_communities)):
                break
            min_communities = cur_communities.copy()
        self.write_communities(communities, write_path)
        print(EQ.cal_EQ(communities.values(), graph, real_path[: -4] + "EQ.txt" ))
        onmi.cale_onmi(real_path, write_path, real_path[: -4] + "ONMI.txt")
        return communities

    def communities_changed(self, communities, min_communities):
        if min_communities is None:
            return True
        else :
            for community, value in communities.items():
                if community not in min_communities:
                    return True
                else :
                    if not not (min_communities[community] - value):
                        return True
            return False

    def write_communities(self, communities, location):
        output_file = open(location, 'w')
        for key, value in communities.items():
            value
            valuetemp = sorted(value, reverse=False)
            for member in valuetemp:
                output_file.write(str(member) + " ")
            output_file.write("\n")
        output_file.close()
        return


if __name__ == "__main__":
    # graph = {"A": set(["B", "D", "E", "G"]), \
    #          "B": set(["A", "C", "D"]), \
    #          "C": set(["B", "D"]), \
    #          "D": set(["A", "B", "C"]), \
    #          "E": set(["A", "G", "F"]), \
    #          "F": set(["E", "G"]), \
    #          "G": set(["A", "E", "F"])}
    # G = nx.Graph(graph)
    #
    # for node, data in G.nodes(True):
    #     dictt = defaultdict(float)
    #     dictt[node] = 1.0
    #     data["label"] = dictt.copy()

    file = ["100","200","300","400","500"]
    copra = COPRA()

    # feature_name = "../data/artificial/on/feat/network100_bd_feat.txt"
    for i in file:

        file_name = "../data/artificial/on/network" + i + ".txt"
        write_path = "../data/network.txt"
        real_path = "../data/artificial/on/community" + i + ".txt"
        G = copra.read_graph(file_name)
        start_time = time.time()
        Glabel = copra.i_label_propagation(G, 2, write_path, real_path)
        end_time = time.time()
        print("Time spend: %.5f" % (end_time - start_time))