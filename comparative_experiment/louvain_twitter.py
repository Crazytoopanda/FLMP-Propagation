import random

import community
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
from utils.tools import jaccard_sim, read_comms, calc_ONMI, calc_EQ, save_comms
def redCommunity1(real_comms_path):
    df3 = pd.read_csv(real_comms_path, header=None)

    hasIndex = False  # 有些社区前面会有编号
    community = []
    for i in range(df3.shape[0]):
        a = (df3.iat[i, 0].split(' '))
        print(a)

        if hasIndex:
            a.pop(0)
        a = set(map(int, a))  # 转换
        print(type(a))
        community.append(a)
    return community
def redCommunity(real_comms_path):

    df3 = pd.read_csv(real_comms_path, sep=' ', header=None)
    hasIndex = False  # 有些社区前面会有编号
    community = []
    for i in range(df3.shape[0]):
        a = (df3.iat[i, 0].split('\t'))
        print("社区长度"+str(len(a)))

        if hasIndex:
            a.pop(0)
        a = set(map(int, a)) #转换
        print(type(a))
        community.append(a)
    return community
def dp(G,s): #差分

    list=[x for x in G.nodes()]
    # 遍历邻接矩阵
    for i in range(len(list)):
        for j in range(len(list)):
            if i>j:
                node1=list[i]
                node2=list[j]
                each = random.random()
                if each < 1 - s:
                    continue
                else:  # 随机生成   0 1
                    zero = random.random()
                    if zero < 0.5:#移除或者增加
                        if(G.has_edge(node1,node2)):
                            G.remove_edge(node1, node2)
                    else :
                        G.add_edge(node1, node2)
    return G



def run(edge_path, real_comms_path, feat_path,s,party):

    G=nx.Graph()
    # 读取边集
    for i in range(int(party)):
        # G = nx.read_edgelist(edge_path[i],nodetype=int)# nodetype=int
        G.add_edges_from(nx.read_edgelist(edge_path[i],nodetype=int).edges())
        print('第{0}轮的节点个数：{1}'.format(i,G.number_of_nodes()))
        print('第{0}轮的边个数：{1}'.format(i,G.number_of_edges()))

    print('全部读完的节点数：{0} 边数：{1}'.format(G.number_of_nodes(),G.number_of_edges()))

    #，准备差分隐私扰动
    G = dp(G,s)

    # 社区发现 -lovain 方法 原论文scan
    partition = community.best_partition(G)

    print(partition)
    count=list(set([i for i in partition.values()]))
    print(count)
    print(len(count))

    res=[]
    for value in count:
        res.append(set([k for k,v in partition.items() if v == value]))

    print('louvain的partrition的东西：')
    print(type(res))
    print(res)
    print(type(res[0]))
    # copra


    onmi = calc_ONMI(res, redCommunity(real_comms_path))
    print(onmi)

    print('res.type{0}'.format(type(res)))
    return onmi

if __name__ == '__main__':

    hasIndex = False
    isReal = True
    file_type = 'real'
    dp_s =0.02  #(0,1)
    file_name_list = [ '1239671']
    nparts=1
    # 以下是我写的
    parties = ['2', '4', '6', '8', '10']
    party = '2'
    datatype='real'
    edge_path = []
    for file_name in file_name_list:
        if isReal:
            # for party in parties:
            for i in range(int(party)):
                edge_path.append('../data/' + datatype + '/' + party + '/' + file_name + '_{}.txt'.format(i))

            feat_path = '../data/' + datatype + '/feat/' + file_name + '.feat'
            real_comms_path = '../data/' + datatype + '/' + party + '/' + file_name + '.circles'

        else:
            edge_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/' + 'network' + file_name + '.txt'
            feat_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/' + 'network' + file_name + '_feat.txt'
            real_comms_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/community' + file_name + '.txt'

        onmi= run(edge_path, real_comms_path, feat_path,dp_s,party)

        print("file_name: {0} , nparts: {1} , onmi: {2} ".format(
            file_name, nparts, onmi))
