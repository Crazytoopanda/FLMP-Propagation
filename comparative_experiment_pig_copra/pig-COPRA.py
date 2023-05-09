import random
import sys

sys.path.append("../")
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import onmi
import numpy as np
import xlsxwriter
import time
from copra.COPRA_isolate import COPRA_isolate
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
        print("社区长度" + str(len(a)))

        if hasIndex:
            a.pop(0)
        a = set(map(int, a))  # 转换
        print(type(a))
        community.append(a)
    return community


def dp(G, s):  # 差分

    list = [x for x in G.nodes()]
    # 遍历邻接矩阵
    for i in range(len(list)):
        for j in range(len(list)):
            if i > j:
                node1 = list[i]
                node2 = list[j]
                each = random.random()
                if each < 1 - s:
                    continue
                else:  # 随机生成   0 1
                    zero = random.random()
                    if zero < 0.5:  # 移除或者增加
                        if (G.has_edge(node1, node2)):
                            G.remove_edge(node1, node2)
                    else:
                        G.add_edge(node1, node2)
    return G


def run(edge_path, real_comms_path, feat_path, write_path, s):
    seed_node = 'off'
    scale = 0.1
    attribute = 'on'
    v = 2
    algorithm = COPRA_isolate()

    G = COPRA_isolate.read_graph(algorithm, seed_node, scale, edge_path, attribute, feat_path)

    print('边个数：{0}'.format(G.number_of_edges()))
    print('节点个数：{0}'.format(G.number_of_nodes()))

    # 准备差分隐私扰动
    G = dp(G, s)

    partition = algorithm.execute(G)
    print('结果:')
    print(type(partition))
    print(len(partition))

    algorithm.print_communities_to_file(partition, write_path)
    eq = algorithm.cal_EQ(partition, G)
    onmi_val = onmi.cale_onmi(real_path, write_path)

    return onmi_val, eq


if __name__ == '__main__':

    hasIndex = False
    isReal = False
    # isReal = True
    # datatype = 'real'
    datatype = 'artificial'
    dp_s = 0.001  # (0,1)
    # file_name_list = ['0.1' ,'0.2','0.3','0.4','0.5']
    file_name_list = ['10k']
    # file_name_list = ['1k']
    # file_name_list = ['1', '2', '3', '4', '5']
    # file_name_list = ['100', '200', '300', '400', '500']
    # file_name_list = ['1239671' ,'2363991','5747502','7682452']
    # file_name_list = ['7682452']
    artificial_file_list = ['2222-3434', '3221-5342', '4211-3211', '5111-7222', "alone_mu0.1", "alone_mu0.2",
                            "alone_mu0.3", "alone_mu0.4", "alone_mu0.5"]

    file_namea = "10k"
    EQ_list = []
    onmi_list = []
    timex_list = []

    if isReal:
        for file_name in file_name_list:
            onmi_arr = []
            eq_arr = []
            for i in range(50):
                edge_path = '../data/' + datatype + '/' + file_name + '.edges'
                feat_path = '../data/' + datatype + '/feat/' + file_name + '.feat'
                real_path = '../data/' + datatype + '/' + file_name + '.circles'
                write_path = '../data/' + datatype + '/' + file_name + '_re_pig_copra.txt'
                onmi_val, eq = run(edge_path, real_path, feat_path, write_path, dp_s)
                EQ_list.append(eq)
                onmi_list.append(onmi_val)
            #     onmi_arr.append(onmi_val)
            #     eq_arr.append(eq)
            # print('平均值')
            # print(np.mean(eq_arr))
            # print(np.mean(onmi_arr))
            # EQ_list.append(np.mean(eq_arr))
            # onmi_list.append(np.mean(onmi_arr))
    else:

        for file_name in artificial_file_list:
            onmi_arr = []
            eq_arr = []
            for i in range(1):
                print('正在处理人工数据集{0}的{1}的第{2}'.format(file_name, file_namea, i))
                edge_path = '../data/' + datatype + '/' + file_name + '/network' + file_namea + '.txt'
                feat_path = '../data/' + datatype + '/' + file_name + '/feat/network' + file_namea + '_bd_feat.txt'
                real_path = '../data/' + datatype + '/' + file_name + '/community' + file_namea + '.txt'
                write_path = '../data/' + datatype + '/' + file_name + '_re_pig_copra0107.txt'
                start = time.time()
                onmi_val, eq = run(edge_path, real_path, feat_path, write_path, dp_s)
                onmi_arr.append(onmi_val)
                eq_arr.append(eq)
                end = time.time()
                print('平均值')
                print(np.mean(eq_arr))
                print(np.mean(onmi_arr))
                print('人工数据集{0}的{1}的平均eq={2},平均onmi={3}'.format(file_namea, file_namea, np.mean(eq_arr),
                                                                np.mean(onmi_arr)))

                EQ_list.append(np.mean(eq_arr))
                onmi_list.append(np.mean(onmi_arr))
                EQ_list.append(eq)
                onmi_list.append(onmi_val)
                timex_list.append(end-start)
        print("----------------------------")
        print(EQ_list)
        print(onmi_list)
        print(timex_list)

    # workbook = xlsxwriter.Workbook('test'+'_pig_copra_20.xlsx')
    # worksheet = workbook.add_worksheet('data')
    # for i in range(len(file_name_list)):
    #     for i  in range(50):
    #         worksheet.write(i, 1, file_name_list[0])
    #         worksheet.write(i, 2, EQ_list[i])
    #         worksheet.write(i,3,onmi_list[i])
    # workbook.close()
