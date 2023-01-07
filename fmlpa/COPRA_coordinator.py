# -*- coding: utf-8 -*-
# @Time    : 2019/11/12
# @Author  : yz
# @Version : 1.0

import collections
import random

import networkx as nx

from sad import SAD
from sm import SM
from smax import SMAX


# from intersect_mp.tools import IntersectTools


class Cnode(object):
    def __init__(self,label,value):
        self.label = label
        self.value = value

class COPRA_Coordinator(object):
    # 分组求和
    def __init__(self):
        self.map1=[]
        self.map2=collections.defaultdict(set)
        self.nodedegree=[]
        self.intersect_Hid = []
        
    def clear_data(self):
        self.map1=[]
        self.map2=collections.defaultdict(set)
        self.nodedegree=[]
        
    def receive_pk(self,public_key,private_key):
        self.public_key = public_key
        self.private_key = private_key
        
    def receive_nodedegree(self,degree):
        self.nodedegree.append(degree)
        
    def receive_intersect_Hid(self,intersect_Hid):
        self.intersect_Hid.append(intersect_Hid)
        
    def get_global_intersect_Hid(self):
        self.global_intersect_Hid = set()
        for i in range(len(self.intersect_Hid)):
            self.global_intersect_Hid = self.global_intersect_Hid | self.intersect_Hid[i]
    
    def hash_to_num(self,mi):
        length = len(self.intersect_Hid)+1
        self.mi = mi
        self.gap = int(((10**(mi+1)-1)-10**mi)/length)
        MIN = 10**mi
        MAX = MIN + self.gap
        self.hton = dict()
        ln = len(self.global_intersect_Hid)
        numlist = random.sample(range(MIN,MAX),ln)
        # print('g':len(self.global_intersect_Hid))
        for Hnode in self.global_intersect_Hid:
            num = random.choice(numlist)
            numlist.remove(num)
            self.hton[Hnode] = num
    
    def send_hton_to_hosts(self,hosts):
        for i in range(len(hosts)):
            MIN = 10**self.mi+(i+1)*self.gap
            MAX = 10**self.mi+(i+2)*self.gap
            hton = dict()
            for Hnode in self.global_intersect_Hid:
                if Hnode in self.intersect_Hid[i]:
                    hton[Hnode] = self.hton[Hnode]
            hosts[i].receive_hton(hton,MIN,MAX)
        
    def choose_seednodes(self,scale):
        nddict={}
        for nds in self.nodedegree:
            for nd in nds:
                if nd[0] in nddict.keys():
                    nddict[nd[0]]+=nd[1]
                else:
                    nddict[nd[0]] = nd[1]
        ndlist=sorted(nddict.items(),key=lambda x:x[1],reverse=True)
        num = round(len(ndlist)*scale)
        seednodes=[]
        for i in range(num):
            seednodes.append(ndlist[i][0])
        self.seednodes = seednodes
        
    def send_seednodes(self,i,host):
        nodelist =[]
        for nd in self.nodedegree[i]:
            nodelist.append(nd[0])
        seednodes = []
        for node in self.seednodes:
            if node in nodelist:
                seednodes.append(node)
        # print(self.nodedegree)
        host.receive_seednodes(seednodes)

    def get_intersect_data_com(self,hosts):
        '''
        取全局重叠结点的邻接表
        '''
        n=len(hosts)
        for i in range(n):
            for j in range(n-1):
                keys1=[key1 for key1, item1 in self.map1]
                for key2, item2 in hosts[i].intersect_host_data[j]:
                    self.map2['{}'.format(i)].add(key2)
                    if key2 in keys1:
                        A = self.map1[keys1.index(key2)][1]
                        B = item2
                        C = {}
                        for key in list(set(A) | set(B)):
                            # print(A.get(key),B.get(key))
                            if A.get(key) and B.get(key):
                                # C.update({key: A.get(key) + B.get(key)})
                                # C.update({key:self.private_key.decrypt(self.ADD(A.get(key),B.get(key)))})
                                C.update({key:self.ADD(A.get(key),B.get(key))})
                            else:
                                # C.update({key:self.private_key.decrypt( A.get(key) or B.get(key))})
                                C.update({key: A.get(key) or B.get(key)})
                                # if (A.get(key) or B.get(key)) == None:
                                #     C.update({key:0})
                                # else:
                                #     C.update({key: A.get(key) or B.get(key)})
                        self.map1[keys1.index(key2)]=[key2,C]
                    else:
                        self.map1.append([key2,item2])
        self.map1 = sorted(self.map1,key = lambda x:x[0])
        
    def findSMAX(self,l,r):
        mid = (l+r)//2
        if l>r:
            return
        if l == r:
            return list1[l]
        if(r-l <= 1):
            SK111 = SMAX(list1[l],list1[r],self.public_key)
            SK111.StepOne()
            SK111.StepTwo()
            SK111.StepThree()
            return SK111.FINMX
        ls = self.findSMAX(l, mid)
        rs = self.findSMAX(mid + 1, r)
        SK112 = SMAX(ls, rs, self.public_key)
        SK112.StepOne()
        SK112.StepTwo()
        SK112.StepThree()
        return SK112.FINMX

    def COMPARE(self,init_list):
        if len(init_list) == 1:
            return init_list[0]
        else:
            # E1 = init_list[0].value
            # E2 = init_list[1].value
            # SK11 = SMAX(E1, E2, self.public_key)
            # SK11.StepOne()
            # SK11.StepTwo()
            # SK11.StepThree()
            # re1 = self.private_key.decrypt(SK11.FINMX)
            # # print(re)
            # if re1 == self.private_key.decrypt(E1):
            #     return init_list[0]
            # elif re1 == self.private_key.decrypt(E2):
            #     return init_list[1]
            
            E11 = self.private_key.decrypt(init_list[0].value)
            E22 = self.private_key.decrypt(init_list[1].value)
            re2 = max(E11,E22)
            if re2 == E11:
                return init_list[0]
            elif re2 == E22:
                return init_list[1]
            
            # re = max(init_list[0].value,init_list[1].value)
            # if re == init_list[0].value:
            #     return init_list[0]
            # elif re == init_list[1].value:
            #     return init_list[1]
            
    # def get_max(self,init_list):
    #     '''
    #     logn复杂度取最大值
    #     '''
    #     if len(init_list) <= 2:
    #         return self.COMPARE(init_list)
    #     else:
    #         init_list=[init_list[i:i+2] for i in range(0,len(init_list),2)]
    #         max_init_list = []
    #         for _list in init_list:
    #             # print(_list)
    #             max_init_list.append(self.COMPARE(_list))
    #         s = self.get_max(max_init_list)
    #     return s
    
    def get_max(self,init_list):
        l = 0
        r = len(init_list)-1
        global list1
        list1 = []
        list2 = []
        for Cnode in init_list:
            list1.append(Cnode.value)
            list2.append(self.private_key.decrypt(Cnode.value))
        # re = self.private_key.decrypt(self.findSMAX(l,r))
        for i in range(len(list2)):
            # if re == list2[i]:
            #     return init_list[i]
            if max(list2) == list2[i]:
                return init_list[i]
    
    def ADD(self,E1,E2):
        SK17 = SAD(E1, E2, self.public_key)
        SK17.StepOne()
        SK17.StepTwo()
        SK17.StepThree()
        return SK17.FIN
    
    def MU(self,E1,num):
        SK18 = SM(E1, num, self.public_key)
        SK18.StepOne()
        return SK18.FIN
    
    def get_label(self):
        '''
        返回1个权重最大的标签
        '''
        self.node_label = dict()
        for node,item in self.map1:
            classlw = []
            for label in item.keys():
                # print(item[label])
                classlw.append(Cnode(label,item[label]))
            re = self.get_max(classlw)
            self.node_label[node] = [re.label]
            
    def get_labels(self,v,hosts):
        '''
        返回v个权重最大的标签
        {node:[Cnode1,Cnode2...]...}
        '''
        self.node_label = dict()
        for node,item in self.map1:
            #选择V个Cnode
            classlw = []
            for label in item.keys():
                classlw.append(Cnode(label,item[label]))
            result = []
            for i in range(v+1):
                re = self.get_max(classlw)
                # print('第%d次%s'%(i,type(re)))
                result.append(re)
                if re in classlw:
                    classlw.remove(re)
                    # i=i-1
            # hq:23开头的twitter会报错 ：https://blog.csdn.net/qq_41173604/article/details/105481945?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.nonecase
            # 因为non_type的元素不会出现在classlw中，所以会报错！
            # print('result的长度%d'%(len(result)))

            #根据COPRA规则选择最终标签
            for i in range(len(self.map2)):
                if node in self.map2['{}'.format(i)]:
                    # print("传进来之前是什么type")
                    # print(type(result[0]))
                    # print(type(result[v-1]))
                    # print(type(result[v]))
                    if hosts[i].judge_labels(result[0],result[v-1],result[v]):
                        labels = []
                        for i in range(len(result)):
                            labels.append(result[i].label)
                        self.node_label[node] = labels
                    else:
                        self.node_label[node] = [result[0].label]
                    break
    # def send_intersect_data_com(self,i,host):
    #     keys=[keys for keys, items in self.map1]
    #     for num in self.map2['{}'.format(i)]:
    #         nodeitem=self.map1[keys.index(num)]
    #         host.receive_intersect_data_com(nodeitem)
            
    def send_nodelabelpair(self,i,hosts):
        '''
        Returns
        -------
        每个参与方重叠结点标签的更新方案

        '''
        for node in self.map2['{}'.format(i)]:
            nlpair = [node,self.node_label[node]]
            hosts.receive_nodelabelpair(nlpair)
            # print(nlpair)
        
