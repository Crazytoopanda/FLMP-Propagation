import random
# https://blog.csdn.net/weixin_43874070/article/details/109743309
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
    # #对每条边,1-s 的概率保留
    # for i in  range(A.shape[0]):
    #     for j in range(A.shape[1]):
    #         if i<j:
    #             each = random.random()
    #             if each < 1-s :
    #                 continue
    #             else:# 随机生成   0 1
    #                 zero = random.random()
    #                 if zero<0.5:
    #                     A[i][j] = 0
    #                     A[j][i] = 0
    #                 else:
    #                     A[i][j] = 1
    #                     A[j][i] = 1
    #  # 完成扰动的邻接矩阵 准备生成？


def run(edge_path, real_comms_path, feat_path,s):
    print('在run中')
    G=nx.Graph()

    G=nx.read_edgelist(edge_path,nodetype=int)

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

    print('res:')
    print(len(res))
    print(res)
    onmi = calc_ONMI(res, redCommunity(real_comms_path))
    print(onmi)
    return onmi

if __name__ == '__main__':

    hasIndex = False
    isReal = True
    file_type = 'real'
    dp_s =0.02  #(0,1)
    file_name_list = [ 'facebook414']
    nparts=1
    for file_name in file_name_list:
        if isReal:
            edge_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/' + file_name + '.txt'
            feat_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/' + file_name + '_feat.txt'

            real_comms_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/real_' + file_name + '.txt'
        else:
            edge_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/' + 'network' + file_name + '.txt'
            feat_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/' + 'network' + file_name + '_feat.txt'
            real_comms_path = '../datasets/attribute/' + file_type + '/' + str(
                nparts) + '/community' + file_name + '.txt'

        onmi= run(edge_path, real_comms_path, feat_path,dp_s)

        print("信息：file_name: {0} , nparts: {1} , onmi: {2} ".format(
            file_name, nparts, onmi))
