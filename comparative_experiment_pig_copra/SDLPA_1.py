"""
SDLPA 对比算法
平均化每个参与方acopra下的eq和onmi
@author: lfa
@update: 2023/4/22
"""

import random
import sys

sys.path.append("../")
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import onmi
import numpy as np
import networkx as nx
import xlsxwriter
from copra.COPRA_isolate import COPRA_isolate
from fmlpa import EQ
from utils.tools import jaccard_sim, read_comms, calc_ONMI, calc_EQ, save_comms
import time


def print_communities_to_file(communities, output_path):
    output_file = open(output_path, 'w')
    for cmu in communities:
        for member in cmu:
            output_file.write(member + " ")
        output_file.write("\n")
    output_file.close()
    return


def run(edge_path, real_comms_path, feat_path, write_path):
    seed_node = 'off'
    scale = 0.1
    attribute = 'on'
    v = 2
    algorithm = COPRA_isolate()

    G = COPRA_isolate.read_graph(algorithm, seed_node, scale, edge_path, attribute, feat_path)

    print('边个数：{0}'.format(G.number_of_edges()))
    print('节点个数：{0}'.format(G.number_of_nodes()))

    partition = algorithm.execute(G)
    print('结果:')
    print(type(partition))
    print(len(partition))

    algorithm.print_communities_to_file(partition, write_path)
    eq = algorithm.cal_EQ(partition, G)
    onmi_val = onmi.cale_onmi(real_path, write_path)

    print("eq:", eq)
    print("onmi:", onmi_val)

    return onmi_val, eq, G, partition


if __name__ == '__main__':

    hasIndex = False
    isReal = False
    # isReal = True
    # datatype = 'real'
    datatype = 'artificial'
    party = "4"
    # file_name_list = ['0.1' ,'0.2','0.3','0.4','0.5']
    file_name = '10k'
    # file_name_list = ['1k']
    # file_name_list = ['1', '2', '3', '4', '5']
    # file_name_list = ['100', '200', '300', '400', '500']
    # file_name_list = ['1239671' ,'2363991','5747502','7682452']
    # file_name_list = ['7682452']
    artificial_file_list = ['2222-3434', '3221-5342', '4211-3211', '5111-7222', "alone_mu0.1", "alone_mu0.2",
                            "alone_mu0.3", "alone_mu0.4", "alone_mu0.5"]
    EQ_list = []
    onmi_list = []
    _real_eo_list = []

    if isReal:
        for file_name in artificial_file_list:
            onmi_arr = []
            eq_arr = []
            for i in range(50):
                edge_path = '../data/' + datatype + '/' + file_name + '.edges'
                feat_path = '../data/' + datatype + '/feat/' + file_name + '.feat'
                real_path = '../data/' + datatype + '/' + file_name + '.circles'
                write_path = '../data/' + datatype + '/' + file_name + '_re_pig_copra.txt'
                onmi_val, eq, G, partition = run(edge_path, real_path, feat_path, write_path)
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

        for artificial_file_name in artificial_file_list:
            community = []
            onmi_arr = []
            eq_arr = []
            write_path = '../data/' + datatype + '/' + artificial_file_name + '/' + '/network' + file_name + '_' + '_lfa_re.txt'
            real_path = '../data/' + datatype + '/' + artificial_file_name + '/' + party + '/community' + file_name + '.txt'
            real_edge_path = "../data/" + datatype + "/" + artificial_file_name + "/network" + file_name + ".txt"
            feat_path = '../data/' + datatype + '/' + artificial_file_name + '/feat/network' + file_name + '_bd_feat.txt'
            start = time.time()
            for i in range(int(party)):
                print('正在处理人工数据集{0}的{1}的第{2}'.format(artificial_file_name, file_name, i))
                edge_path = '../data/' + datatype + '/' + artificial_file_name + '/' + party + '/network' + file_name + '_' + str(
                    i) + '.txt'
                write_path1 = '../data/' + datatype + '/' + artificial_file_name + '/' + '/network' + file_name + '_' + str(
                    i) + '_lfa_re.txt'

                onmi_val, eq, G, partition = run(edge_path, real_path, feat_path, write_path1)
                community.extend(list(partition))

                onmi_arr.append(onmi_val)
                eq_arr.append(eq)
                print('平均值')
                print(np.mean(eq_arr))
                print(np.mean(onmi_arr))
                print('人工数据集{0}的{1}的平均eq={2},平均onmi={3}'.format(artificial_file_name, file_name, np.mean(eq_arr),
                                                                np.mean(onmi_arr)))
                EQ_list.append(np.mean(eq_arr))
                onmi_list.append(np.mean(onmi_arr))
                EQ_list.append(eq)
                onmi_list.append(onmi_val)

            print_communities_to_file(community, write_path)

            seed_node = 'off'
            scale = 0.1
            attribute = 'on'
            v = 2

            G_sum = COPRA_isolate.read_graph(COPRA_isolate(), seed_node, scale, real_edge_path, attribute, feat_path)
            eq = EQ.cal_EQ(community, G_sum)
            end = time.time()
            onmi_val = onmi.cale_onmi(real_path, write_path)
            print("eq:", eq)
            print("onmi:", onmi_val)
            _real_eo_list.append([eq, onmi_val, end - start])
        print(_real_eo_list)
    # workbook = xlsxwriter.Workbook('test'+'_pig_copra_20.xlsx')
    # worksheet = workbook.add_worksheet('data')
    # for i in range(len(file_name_list)):
    #     for i  in range(50):
    #         worksheet.write(i, 1, file_name_list[0])
    #         worksheet.write(i, 2, EQ_list[i])
    #         worksheet.write(i,3,onmi_list[i])
    # workbook.close()