#     def send_intersect_data(self,intersect_guest_data, intersect_host_data):
#         '''
#                 :param intersect_guest_data:{(vi,{(H(lij), E(nlij))})|vi∈XA ∩XB
#                 :param intersect_host_data: {(vi,{(H(lij), E(nlij))})|vi∈XA ∩XB
#                 :return: {(vi,{(H(lij), ∑E(nlij))})| (H(lij), E(nlij))∈YA∪YB}
#                 '''
#         keys1 = [key1 for key1, item1 in intersect_guest_data]
#         intersect_data = []
#         for key2, item2 in intersect_host_data:
#             if key2 in keys1:
#                 A = intersect_guest_data[keys1.index(key2)][1]
#                 B = item2
#                 C = {}
#                 for key in list(set(A) | set(B)):
#                     if A.get(key) and B.get(key):
#                         C.update({key: A.get(key) + B.get(key)})
#                     else:
#                         C.update({key: A.get(key) or B.get(key)})
#                 intersect_data.append([key2, C])
# #        print("send YC to A")
# #        print("send YC to B")
#         # print("c:",intersect_data)
# #        print('guest:',len(intersect_guest_data))
# #        print('host:',len(intersect_host_data))
# #        print('intersect:',len(intersect_data))
#         return intersect_data
    
    def merge_graph(self,G):
        graph = nx.Graph()
        for i in range(len(G)):
            for j ,data in G[i].nodes(data=True):
                # print(graph.nodes())
                # print(j,data)
                if j not in graph.nodes():
                    graph.add_node(j,label = data['label'])
        return graph
    
    def get_communities(self, graph):
        '''
        生成社区。
        :param graph: 内部图对象。
        :return: {社区标签，社区节点集}字典。
        '''
        # print('Getting communities...')
        com_dict = dict()
        for j in range(len(graph)):
            for i, data in graph[j].nodes(data=True):
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
    
