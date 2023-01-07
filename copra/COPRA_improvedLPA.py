# -*- encoding = "utf-8" -*_
"""

Created on Sat Sept 10 23:00:00 2022

@author lfa

"""
import hashlib
import random
import time
from collections import defaultdict, Counter
import networkx as nx
import pandas as pd


class COPRA_improvedLPA:

    # 用于联机加密, ---未使用
    def hash(self, value):
        return hashlib.sha3_256(bytes(str(value), encoding='utf-8')) \
            .hexdigest()

    def read_graph(self, edgelist_file) -> nx.Graph:
        graph = nx.read_edgelist(edgelist_file)
        # for node, data in graph.nodes(True):
        #     dict = defaultdict(float)
        #     for nodej in graph.neighbors(node):
        #         dict[nodej] = 1.0 / len(graph[node])  # self.hash(nodej)
        #     data["label"] = dict
        return graph

    # def post_processing(self, graph:nx.Graph) -> nx.Graph :
    #     retry = 0
    #     for node, data in graph.nodes(data=True):
    #         dictV = defaultdict(float)
    #         for neighbor_node in graph.neighbors(node) :
    #             for key, value in graph.nodes[neighbor_node] \
    #                     ["label"].items() :
    #                 dictV[key] += value
    #         degree = len(graph[node])
    #         for key in dictV.keys() :
    #             dictV[key] /= degree
    #         if data["label"] != dictV :
    #             retry = 1
    #         data["label"] = dictV
    #     return graph, retry

    def communities_changed(self, cur_com_dict, min_com_dict):
        '''
        判断当前轮迭代生成的社区大小相对于之前迭代生成的最小社区大小是否有变化。若有变化，则需要更新最小社区大小。
        :param cur_com_dict: 当前轮迭代生成的{社区标签,社区大小}字典。
        :param min_com_dict: 之前迭代生成的{社区标签,社区大小最小值}字典。
        :return: 若有变化则True，否则返回False。
        '''
        if min_com_dict is None :
            return True
        if len(cur_com_dict) != len(min_com_dict) :
            return True
        changed = False
        for label in cur_com_dict.keys() :
            # print(label)
            if label not in min_com_dict.keys() :
                return True
            if cur_com_dict[label] < min_com_dict[label] :
                changed = True
            else:
                cur_com_dict[label] = min_com_dict[label]
        return changed

    # def post_processing(self, graph: nx.Graph) -> nx.Graph:
    #     retry = 0
    #     for node, data in graph.nodes(data=True) :
    #         if len(data) > 1 :
    #
    #     return graph, retry

    def cal_EQ(self, cover, G):
        vertex_community = defaultdict(lambda: set())
        for i, c in enumerate(cover):
            for v in c:
                vertex_community[v].add(i)
        m = 0.0
        for v, neighbors in G.edges():
            for n in neighbors:
                if v > n:
                    m += 1
        total = 0.0
        for c in cover:
            for i in c:
                o_i = len(vertex_community[i])
                k_i = len(G[i])
                for j in c:
                    o_j = len(vertex_community[j])
                    if j not in G:
                        print(j)
                    k_j = len(G[j])
                    if i > j:
                        continue
                    t = 0.0
                    if j in G[i]:
                        t += 1.0 / (o_i * o_j)
                    t -= k_i * k_j / (2 * m * o_i * o_j)
                    if i == j:
                        total += t
                    else:
                        total += 2 * t
        # print('EQ:',round(total / (2 * m), 4))
        return round(total / (2 * m), 4)

    def init_label(self, graph) :
        labellist = {i: {i: 1.0} for i in graph.nodes}
        return labellist

    def propagation(self, graph, labellist, visitshuffle, v) :
        for visit in visitshuffle :
            temp_label = {}
            total = len(graph[visit])
            # 根据邻居利用公式计算标签
            for i in graph.neighbors(visit):
                res = {key: value / total for key, value in labellist[i].items()}
                temp_label = Counter(res) + Counter(temp_label)
            temp_count = len(temp_label)
            temp_label2 = temp_label.copy()
            for key, value in list(temp_label.items()) :
                if value < 1 / v :
                    del temp_label[key]
                    temp_count -= 1
            # 如果一个节点中所有的标签都低于阈值就随机选择一个
            if temp_count == 0 :
                b = random.sample(temp_label2.keys(), 1)
                # b = max(temp_label2.keys())
                temp_label = {b[0]: 1}
            # 否则标签个数一定小于等于v个 进行归一化即可
            else :
                tsum = sum(temp_label.values())
                temp_label = {key: value / tsum for key, value in temp_label.items()}
            labellist[visit] = temp_label
            # print(labellist)
        return labellist

    def sort_graph_neighbor(self, graph:pd.DataFrame) :
        temp_list = list(nx.degree(graph))
        temp_list = sorted(temp_list, key=lambda x:x[1], reverse=False)
        return [i[0] for i in temp_list]

    def i_label_propagation(self, graph: nx.Graph, v, time_iterate=1000) -> nx.Graph :
        """

        :param graph: 图
        :param v: 阈值系数
        :return:
        """
        labellist = self.init_label(graph)
        timecount = 0
        min_com_dict = None

        while True :
            timecount += 1

            # inf = list(leader_rank(graph).items())
            # visitshuffle = sorted(inf, key=lambda x: x[1], reverse=True)
            # visitshuffle = [i[0] for i in visitshuffle]

            # visitshuffle = list(graph.nodes)
            # random.shuffle(visitshuffle)

            visitshuffle = self.sort_graph_neighbor(graph)

            labellist = self.propagation(graph, labellist, visitshuffle, v)

            # 将字典的value改为社区大小。
            for key, change in labellist.items():
                graph.nodes[key]["label"] = change
            cur_com_dict = self.get_communities(graph)
            print("此时社区数量:", str(len(cur_com_dict)))
            for com in cur_com_dict.keys():
                cur_com_dict[com] = len(cur_com_dict[com])
            if (not self.communities_changed(cur_com_dict, min_com_dict) \
                    or timecount > time_iterate):
                break
            min_com_dict = cur_com_dict.copy()


        # print(self.cal_EQ(list(community.values()), graph))
        # 排序输出
        # for key, value in min_com_dict.items() :
        #     min_com_dict[key] = sorted(value, reverse=False)
        community = sorted(min_com_dict.items(), key=lambda x:x[1][0], reverse=False)

        return community

    # def propagation(self, graph:nx.Graph, priority_vertice:list, v) \
    #         -> (nx.Graph, list) :
    #     """
    #     标签传播主算法
    #
    #     :param graph: 图存在标签
    #     :param priority_vertice: 图传播顺序
    #     :param v: 阈值系数
    #     :return: 列表，其中每个作为社区
    #     """
    #     labeldict = dict()
    #     for node, data in graph.nodes(data=True) :
    #         labeldict[node] = data["label"]
    #         # labeldict 是字典，key为每个节点，value是标签情况（其中也是字典）
    #     for node in priority_vertice :
    #         maxv = max(labeldict[node].values())
    #         templabel = dict()
    #         for key, value in labeldict[node].items() :
    #             if abs(maxv - value) < 0.00005 :
    #                 templabel[key] = value
    #         if maxv < 1.0/v :
    #             labeldict[node].clear()
    #             labeldict[node] = {random.choice([i for i in templabel.keys()]) : 1.0}  # !!!
    #         else :
    #             sumAverage = 0.0
    #             for key, value in labeldict[node].items() :
    #                 if value < 1.0/v :
    #                     labeldict.pop(key)
    #                     sumAverage += value
    #             for key, value in labeldict[node].items() :
    #                 labeldict[node][key] = value/(1-sumAverage)
    #     # 重新为图"label"赋值
    #     for key, value in labeldict.items() :
    #         graph.nodes[key]["label"] = value.copy()
    #     return graph, labeldict


    def write_communities(self, communities, location) :
        output_file = open(location, 'w')
        for key, value in communities :
            for member in value:
                output_file.write(str(member) + " ")
            output_file.write("\n")
        output_file.close()
        return

    def get_communities(self, graph):
        '''
        生成社区。
        :param graph: 内部图对象。
        :return: {社区标签，社区节点集}字典。
        '''
        # print('Getting communities...')
        com_dict = dict()
        for i, data in graph.nodes(data=True):
            labels = data['label']
            if not labels:
                print('Node ', i, ' has no labels!')
            else:
                for label in labels.keys():
                    if label in com_dict.keys():
                        com_dict[label].add(i)
                    else:
                        com_dict[label] = {i}
        print('Got ', len(com_dict.values()), ' communities.')
        return com_dict

    def i_label_propagation(self, graph: nx.Graph, v) \
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
        priority_vertice, time_iterate = list(G.nodes), 0
        min_communities = None
        while True:

            random.shuffle(priority_vertice)
            time_iterate += 1
            # for nodei in [i[0] for i in priority_vertice]:
            graph, labellist = self.propagation(graph, priority_vertice, v)

            # graph, retry = self.post_processing(graph)

            communities = self.get_communities(labellist)
            print("此时社区数量:", str(len(communities)))
            for com in communities.keys() :
                communities[com] = len(communities[com])
            if time_iterate > 30 or (not self.communities_changed \
                        (communities, min_communities)):
                break
            min_communities = communities.copy()

        return communities


if __name__ == "__main__":

    # graph = {"A": set(["B", "D", "E", "G"]), \
    #          "B": set(["A", "C", "D"]), \
    #          "C": set(["B", "D"]), \
    #          "D": set(["A", "B", "C"]), \
    #          "E": set(["A", "G", "F"]), \
    #          "F": set(["E", "G"]), \
    #          "G": set(["A", "E", "F"])}
    # G = nx.Graph(graph)
    # for node, data in G.nodes(True):
    #     dict = defaultdict(float)
    #     for nodej in G.neighbors(node):
    #         dict[nodej] = 1.0/len(G[node])  # self.hash(nodej)
    #     data["label"] = dict
    copra = COPRA_improvedLPA()

    feature_name = "../data/artificial/on/feat/network100_bd_feat.txt"
    file_name = "../data/artificial/n/network1k.txt"
    G = copra.read_graph(file_name)
    start_time = time.time()
    Glabel = copra.i_label_propagation(G, 2)
    copra.write_communities(Glabel, "../data/network.txt")
    end_time = time.time()
    print("Time spend: %.5f" % (end_time - start_time))
