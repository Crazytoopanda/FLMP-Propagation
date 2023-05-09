# -*- coding: utf-8 -*-
# @Time    : 2019/11/12
# @Author  : yz
# @Version : 1.0

# from phe import paillier
import sys
sys.path.append("..")
import random
import  time
# import copy
from collections import defaultdict
# from intersect_mp.driver import Intersect
from intersect.driver import Intersect
import numpy as np
from intersect.tools import IntersectTools

from scipy.special import comb
import paillierT


class COPRA_Host(object):
    def __init__(self,host_data,n):
        self.other_hosts=[]
        self.intersect_idx=[]#和其他各方的重叠节点集
        self.intersect_host_data=[]#和其他各方重叠节点的信息
        self.other_host_data=[]#当前方除重叠节点外节点的信息
        self.data=host_data#初始图信息
        self.intersect_data_com=[]#重叠节点全局完整信息
        self.nodelabelpair = []
        
    def clear_data(self):
        self.intersect_host_data=[]
        self.other_host_data=[]
        self.intersect_data_com=[]
        self.nodelabelpair = []
        
    def send_paillier_params(self,host):
        host.receive_paillier_params(self.public_key,self.private_key)
        self.other_hosts.append(host)
        
    def send_pk_to_C(self,Coordinator):
        Coordinator.receive_pk(self.public_key,self.private_key)
    
    def send_nodedegree(self,Coordinator):
        degree = list(self.data.degree())
        Coordinator.receive_nodedegree(degree)
        
    def send_intersect_Hid(self,Coordinator):
        intersect_id = set()
        for i in range(len(self.intersect_idx)):
            intersect_id = intersect_id | set(self.intersect_idx[i])
        self.intersect_id = intersect_id
        intersect_Hid = []
        for node in intersect_id:
            for label in self.data.nodes[node]['label']:
                intersect_Hid.append(label)
        Coordinator.receive_intersect_Hid(set(intersect_Hid))
    
    def receive_paillier_params(self,public_key,private_key):
        self.public_key=public_key
        self.private_key=private_key
        
    def receive_seednodes(self,seednodes):
        self.seednodes = seednodes
        
    def receive_hton(self,hton,MIN,MAX):
        self.MIN = MIN
        self.MAX = MAX
        self.hton = hton
        
    def transform_hton(self):
        total_node = self.data.nodes()
        ln = len(total_node) - len(self.intersect_id)
        numlist = random.sample(range(self.MIN,self.MAX),ln)
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
                self.data.nodes[node]['label'] = {self.hton[label]:1}
        
    def save_intersect_data(self,intersect_host_data):
        self.intersect_host_data=intersect_host_data
        
    def save_other_data(self,other_host_data):
        self.other_host_data=other_host_data
        
    # def receive_intersect_data_com(self,nodeitem):
    #     '''
    #     从C端接收本参与方的重叠结点完整信息
    #     '''
        # self.intersect_data_com.append(nodeitem)
        
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
        
    def get_intersect_id(self,nodeset):
        '''
                :param nodeset: user id list from host and guest(i)
                :return: intersection of their idx
        '''
        intersect = Intersect()
        self.intersect_idx = intersect.run(nodeset,self.data)
        
    def add_attr_to_node(self,A):
        for node in self.data:
            self.data.nodes[node]['attr'] = A[node]
            
    def cale_attr_similarity(self,vi,vj):
        vi = self.data.nodes[vi]["attr"]
        vj = self.data.nodes[vj]["attr"]
        Sa = 1.0 * (np.sum(vi == vj) / len(vi))
        # print(Sa)
        return round(Sa,6)
    
    def get_intersect_host_data(self,G,intersect_idx_raw,attribute,k):
        '''
                  :param G: graph from host
                  :param intersect_idx_raw: intersection of their idx
                  :param k:混淆参数
                  :return:{(vi,{lij, nlij})|vi∈XA ∩XB}
          '''
        intersect_host_data = []
        for node in intersect_idx_raw:
            # print(node)
            data = []
            dict = {}
            data.append(node)
            l = 0
            for neighbor_index in G.neighbors(node):
                l += 1
                if attribute == 'on':
                    Sa = self.cale_attr_similarity(node, neighbor_index)
                # print(Sa)
                # print(G.nodes[neighbor_index])
                neighbor_label = G.nodes[neighbor_index]["label"]
                # print(neighbor_label)
                for m in neighbor_label.keys():
                    if attribute == 'on':
                        value = round(neighbor_label.get(m),6)*Sa #Saij*nlij
                    else:
                        value = round(neighbor_label.get(m),6)
                    dict[m] = dict.setdefault(m, 0) + value
            # 生成权重为0的标签
            num = int((l / k)*(1-k))
            labels = list(range(100000,100000+num))
            for i in range(num):
                label = IntersectTools.hash(labels[i])
                dict[label] = dict.setdefault(label, 0)

            data.append(dict)
            intersect_host_data.append(data)
        # intersect_host_data = self.normalize(intersect_host_data)
        # print("host_data:",intersect_host_data)
        return intersect_host_data

    def get_other_host_data(self,G, intersect_idx_raw,attribute):
        '''
                  :param G: graph from host
                  :param intersect_idx_raw: intersection of their idx
                  :return:{(vi,{lij, nlij})|vi∈XA & ∉XB}
        '''
        other_host_data = []
        for node in G.nodes:
            if node not in intersect_idx_raw:
                data = []
                dict = {}
                data.append(node)
                for neighbor_index in G.neighbors(node):
                    if attribute == 'on':
                        Sa = self.cale_attr_similarity(node,neighbor_index)
                    neighbor_label = G.nodes[neighbor_index]["label"]
                    for k in neighbor_label.keys():
                        if attribute == 'on':
                            value = round(neighbor_label.get(k),6)*Sa #Saij*nlij
                        else:
                            value = round(neighbor_label.get(k),6)
                        dict[k] = dict.setdefault(k, 0) + value
                data.append(dict)
                other_host_data.append(data)
        other_host_data = self.normalize(other_host_data)
        # print('other_host_data',other_host_data)
        return other_host_data

    # 加密并发送给C端
    def encrypt_host_data(self,intersect_host_data, intersect_idx_raw,mi):
        '''
                :param intersect_host_data:{(vi,{lij, nlij})|vi∈XA ∩XB}
                :param intersect_idx_raw: intersection of their idx
                :return: {(vi,{(H(lij), E(nlij))})|vi∈XA ∩XB}
                '''
        for i in range(len(intersect_idx_raw)):
            for x, y in list(intersect_host_data[i][1].items()):
                intersect_host_data[i][1].update({x: self.public_key.Encrypt(int(y*100000))})
                
                # intersect_host_data[i][1].update({x: int(y*100000)})
                # if type(x) == str:
                #     intersect_host_data[i][1].update({x: self.public_key.Encrypt(
                #         int(y*10**(mi+7)))})
                # else:
                #     intersect_host_data[i][1].update({x: self.public_key.Encrypt(
                #         int(y*10**(mi+7)+x*10**(mi+1)))})
        return intersect_host_data
    
    # 归一化函数
    def normalize(self,data):
        for i in range(len(data)):
            sum=0
            for x, y in list(data[i][1].items()):
                sum+=y
            # print(sum)
            for x, y in list(data[i][1].items()):
                data[i][1].update({x: round(y/sum,6)})
        # print(data)
        return data
    
    #判断是否满足标签权重全等于阈值
    def judge_labels(self,c1,c2,c3):
        # w1 = self.private_key.Decrypt(c1.value)
        # w2 = self.private_key.Decrypt(c2.value)
        # w3 = self.private_key.Decrypt(c3.value)
        # print("after: 传之后是什么type" )
        # print(type(c1))
        # print(type(c2))
        # print(type(c3))
        w1 = c1.value
        w2 = c2.value
        w3 = c3.value
        if w1 == w2 and w3 == 0:
            return True
        else:
            return False
    
    # 解密,标签传播
    def label_propagate(self,G):
        # 更新标签
        for nl in self.nodelabelpair:
            label = dict()
            length = len(nl[1])
            for la in nl[1]:
                label.update({la:1/length})
            G.nodes[nl[0]]["label"] = label

    # 归一化并更新host的其他标签
    def populate_other_host_label(self,G,v):
        '''
           :param G:the graph of host
          :param other_guest_data: the data of host |vi∈XB and ∉XA
        '''
        other_host_data=self.other_host_data

        for i in range(len(other_host_data)):
            sum = 0
            maxc = max(other_host_data[i][1].values())
            a = [item[0] for item in other_host_data[i][1].items() if abs(item[1]-maxc) <= 0.000005]
            if maxc < 1 / float(v):
                other_host_data[i][1].clear()
                # m = random.choice(a) #随机性
                m = max(a)
                other_host_data[i][1][m] = 1
            else:
                for x, y in list(other_host_data[i][1].items()):
                    if y < 1/float(v):
                        other_host_data[i][1].pop(x)
                        sum += y
                for x, y in list(other_host_data[i][1].items()):
                    other_host_data[i][1].update({x: round(y/(1-sum),6)})
            # 更新标签
            G.nodes[other_host_data[i][0]]["label"] = other_host_data[i][1]

    def load_data(self,path):
            with open(path, "r") as f:
                text = f.read()
            com = []
            for line in text.split("\n"):
                arr = line.strip().split()
                # arr = list(map(int, arr))
                com.append(arr)
            return com
            
     # def encrypt(self, item_label_weight):
     #    item_label_weight = self.public_key.encrypt(item_label_weight)
     #    return item_label_weight

     # def decrypt(self, item_label_weight):
     #    item_label_weight = self.private_key.decrypt(item_label_weight)
     #    return item_label_weight

    def assign_labels(self):
        graph = self.data
        seed = self.seednodes
        # print(seed)
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
                if len(seed_index):
                    seed_choice = random.choice(list(seed_index))
                else:
                    seed_choice = random.choice(seed)
                dict = defaultdict(float)
                dict[IntersectTools.hash(seed_choice)] = 1
                data['label'] = dict
            # print(graph.nodes(node))
        return graph

    # def cale_degree_leakage(self,seed_node):
    #     #计算重叠节点
    #     n = len(self.intersect_idx)
    #     intersect_node = set()
    #     for part in self.intersect_idx:
    #         intersect_node = intersect_node | part
    #     node_num = len(intersect_node)
    #     # print(node_num)
        
    #     #猜测全局节点最大度
    #     label = []
    #     for node in list(self.data.degree()):
    #         label.append(node[1])
    #     max_degree = max(label)
    #     # print(max_degree)
    #     # print('data:',len(self.data.degree()))
    #     # print('intersect_host_data:',len(self.intersect_host_data))
    #     # print('intersect_idx:',len(self.intersect_idx))
        
    #     #计算节点实际增加度
    #     degreeup=dict()
    #     degreenow=dict()
    #     degree_init=list(self.data.degree())
    #     # degree_init.sort(key = lambda degree:degree[0],reverse = True)
    #     # print(self.intersect_data_com)
    #     for node in self.intersect_data_com:
    #         key = node[0]
    #         lws = node[1]
    #         value = 0
    #         for idx in lws.keys():
    #             value+=self.decrypt(lws[idx])
    #         degreenow[key] = round(value)
    #     for nd in degree_init:
    #         if nd[0] in intersect_node:
    #             degreeup[nd[0]] = degreenow[nd[0]] - nd[1]
    #     # print('degreenow:',len(degreenow))        
    #     # print('degreeup:',degreeup)
    #     # print(min(degreeup.values()))
        
    #     #计算节点标签数
    #     label_num=dict()
    #     for node in self.intersect_data_com:
    #         key = node[0]
    #         value = len(node[1])
    #         label_num[key] = value
    #     # print(max(label_num.values()))
    #     #计算节点度泄露
    #     leakagelist = []
    #     if seed_node == 'on':
    #         for node in intersect_node:
    #             l = label_num[node]
    #             d = degreeup[node]
    #             C = comb(n - 2 + d, d, exact=True)
    #             # print(l,d)
    #             # print(C)
    #             if C == 0 and max_degree - l != 0:
    #                 p = 1 / ((max_degree - l) * 1)
    #             elif max_degree - l == 0 and C != 0:
    #                 p = 1 / (1 * C)
    #             elif max_degree - l == 0 and C == 0:
    #                 p = 1
    #             else:
    #                 p = 1 / ((max_degree - l) * C)
    #             leakagelist.append(p)
    #         ave_leakage = sum(leakagelist)/node_num
    #     else:
    #         for node in intersect_node:
    #             d = degreeup[node]
    #             C = comb(n - 2 + d, d, exact=True)
    #             if C == 0:
    #                 p = 1
    #             else:
    #                 p = 1 / C
    #             leakagelist.append(p)
    #         ave_leakage = sum(leakagelist)/node_num
        
    #     return ave_leakage
        