#     def get_communities(self, datasets):
#         ids = []
#         communities = collections.defaultdict(lambda: list())
#         for G in datasets:
#             for node in G.nodes(True):
#                 label = node[1]["label"]
#                 for i in label.keys():
#                     communities[i].append(node[0])
#         for i in communities.values():
#             id = list(set(i))
#             ids.append(id)
# #        print('communities.values()',communities.values())
#         print('ids:',ids)
#         return ids

    def print_communities_to_file(self, communities, output_path):
        output_file = open(output_path, 'w')
        for cmu in communities:
            for member in cmu:
                output_file.write(member + " ")
            output_file.write("\n")
        output_file.close()
        return

    def get_intersect_idx(self,intersect_idx_raw):
        n=len(intersect_idx_raw)
        A=set(intersect_idx_raw[n-1])
        for i in range(n-1):
            A=A | set(intersect_idx_raw[i])
        return A
                
    def get_processed_data(self,hosts,i):
        n=len(hosts)
        # print('n',n)
        intersect_guest_data=[]
        # print('i:',i)
        for k in range(i):
            intersect_guest_data.append(hosts[k].intersect_host_data[i-1])
            # print('k1:',k)
        for k in range(i+1,n):
            # print('k2:',k)
            # if k is not None:
            intersect_guest_data.append(hosts[k].intersect_host_data[i])
        return intersect_guest_data