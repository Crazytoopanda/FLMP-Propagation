"""
COPRA_Reviewer联邦化参与方

@author: Lfa
update: 2022/9/26
"""
import random
from collections import defaultdict
from COPRA_coordinator import COPRA_Coordinator
import numpy as np
import networkx as nx
import paillierT
from intersect.driver import Intersect
from intersect.tools import IntersectTools
from LeaderRank import leader_rank

class COPRA_Host(object):

    def __init__(self,host_data,n):
        self.other_hosts=[]
        # 和其他各方的重叠节点集
        self.intersect_idx=[]
        # 和其他各方重叠节点的信息
        self.intersect_host_data=[]
        # 当前方除重叠节点外节点的信息
        self.other_host_data=[]
        # 初始图信息
        self.data=host_data
        # 重叠节点全局完整信息
        self.intersect_data_com=[]
        self.nodelabelpair = []

    def clear_data(self):
        self.intersect_host_data=[]
        self.other_host_data=[]
        self.intersect_data_com=[]
        self.nodelabelpair = []

    def send_paillier_params(self,host):
        host.receive_paillier_params(self.public_key,self.private_key)
        self.other_hosts.append(host)

    def send_key_to_coordinator(self, Coordinator):
        Coordinator.receive_key(self.public_key,self.private_key)

    def send_nodedegree(self, Coordinator):
        degree = list(self.data.degree())
        Coordinator.receive_nodedegree(degree)

    def send_intersect_Hid(self, Coordinator):
        intersect_id = set()
        for i in range(len(self.intersect_idx)):
            intersect_id = intersect_id | set(self.intersect_idx[i])
        self.intersect_id = intersect_id
        intersect_Hid = []
        for node in intersect_id:
            for label in self.data.nodes[node]['label']:
                intersect_Hid.append(label)
        Coordinator.receive_intersect_Hid(set(intersect_Hid))

    def receive_paillier_params(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def receive_seednodes(self,seednodes):
        self.seednodes = seednodes

    def receive_hton(self,hton,MIN,MAX):
        self.MIN = MIN
        self.MAX = MAX
        self.hton = hton

    def save_intersect_data(self, intersect_host_data):
        self.intersect_host_data = intersect_host_data

    def save_other_data(self, other_host_data):
        self.other_host_data = other_host_data

    def receive_nodelabelpair(self,nlpair):
        '''
        从C端接收本参与方重叠节点更新方案
        '''
        self.nodelabelpair.append(nlpair)

    def params_init(self):
        key_length = 128  # paillier秘钥长度
        public_key, private_key = paillierT.generate_paillier_keypair(key_length)  # paillier秘钥
        self.public_key=public_key
        self.private_key=private_key

    def get_intersect_id(self, nodeset):
        '''
        : 得到重叠节点的名称

        :param nodeset: user id list from host and guest(i)
        :return: intersection of their idx
        '''
        intersect = Intersect()
        self.intersect_idx = intersect.run(nodeset, self.data)

    def transform_hton(self):
        total_node = self.data.nodes()
        ln = len(total_node) - len(self.intersect_id)
        numlist = random.sample(range(self.MIN, self.MAX), ln)
        # print('t',len(total_node))
        for node in total_node:
            if node not in self.intersect_id:
                num = random.choice(numlist)
                numlist.remove(num)
                for label in self.data.nodes[node]['label']:
                    self.hton[label] = num
        # print('h',len(self.hton.keys()))
        self.ntoh = dict()
        for Hnode in self.hton.keys():
            self.ntoh[self.hton[Hnode]] = Hnode

        for node in total_node:
            for label in self.data.nodes[node]['label'].keys():
                self.data.nodes[node]['label'] = {self.hton[label]: 1}

    def add_attribute_to_node(self,A):
        for node in self.data:
            self.data.nodes[node]['attr'] = A[node]

    def calc_attribute_similarity(self,vi,vj):
        vi = self.data.nodes[vi]["attr"]
        vj = self.data.nodes[vj]["attr"]
        Sa = 1.0 * (np.sum(vi == vj) / len(vi))
        # print(Sa)
        return round(Sa,6)

    def get_intersect_host_data(self, G:nx.Graph, intersect_idx_raw,
                                attribute, k):
        """
        :param G: 参与方的Graph图
        :param intersect_idx_raw: intersection of their idx
        :param k: 混淆参数
        :return: {(vi,{lij, nlij})|vi为重叠节点}
        """

        intersect_host_datas = []
        for node in intersect_idx_raw:
            datas, data_dict = [], {}
            datas.append(node)
            count = 0
            for neighbor_node in G.neighbors(node):
                count += 1
                if attribute == 'on':
                    Sa = self.calc_attribute_similarity(
                        neighbor_node, node)
                neighbor_label = G.nodes[neighbor_node]["label"]
                for m in neighbor_label.keys():
                    value = 0
                    if attribute == 'on':
                        value = round(neighbor_label.get(m), 6) * Sa #Saij*nlij
                    else:
                        value = round(neighbor_label.get(m), 6)
                    data_dict[m] = data_dict.setdefault(m, 0) + value
            num = int((count / k) * (1 - k))
            labels = list(range(100000, 100000 + num))
            for i in range(num):
                label = IntersectTools.hash(labels[i])
                data_dict[label] = data_dict.setdefault(label, 0)

            datas.append(data_dict)
            intersect_host_datas.append(datas)
        return intersect_host_datas

    def normalize(self, graph:nx.Graph, priority_vertice) -> nx.Graph:
        for node, data in graph.nodes(data=True):
            if node in priority_vertice:
                tempdict = defaultdict(float)
                degree = graph.degree[node]
                for neighbor in graph.neighbors(node):
                    for neig_node, neig_data in graph.nodes[neighbor]["label"].items():
                        tempdict[neig_node] += neig_data / degree
                data["label"] = tempdict.copy()
        return graph

    def normalize_list(self,data):
        for i in range(len(data)):
            sum=0
            for x, y in list(data[i][1].items()):
                sum+=y
            # print(sum)
            for x, y in list(data[i][1].items()):
                data[i][1].update({x: round(y/sum,6)})
        # print(data)
        return data

    def get_other_host_data(self,G:nx.Graph, intersect_idx_raw,attribute):
        """

        :param G: 参与方的Graph图
        :param intersect_idx_raw: intersection of their idx
        :param attribute:
        :return: {(vi,{lij, nlij})|vi本图的非重叠节点}
        """

        other_host_datas = []
        for node in G.nodes:
            if node not in intersect_idx_raw:
                datas, data_dict = [], {}
                datas.append(node)
                for neighbor_index in G.neighbors(node):
                    if attribute == 'on':
                        Sa = self.calc_attribute_similarity(node, neighbor_index)
                    neighbor_label = G.nodes[neighbor_index]["label"]
                    for k in neighbor_label.keys():
                        if attribute == 'on':
                            value = round(neighbor_label.get(k), 6) * Sa  # Saij*nlij
                        else:
                            value = round(neighbor_label.get(k), 6)
                        data_dict[k] = data_dict.setdefault(k, 0) + value
                datas.append(data_dict)
                other_host_datas.append(datas)
        other_host_datas = self.normalize_list(other_host_datas)
        return other_host_datas

    def encrypt_host_data(self, intersect_host_data, intersect_idx_raw, mi):
        """
        :param intersect_host_data:c{(vi,{lij, nlij})|vi为重叠节点}
        :param intersect_idx_raw: intersection of their idx
        :return: {(vi,{(H(lij), E(nlij))})|vi为重叠节点}
        """
        for i in range(len(intersect_idx_raw)):
            for x, y in list(intersect_host_data[i][1].items()):
                intersect_host_data[i][1].update({x: self.public_key.Encrypt(int(y * 100000))})
        return intersect_host_data

    def label_propagate(self,G):
        # 更新标签
        for nl in self.nodelabelpair:
            label = dict()
            length = len(nl[1])
            for la in nl[1]:
                label.update({la:1/length})
            G.nodes[nl[0]]["label"] = label
        return G

    def propagation(self, graph:nx.Graph, priority_vertice:list, v:int) \
                    -> nx.Graph:
        """
        标签传播主算法

        :param graph: 图存在标签
        :param priority_vertice: 图传播顺序
        :param v: 阈值系数
        :return: 列表，其中每个作为社区
        """
        labeldict = dict(self.other_host_data)

        # graph = self.normalize(graph, priority_vertice)

        for node in priority_vertice:

            sum_node_label = labeldict[node].copy()

            max_label_value = max(sum_node_label.values())
            if max_label_value < 1.0 / v:
                labeldict[node].clear()
                for label in sum_node_label.keys():
                    if max_label_value == sum_node_label[label]:
                        labeldict[node] = {label: 1.0}
                        break
            else:
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
        return graph

    def spawn_prior_vertice(self, G:nx.Graph, other_host_data):
        raw_priority_vertice = [i[0] for i in sorted(leader_rank(G).items(),
                                key=lambda x: x[1], reverse=True)]
        priority_vertice = []
        for node in raw_priority_vertice:
            if node in [item[0] for item
                        in other_host_data]:
                priority_vertice.append(node)
        return priority_vertice

    def populate_other_host_label(self, G, v):
        '''
            :param G:the graph of host
            :param other_guest_data: the data of host |vi∈XB and ∉XA
        '''
        other_host_data = self.other_host_data
        priority_vertice = self.spawn_prior_vertice(G, other_host_data)
        G = self.propagation(self.label_propagate(G), priority_vertice, v)

    def assign_labels(self):
        graph = self.data
        seed = self.seednodes
        # print(seed)
        for node, data in graph.nodes(True):
            # 赋予种子节点标签
            if node in seed:
                dict = defaultdict(float)
                dict[IntersectTools.hash(node)] = 1
                data['label'] = dict
            # 根据规则赋予其他节点标签

            if node not in seed:
                neighbor_index = graph.neighbors(node)
                seed_index = set(seed) & set(neighbor_index)
                if len(seed_index):
                    seed_choice = random.choice(list(seed_index))
                else:
                    seed_choice = random.choice(seed)
                dict = defaultdict(float)
                dict[IntersectTools.hash(seed_choice)] = 1
                data['label'] = dict
            # print(graph.nodes(node))
        return graph

    def load_data(self,path):
        with open(path, "r") as f:
            text = f.read()
        com = []
        for line in text.split("\n"):
            arr = line.strip().split()
            # arr = list(map(int, arr))
            com.append(arr)
        return com
    def judge_labels(self,c1,c2,c3):
        w1 = c1.value
        w2 = c2.value
        # w3 = c3.value
        if w1 == w2 and c3 == 0:
            return True
        else:
            return False