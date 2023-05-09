# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:34:19 2020

@author: yz
"""

import networkx as nx
import numpy as np
from collections import defaultdict
import hashlib
import onmi
import time
import xlsxwriter
import random

class COPRA_isolate:
    def hash(self,value):
        return hashlib.sha3_256(bytes(str(value), encoding='utf-8')).hexdigest()
    
    def read_graph(self,seed_node,scale,edgelist_file,attribute,attr_file):
        graph = nx.read_edgelist(edgelist_file)
        if seed_node == 'on':
            nd = list(graph.degree())
            ndlist=sorted(nd,key=lambda x:x[1],reverse=True)
            num = round(len(ndlist)*scale)
            seed = []
            for i in range(num):
                seed.append(ndlist[i][0])
            for node, data in graph.nodes(True):
                #赋予种子节点标签
                if node in seed:
                    dict = defaultdict(float)
                    dict[self.hash(node)] = 1
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
                    dict[self.hash(seed_choice)] = 1
                    data['label'] = dict
        else:
            for node, data in graph.nodes(True):
                dict = defaultdict(float)
                dict[self.hash(node)] = 1
                data['label'] = dict
        if attribute == 'on':
            data = np.loadtxt(attr_file,str, delimiter=' ')
            A={}
            for attr in data:
                A.update({attr[0]:attr[1:len(attr)]})
            for node in graph:
                graph.nodes[node]['attr'] = A[node]           
        return graph
    
    # def cale_attr_similarity(self,vi,vj,graph):
    #     vi = graph.nodes[vi]["attr"]
    #     vj = graph.nodes[vj]["attr"]
    #     Sa = 1.0 * (np.sum(vi == vj) / len(vi))
    #     return round(Sa,6)
    
    def cale_attr_similarity(self,vi,vj,graph):
        vi = graph.nodes[vi]["attr"]
        vj = graph.nodes[vj]["attr"]
        #Hamming Distance
        Sa = 1.0 * (np.sum(vi == vj) / len(vi))
            
        # # Jaccard
        # l1 = np.sum(vi + vj == 2)
        # l2 = min(np.sum(vi == 1),np.sum(vj == 1))
        # Sa = max(1.0 * l1 / l2, 0.000001)
        # Sa = 1.0 * l1 / l2
        
        # # Euclidean Distance
        # Sa = np.sqrt(np.sum(np.square(vi-vj)))
        
        # #Cosine Similarity
        # Sa = np.dot(vi,vj)/(np.linalg.norm(vi)*np.linalg.norm(vj))
        
        # #Jaccard Similarity
        # up=np.double(np.bitwise_and((vi != vj),np.bitwise_or(vi != 0, vj != 0)).sum())
        # down=np.double(np.bitwise_or(vi != 0, vj != 0).sum())
        # Sa=(up/down)
        
        return round(Sa,6)

    
    def cale_weight(self,graph,attribute,iteration):
        G=[]
        for node in graph:
            data = []
            dict = {}
            data.append(node)
            for neighbor_index in graph.neighbors(node):
                if attribute == 'on':
                    Sa = self.cale_attr_similarity(node,neighbor_index,graph)
                neighbor_label = graph.nodes[neighbor_index]["label"]
                # test
                # if iteration == 7:
                #     print(neighbor_label,'done')
                for k in neighbor_label.keys():
                    if attribute == 'on':
                        # print(neighbor_label.get(k),Sa)
                        value = round(neighbor_label.get(k),6)*Sa #Saij*nlij
                    else:
                        value = neighbor_label.get(k)
                    # print(value)
                    dict[k] = dict.setdefault(k, 0) + round(value,6)
            data.append(dict)
            G.append(data)
        return G
    
    def normalize(self,data):
        for i in range(len(data)):
            
            # if data[i][0] == '776':
            #     print(data[i][1].items())
            
            sum=0
            for x, y in list(data[i][1].items()):
                sum+=y
            # print(sum)
            for x, y in list(data[i][1].items()):
                data[i][1].update({x: round(y/sum,6)})
        # print(data)
        return data
    
    def label_propagate(self,graph,G,v,iteration):
        # g = graph
        Graph= self.normalize(G)
        # print(Graph)
        for i in range(len(Graph)):
            # #test
            # if (Graph[i][0] == '421') & (iteration == 13):
            #     print(Graph[i][1].keys())
            #     print(Graph[i][1].values())

            sum1 = 0
            maxc = max(Graph[i][1].values())
            a = [item[0] for item in Graph[i][1].items() if abs(item[1]-maxc) <= 0.000005]
            
            # if Graph[i][0] == '776':
            #     print(Graph[i][1].values())
        
            if maxc < 1 / float(v):
                Graph[i][1].clear()
                # m = random.choice(a) #随机性
                m = max(a)
                Graph[i][1][m] = 1
            else:
                for x, y in list(Graph[i][1].items()):
                    if y < 1 / float(v):
                        Graph[i][1].pop(x)
                        sum1 += y
                for x, y in list(Graph[i][1].items()):
                    Graph[i][1].update({x: round(y / (1-sum1),6)})
            # 更新标签
            graph.nodes[Graph[i][0]]["label"] = Graph[i][1]
            # if g == graph:
            #     print("error!!!!!!!!!!!!!!!!!!!!!!!!")
        return graph
            
#     def get_communities(self,G):
#         ids = []
#         communities = collections.defaultdict(lambda: list())
#         for node in G.nodes(True):
#             label = node[1]["label"]
#             for i in label.keys():
#                 communities[i].append(node[0])
#         for i in communities.values():
#             id = list(set(i))
#             ids.append(id)
# #        print('communities.values()',communities.values())
#         print('ids:',ids)
#         return ids
    
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
    
    def determine_final_communities(self, graph):
        '''
        清除嵌入在其它社区中的社区，将无社区节点归到同一个社区，将同一个社区中的非连通分支分割为独立社区，以得到最终用于输出的社区集。
        :param graph: 内部图对象。
        :return: {社区标签，社区节点集}字典。
        '''
        print('Determining final communities...')
        coms = dict()
        subs = dict()
        orphans = set()
        nolabels = 0
        for i, data in graph.nodes(data=True):
            labels = data['label']
            # 将没有标签的节点归到同一个社区。
            if not labels:
                nolabels += 1
                orphans.add(i)
            else:
                # 计算社区包含的节点，以及社区之间的包含关系。
                for label in labels.keys():
                    if label in coms.keys() and label in subs.keys():
                        coms[label].add(i)
                        subs[label] &= labels.keys()
                    else:
                        coms[label] = {i}
                        subs[label] = set(labels.keys())
        subsetc = 0
        # 删除包含在其它社区内部的社区，以及完全相等的社区。
        del_com = list()
        for lab in subs.keys():
            if len(subs[lab]) > 1:
                del_com.append(lab)
                for parent in subs[lab]:
                    # 如果父社区集包含除了自身之外的其它社区，则从父社区的父社区集中删除自身（如果有的话），以处理社区完全相等的情况。
                    if parent != lab:
                        if lab in subs[parent]:
                            subs[parent].remove(lab)
                subs[lab].remove(lab)
        for com in del_com:
            coms.pop(com)
        # 将无标签节点归到同一个社区。
        if len(orphans) > 0:
            coms['nolabel'] = orphans
        for c in coms.keys():
            if len(coms[c]) == 0:
                print('Community ', c, ' is empty.')
        # 将同一个社区中的非连通分支分割为独立社区。
        # for com in coms.values():
        #     s = com.copy()
        #     while len(s) > 0:
        #         ls = list(s)
        #         q = queue.Queue()
        #         visited = set()
        #         q.put(ls[0])
        #         visited.add(ls[0])
        #         con_com = set()
        #         while not q.empty():
        #             i = q.get()
        #             con_com.add(i)
        #             nbs = (set(graph[i]) - visited) & com
        #             for nb in nbs:
        #                 q.put(nb)
        #                 visited.add(nb)
        #         s -= con_com
        #         if len(s) > 0:
        #             print('Disconnected community found!')
        print('[DEBUG]', nolabels, ' vertices have no labels. ', len(del_com),
              ' communities are subsets of or equal to others.')
        return coms
    
    def communities_changed(self, cur_com_dict, min_com_dict):
        '''
        判断当前轮迭代生成的社区大小相对于之前迭代生成的最小社区大小是否有变化。若有变化，则需要更新最小社区大小。
        :param cur_com_dict: 当前轮迭代生成的{社区标签,社区大小}字典。
        :param min_com_dict: 之前迭代生成的{社区标签,社区大小最小值}字典。
        :return: 若有变化则True，否则返回False。
        '''
        if min_com_dict is None:
            return True
        if len(cur_com_dict) != len(min_com_dict):
            return True
        changed = False
        for label in cur_com_dict.keys():
            if label not in min_com_dict.keys():
                return True
            if cur_com_dict[label] < min_com_dict[label]:
                changed = True
            else:
                cur_com_dict[label] = min_com_dict[label]
        return changed
    
    def run(self,seed_node,scale,edgelist_file,attribute,attr_file,v):

        graph = self.read_graph(seed_node,scale,edgelist_file, attribute, attr_file)
        iteration=0
        min_com_dict = None
        cur_com_dict = None
        G = graph
        while True:
            iteration+=1
            G = self.cale_weight(G, attribute,iteration)
            # print(G)
            G = self.label_propagate(graph,G, v,iteration)
            
            cur_com_dict = self.get_communities(G)
            # 将字典的value改为社区大小。
            for com in cur_com_dict.keys():
                cur_com_dict[com] = len(cur_com_dict[com])
            # print('[DEBUG]', 'cur_com_dict com idx: ', cur_com_dict.keys())
            # print('[DEBUG]', 'last_com_dict com idx: ', last_com_dict.keys() if last_com_dict is not None else '')
            # print(self.communities_changed(cur_com_dict, min_com_dict))
            if (not self.communities_changed(cur_com_dict, min_com_dict) or iteration > 30):
                break
            min_com_dict = cur_com_dict
            
            # # test
            # write_path = r'C:\Users\asus\Desktop\COPRA\testdata\iso\iter_{}.txt'.format(iteration)
            # coms = self.determine_final_communities(G)
            # key = list(coms.keys())
            # data = list(coms.values())
            # for i in range(len(key)):
            #     data[i].add(key[i])
            #     data[i] = sorted(list(data[i]),reverse=True)
            # self.print_communities_to_file(data, write_path)
            
        coms = self.determine_final_communities(G)
        return coms.values()
    
    def print_communities_to_file(self, communities, output_path):
        output_file = open(output_path, 'w')
        for cmu in communities:
            for member in cmu:
                output_file.write(member + " ")
            output_file.write("\n")
        output_file.close()
        return
    
    def Test(self,seed_node,scale,datatype, attribute,param,file_name,real_path):
        v = 2
        # 人工数据集
        file_path = '../data/' + datatype + '/' + param + '/network' + file_name + '.txt'
        attr_path = '../data/' + datatype + '/' + param + '/feat/network' + file_name + '_bd_feat.txt'
        write_path = '../data/' + datatype + '/' + param + '/network' + file_name + '_hqq0102_re.txt'

        # file_path = '../data/' + datatype + '/' + file_name + '.edges'
        # attr_path = '../data/' + datatype + '/feat/' + file_name + '.feat'
        # write_path = '../data/' + datatype + '/' + file_name + '_re_hqq_1226.txt'

        # 真实数据集
        # file_path = '../data/' + datatype + '/' + file_name + '.edges'
        # attr_path = '../data/' + datatype + '/feat/' + file_name + '.feat'
        # write_path = '../data/' + datatype + '/' + file_name + '_re_hqq_0102_isolate_copra.txt'
        
        begin_time = time.perf_counter()
        communities = self.run(seed_node,scale,file_path, attribute, attr_path, v)
        print('copra里面的community长什么样子')
        # print(communities)
        end_time = time.perf_counter()
        total_time = end_time - begin_time
        print(total_time)
        
        app.print_communities_to_file(communities,write_path)
        
        #计算模块度或精确度
        if datatype == 'real':
            # real_path = 'data/' + datatype + '/' + file_name + '_com.txt'
            graph = nx.read_edgelist(file_path)
            print(communities)
            re = [self.cal_EQ(communities, graph), onmi.cale_onmi(real_path,write_path)]
            print(self.cal_EQ(communities, graph))
        else:
            graph = nx.read_edgelist(file_path)
            print(communities)
            re = [self.cal_EQ(communities, graph), onmi.cale_onmi(real_path,write_path)]
            print(self.cal_EQ(communities, graph))
        return total_time, re

    def execute(self, G):
        # 最终目标拿到community
        attribute = 'on'
        v = 2
        iteration = 0
        min_com_dict = None
        cur_com_dict = None
        # G = graph
        graph=G
        while True:
            iteration += 1
            G = self.cale_weight(G, attribute, iteration)
            G = self.label_propagate(graph, G, v, iteration)

            cur_com_dict = self.get_communities(G)
            # 将字典的value改为社区大小。
            for com in cur_com_dict.keys():
                cur_com_dict[com] = len(cur_com_dict[com])

            if (not self.communities_changed(cur_com_dict, min_com_dict) or iteration > 30):
                break
            min_com_dict = cur_com_dict



        coms = self.determine_final_communities(G)
        return coms.values()


        
if __name__ == '__main__':
    app = COPRA_isolate()
    attrs = ['off']
    seed_node ='off'
    scale = 0.1
    # datatype = 'real'
    datatype = 'artificial'

    # file_names =  ['1239671' ,'2363991','5747502','7682452']
    # file_names =  ['7682452']
    # file_names = ['0.1' ,'0.2','0.3','0.4','0.5','0.6','0.7']
    # file_names = ['1k', '2k', '3k', '4k', '5k']
    # file_names = ['1', '2', '3', '4', '5']
    file_names = ['10k']
    # , '200', '300', '400', '500']
    # file_names = ['park']
    
    # params = ['mu','n','om','on']
    # params = ['alone_mu0.1', 'alone_mu0.2', 'alone_mu0.3', 'alone_mu0.4', 'alone_mu0.5']
    params = ['2222-3434', '3221-5342', '4211-3211', '5111-7222']
    # file_names = [
        # ['5']
                      # ['0.1','0.2','0.3','0.4','0.5','0.6','0.7'],
                      # ['1k','2k','3k','4k','5k'],
                      # ['1','2','3','4','5'],
                      # ['100','200','300','400','500']
                    # ]
    time_list = []
    onmi_list = []
    EQ_list = []
    times_list = []
    if datatype == 'artificial':
        for attr in attrs:
            i = 0
            for param in params:
                for file_name in file_names:
                    print('running 人工',param ,file_name,'...')
                    real_path = '../data/' + datatype + '/' + param + '/community' + file_name + '.txt'
                    time_,re = app.Test(seed_node,scale,datatype, attr, param, file_name,real_path)
                    time_list.append(time_)
                    onmi_list.append(re[1])
                    EQ_list.append(re[0])
                i = i + 1
        workbook = xlsxwriter.Workbook(params[0]+'_copra_isolate_artificial.xlsx')
        worksheet = workbook.add_worksheet('data')
        for i in range(len(file_names)):
            worksheet.write(i,1,param[0]+'_'+file_names[i])
            worksheet.write(i,2,EQ_list[i])
            worksheet.write(i,3,onmi_list[i])
        workbook.close()
                
    else:
        for attr in attrs:
            for file_name in file_names:
                start = time.time()
                print('running',file_name,'...')
                real_path = '../data/' + datatype + '/' + file_name + '.circles'
                time_,re = app.Test(seed_node,scale,datatype, attr, None, file_name,real_path)
                time_list.append(time_)
                # EQ_list.append(re)
                EQ_list.append(re[0])
                onmi_list.append(re[1])
                end = time.time()
                # times_list.append(end-start)
    print(time_list)
    print(EQ_list)
    print(onmi_list)
        # workbook = xlsxwriter.Workbook('copra_isolate_as.xlsx')
        # worksheet = workbook.add_worksheet('data')
        # for i in range(len(file_names)):
        #     worksheet.write(i, 1, file_names[i])
        #     worksheet.write(i, 2, EQ_list[i])
        #     worksheet.write(i, 3, onmi_list[i])
        # workbook.close()
            
    
    
    
    
    
    
    
    
    
    
    
    