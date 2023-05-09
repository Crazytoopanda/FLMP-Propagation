import random

import community
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from copra.COPRA_isolate import COPRA_isolate
import onmi as omcode
import numpy as np
import xlsxwriter
from comparative_experiment.SCAN import SCAN
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

    # df3 = pd.read_csv(real_comms_path, sep=' ', header=None)
    df3=pd.read_csv(real_comms_path)
    # hasIndex = False  # 有些社区前面会有编号
    hasIndex = True  # 有些社区前面会有编号

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




def run(edge_path, real_comms_path, feat_path,s):
    G=nx.Graph()
    # 读取边集
    df = pd.read_csv(edge_path, sep=' ', header=None)
    print(df)

    # 加入边
    for i in range(df.shape[0]):
        a = df.iat[i, 0]
        b = df.iat[i, 1]
        # G.add_edge(str(a), str(b))  # 字符型
        G.add_edge(a, b)  # 字符型

    #，准备差分隐私扰动
    G = dp(G,s)

    # 社区发现 -lovain 方法 原论文scan
    print('='*10+'scan'+'='*10)
    algorithm = SCAN(G,0.5,3)
    partition = algorithm.execute()
    print('='*10+'scan-fin'+'='*10)
    print('partition:')
    print(partition)
    res=[]
    for e in partition:
        res.append(set(e))
    print('打印res:')
    print(res)
    print('聚出来几个社区:{0}'.format(len(res)))

    onmi = calc_ONMI(res, redCommunity(real_comms_path))
    # onmi = calc_ONMI(res, load_data(real_comms_path))
    # calc_EQ(edge_path, comms)
    eq_val = calc_EQ(edge_path,res)

    #用copra_isolate里算EQ的代码算一下
    # algorithm=COPRA_isolate()
    # eq_val=algorithm.cal_EQ(partition, G)
    print('onmi={0},eq={1}'.format(onmi,eq_val))

    return onmi,eq_val

if __name__ == '__main__':

    hasIndex = False
    # isReal = False
    isReal = True
    # datatype = 'artificial'
    datatype = 'real'
    dp_s =0.02
    # file_name_list = ['1239671' ,'2363991','5747502','7682452']
    file_name_list = ['7682452']
    # file_name_list = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7']
    # file_name_list = ['1k', '2k', '3k', '4k', '5k']
    # file_name_list = ['1', '2', '3', '4', '5']
    # file_name_list = ['100', '200', '300', '400', '500']
    artificial_file_list=['mu','n','om','on']
    EQ_list=[]
    onmi_list=[]

    if isReal:
        for file_name in file_name_list:
            print('当前是{0}文件'.format(file_name))
            edge_path = '../data/' + datatype + '/' + file_name + '.edges'
            feat_path = '../data/' + datatype + '/feat/' + file_name + '.feat'
            real_path = '../data/' + datatype + '/' + file_name + '.circles'
            onmi,eq_val= run(edge_path, real_path, feat_path, dp_s)
            onmi_list.append(onmi)
            EQ_list.append(eq_val)
    else:
        artificial_file_name = artificial_file_list[1]
        for file_name in file_name_list:
            print('正在处理人工数据集{0}的{1}'.format(artificial_file_name, file_name))
            edge_path = '../data/' + datatype + '/' + artificial_file_name + '/network' + file_name + '.txt'
            feat_path = '../data/' + datatype + '/' + artificial_file_name + '/feat/network' + file_name + '_bd_feat.txt'
            real_path = '../data/' + datatype + '/' + artificial_file_name + '/community' + file_name + '.txt'
            onmi, eq_val = run(edge_path, real_path, feat_path, dp_s)
            onmi_list.append(onmi)
            EQ_list.append(eq_val)

    print('onmi_list.len={0}'.format(len(onmi_list)))
    workbook = xlsxwriter.Workbook(artificial_file_name+' '+'artificial_pig_scan_0.1_3.xlsx')
    # workbook = xlsxwriter.Workbook('aaaaa_pig_scan_0.5_3.xlsx')
    worksheet = workbook.add_worksheet('data')
    for i in range(len(file_name_list)):
        worksheet.write(i, 1, artificial_file_name+'_'+file_name_list[i])
        # worksheet.write(i, 1, 'twitter_'+file_name_list[i])
        worksheet.write(i, 2, EQ_list[i])
        worksheet.write(i, 3, onmi_list[i])
    workbook.close()

        # print("file_name: {0} , nparts: {1} , onmi: {2} , eq: {3}".format(
        #     file_name, nparts, onmi, eq,))
