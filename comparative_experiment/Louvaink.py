import random
# https://blog.csdn.net/weixin_43874070/article/details/109743309
import sys

sys.path.append("../")
import community
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import collections
import onmi
import xlsxwriter
from utils.tools import jaccard_sim, read_comms, calc_ONMI, calc_EQ, save_comms
def redCommunity_artificial(real_comms_path):
    with open(real_comms_path, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        numbers = list(map(int, line.strip().split()))
        data.append(set(numbers))
    print("data读出来的{}".format(data))
    return data
def redCommunity_real(real_comms_path):

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
        # print("redCommunity读出来的{}".format(type(community[0].pop())))
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

def cal_EQ(cover1, G):
    cover = [[val for val in set_val] for set_val in cover1]
    m = len(G.edges(None, False))  # 如果为真，则返回3元组（u、v、ddict）中的边缘属性dict。如果为false，则返回2元组（u，v）
    # 存储每个节点所在的社区
    vertex_community = collections.defaultdict(lambda: set())
    # i为社区编号(第几个社区) c为该社区中拥有的节点
    for i, c in enumerate(cover):
        # v为社区中的某一个节点
        for v in c:
            # 根据节点v统计他所在的社区i有哪些
            vertex_community[v].add(i)
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
    return round(total / (2 * m), 4)

def print_communities_to_file(communities1, output_path):
    communities = [[val for val in set_val] for set_val in communities1]
    output_file = open(output_path, 'w')
    for cmu in communities:
        for member in cmu:
            output_file.write(str(member) + " ")
        output_file.write("\n")
    output_file.close()
    return

def run(edge_path, real_comms_path, feat_path,s):
    print('在run中')
    G=nx.Graph()

    G=nx.read_edgelist(edge_path,nodetype=int)

    #，准备扰动
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
    # onmi = calc_ONMI(res, redCommunity(real_comms_path))
    # print_communities_to_file(res,write_path)
    G1=nx.read_edgelist(edge_path,nodetype=int)
    # re = [calc_ONMI(res, redCommunity_real(real_comms_path)),cal_EQ(res,G1)]
    re = [calc_ONMI(res, redCommunity_artificial(real_comms_path)),cal_EQ(res,G)]
    return re

if __name__ == '__main__':

    hasIndex = False
    # isReal = True
    isReal = False
    # file_type = 'real'
    file_type = 'as'
    # file_type = 'n'
    # file_type = 'ni'
    dp_s =0.01  #(0,1)
    # dp_s = 0.1
    onmi_list = []
    EQ_list = []
    # file_name_list = ['1239671' ,'2363991','5747502','7682452']
    # file_name_list = ['1239671']
    file_name_list = ['10k']
    # file_name_list = ['0.1']
    # file_name_list = ['1k','2k','3k','4k','5k']
    # file_name_list = ['0.8' , '1.0' ,'1.5' ,'3.5']
    nparts=2
    for file_name in file_name_list:
        if isReal:
            edge_path = '../data/artificial/' + file_type + '/' + file_name + '.edges'
            feat_path = '../data/artificial/' + file_type + '/' + file_name + '_feat.txt'

            real_comms_path = '../data/artificial/' + file_type + '/' + file_name + '.circles'
        else:
            edge_path = '../data/artificial/' + file_type + '/' + 'network' + file_name + '.txt'
            feat_path = '../data/artificial/' + file_type + '/' + 'network' + file_name + '_feat.txt'
            real_comms_path = '../data/artificial/' + file_type + '/community' + file_name + '.txt'
            write_path = '../data/artificial/' + file_type + '/community' + file_name + '_re_hqq_0102_isolate_copra.txt'
        re= run(edge_path, real_comms_path, feat_path,dp_s)

        print("信息：file_name: {0} , nparts: {1} , onmi: {2} , eq: {3}".format(
            file_name, nparts, re[0], re[1]))
        EQ_list.append(re[1])
        onmi_list.append(re[0])

    workbook = xlsxwriter.Workbook('louvain.xlsx')
    worksheet = workbook.add_worksheet('data')
    for i in range(len(file_name_list)):
        worksheet.write(i, 1, file_name_list[i])
        worksheet.write(i, 2, EQ_list[i])
        worksheet.write(i, 3, onmi_list[i])
    workbook.close()