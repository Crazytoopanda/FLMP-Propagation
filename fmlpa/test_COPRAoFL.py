# -*- coding: utf-8 -*-
# @Author  : yz
# @Version : 1.0
# @Time    : 2019/12/16
# import unittest
# from graph.community_detection.corpaoml_al_mp.COPRA_host import COPRA_Host
# from corpaoml_al_mp.COPRA_driver import COPRA_Driver
# from corpaoml_al_mp.COPRA_load_data import COPRA_Load_Data
# from corpaoml_al_mp.COPRA_coordinator import COPRA_Coordinator
from COPRA_driver import COPRA_Driver
from COPRA_load_data import COPRA_Load_Data
from COPRA_coordinator import COPRA_Coordinator
import time
# from collections import defaultdict
import networkx as nx
import onmi
import EQ


class Test():
    def test_intersect(datatype,seed_node,attribute,param,party,file_name,scale,k,mi):
        edge_path = []
        if datatype == 'artificial':
            for i in range(int(party)):   
                edge_path.append('../data/' + datatype + '/' + param + '/' + party + '/network'+ file_name +'_{}.txt'.format(i))
            feat_path = '../data/' + datatype + '/' + param + '/feat/network' + file_name +'_bd_feat.txt'
            # write_path = '../data/' + datatype + '/' + param + '/' + party + '/network' + file_name + '_' + party + '_re.txt'
            write_path = '../data/' + datatype + '/' + param + '/' + party + '/network' + file_name + '_' + party + '_re.txt'
            real_path = '../data/' + datatype + '/' + param + '/' + party + '/community' + file_name +'.txt'
        else:
            # for i in range(int(party)):   
            #     edge_path.append('../data/' + datatype + '/' + party + '/'+ file_name +'_{}.txt'.format(i))
            # feat_path = '../data/' + datatype + '/feat/' + file_name +'.feat'
            # write_path = '../data/' + datatype + '/' + party + '/' + file_name + '_' + party + '_re.txt'
            # real_path = '../data/' + datatype + '/' + party + '/' + file_name +'.circles'
            # graph_path = '../data/' + datatype + '/' + file_name + '.edges'
            for i in range(int(party)):   
                edge_path.append('../data/' + datatype + '/' + party + '/'+ file_name +'_{}.txt'.format(i))

            # ？？？
            # edge_path 原始图数据的存放位置
            #feat_path 属性的存放位置
            #real_path 存放答案的位置
            # feat_path = '../data/' + datatype + '/feat/' + file_name +'.txt'
            feat_path = '../data/' + datatype + '/feat/' + file_name +'.feat'
            # write_path = '../data/' + datatype + '/' + party + '/' + file_name + '_' + party + '_re.txt'
            # 怕重复写加个后缀
            write_path = '../data/' + datatype + '/' + party + '/' + file_name + '_' + party + '_re.txt'
            # real_path = '../data/' + datatype + '/' + party + '/' + file_name +'_com.txt'
            # 并没有xx.com.txt 只有.circles
            real_path = '../data/' + datatype + '/' + party + '/' + file_name +'.circles'
            # graph_path = '../data/' + datatype + '/' + file_name + '.txt'
            graph_path = '../data/' + datatype + '/' + file_name + '.edges'

        begin_time = time.perf_counter()
        G = []
        nodeset = []
        n = int(party) #party是2|4|8|10 这种
        Coordinator = COPRA_Coordinator()
        load_data = COPRA_Load_Data()
        for i in range(n):
            G.append(load_data.read_graph_from_file(edge_path[i],seed_node))
            nodeset.append(G[i].nodes()) #nodeset是所有多个网络里的所有节点 e.g. n=2 有两个网络
        sum1=0
        sum2=0
        for small_g in G:
            sum1+=small_g.number_of_edges()
            sum2+=small_g.number_of_nodes()


        if datatype == 'real':

            # 用于计算模块度
            Graph = load_data.read_graph_from_file(graph_path,seed_node)
        # Graph = load_data.read_graph_from_file(graph_path, seed_node)
        # print(G[0].nodes(1000))

        # 执行COPRA主要逻辑代码的地方

        #读取属性矩阵
        A = load_data.read_attr_from_file(feat_path)
        Driver = COPRA_Driver()
        # 2是什么
        communities= Driver.run(G, A, n, 2, attribute,scale,seed_node,k,mi)
        end_time = time.perf_counter()
        total_time = end_time - begin_time
        
        #输出结果
        Coordinator.print_communities_to_file(communities, write_path)

        # 验证计算onmi
        onmi_ = onmi.cale_onmi(real_path,write_path)
        if datatype == 'real':
            EQ_ = EQ.cal_EQ(communities,Graph)
            print('eq：',EQ_)
        else:
            EQ_ = 0
            # print('人工数据集算EQ')
            # graph_path = '../data/' + datatype + '/' + param +  '/network' + file_name+'.txt'
            # Graph = load_data.read_graph_from_file(graph_path, seed_node)
            # EQ_ = EQ.cal_EQ(communities,Graph)
            # print('eq=',EQ_)
        print('时间：',total_time)
        
        # host = COPRA_Host()
        #     G = nx.read_edgelist("../../corpa/genuine/karate.txt")
        #     com = host.load_data("../../corpa/genuine/copraoml_karate.txt")
        #     mod = host.cal_EQ(com, G)
            # if(mod>=0):
        #     s.append(mod)
        #     print(mod)
        # print("模块度是：",s)
        # print("平均模块度是：",sum(s) / len(s))
        return total_time,[onmi_,EQ_]


if __name__ == '__main__':
    datatype = 'real'
    seed_node = 'off'
    scale = 0.5
    k = 0.5
    mi = 5
    attribute = 'on'
    # attribute = 'off'
    param = 'n'
    party = '2'
    # party = "4"
    # party = "6"
    # party = "8"
    party = '10'
    # file_name = '1239671'
    # file_name = '2363991'
    # file_name = '5747502'
    file_name = '7682452'
    app=Test
    app.test_intersect(datatype, seed_node, attribute, param, party, file_name ,scale, k ,mi)
    
