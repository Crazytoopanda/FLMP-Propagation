"""
COPRA_Reviewer联邦化协调方

@author: Lfa
update: 2022/9/22
"""

import collections
import random
import networkx as nx
from sad import SAD
from sm import SM
from smax import SMAX

class Cnode(object):
    def __init__(self,label,value):
        self.label = label
        self.value = value

class COPRA_Coordinator(object):

    def __init__(self):
        self.map1 = []
        self.map2 = collections.defaultdict(set)
        self.nodedegree = []
        self.intersect_Hid = []

    def clear_data(self):
        self.map1 = []
        self.map2 = collections.defaultdict(set)
        self.nodedegree = []

    def receive_key(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def receive_nodedegree(self,degree):
        self.nodedegree.append(degree)

    def receive_intersect_Hid(self, intersect_Hid):
        self.intersect_Hid.append(intersect_Hid)

    def get_global_intersect_Hid(self):
        self.global_intersect_Hid = set()
        for i in range(len(self.intersect_Hid)):
            self.global_intersect_Hid = self.global_intersect_Hid \
                                        | self.intersect_Hid[i]

    def hash_to_num(self, mi):
        length = len(self.intersect_Hid) + 1
        self.mi = mi
        self.gap = int(((10 ** (mi + 1) - 1) - 10 ** mi) / length)
        MIN = 10 ** mi
        MAX = MIN + self.gap
        self.hton = dict()
        ln = len(self.global_intersect_Hid)
        numlist = random.sample(range(MIN, MAX), ln)
        # print('g':len(self.global_intersect_Hid))
        for Hnode in self.global_intersect_Hid:
            num = random.choice(numlist)
            numlist.remove(num)
            self.hton[Hnode] = num

    def send_hton_to_hosts(self, hosts):
        for i in range(len(hosts)):
            MIN = 10 ** self.mi + (i + 1) * self.gap
            MAX = 10 ** self.mi + (i + 2) * self.gap
            hton = dict()
            for Hnode in self.global_intersect_Hid:
                if Hnode in self.intersect_Hid[i]:
                    hton[Hnode] = self.hton[Hnode]
            hosts[i].receive_hton(hton, MIN, MAX)

    def choose_seednodes(self, scale):
        nddict = {}
        for nds in self.nodedegree:
            for nd in nds:
                if nd[0] in nddict.keys():
                    nddict[nd[0]] += nd[1]
                else:
                    nddict[nd[0]] = nd[1]
        ndlist = sorted(nddict.items(), key=lambda x: x[1],
                        reverse=True)
        num = round(len(ndlist) * scale)
        seednodes = []
        for i in range(num):
            seednodes.append(ndlist[i][0])
        self.seednodes = seednodes

    def send_seednodes(self, i, host):
        nodelist = []
        for nd in self.nodedegree[i]:
            nodelist.append(nd[0])
        seednodes = []
        for node in self.seednodes:
            if node in nodelist:
                seednodes.append(node)
        host.receive_seednodes(seednodes)

    def get_intersect_data_communities(self, hosts):
        """
        : 取得全局重叠节点的邻接表

        :param hosts: 多组参与方
        :return:
        """
        n = len(hosts)
        for i in range(n):
            for j in range(n - 1):
                keys1 = [key1 for key1, item1 in self.map1]
                for key2, item2 in hosts[i].intersect_host_data[j]:
                    self.map2['{}'.format(i)].add(key2)
                    if key2 in keys1:
                        A = self.map1[keys1.index(key2)][1]
                        B = item2
                        C = {}
                        for key in list(set(A) | set(B)):
                            if A.get(key) and B.get(key):
                                C.update({key: self.ADD(A.get(key), B.get(key))})
                            else:
                                C.update({key: A.get(key) or B.get(key)})
                        self.map1[keys1.index(key2)] = [key2, C]
                    else:
                        self.map1.append([key2, item2])
        self.map1 = sorted(self.map1, key=lambda x: x[0])

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

    def COMPARE(self, init_list):
        if len(init_list) == 1:
            return init_list[0]
        else:
            E11 = self.private_key.decrypt(init_list[0].value)
            E22 = self.private_key.decrypt(init_list[1].value)
            re2 = max(E11, E22)
            if re2 == E11:
                return init_list[0]
            elif re2 == E22:
                return init_list[1]

    def ADD(self, E1, E2):
        SK17 = SAD(E1, E2, self.public_key)
        SK17.StepOne()
        SK17.StepTwo()
        SK17.StepThree()
        return SK17.FIN

    def MU(self, E1, num):
        SK18 = SM(E1, num, self.public_key)
        SK18.StepOne()
        return SK18.FIN

    def get_label(self):
        '''
        返回1个权重最大的标签
        '''
        self.node_label = dict()
        for node, item in self.map1:
            classlw = []
            for label in item.keys():
                # print(item[label])
                classlw.append(Cnode(label, item[label]))
            re = self.get_max(classlw)
            self.node_label[node] = [re.label]

    def get_labels(self, v, hosts):
        '''
        返回v个权重最大的标签
        {node:[Cnode1,Cnode2...]...}
        '''
        self.node_label = dict()
        for node, item in self.map1:
            # 选择V个Cnode
            classlw = []
            for label in item.keys():
                classlw.append(Cnode(label, item[label]))
            result = []
            for i in range(v + 1):
                re = self.get_max(classlw)
                # print('第%d次%s'%(i,type(re)))
                result.append(re)
                if re in classlw:
                    classlw.remove(re)
            for i in range(len(self.map2)):
                if node in self.map2['{}'.format(i)]:
                    if hosts[i].judge_labels(result[0], result[v - 1], result[v]):
                        labels = []
                        for i in range(len(result)):
                            labels.append(result[i].label)
                        self.node_label[node] = labels
                    else:
                        self.node_label[node] = [result[0].label]
                    break

    def send_nodelabelpair(self,i,hosts):
        '''
        Returns
        -------
        每个参与方重叠结点标签的更新方案

        '''
        for node in self.map2['{}'.format(i)]:
            nlpair = [node,self.node_label[node]]
            hosts.receive_nodelabelpair(nlpair)

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
        print("此时社区数量:", str(len(com_dict)))
        return com_dict

    def determine_final_communities(self, graph):
        '''
        清除嵌入在其它社区中的社区，将无社区节点归到同一个社区，将同一个社区中的非连通分支分割为独立社区，以得到最终用于输出的社区集。
        :param graph: 内部图对象。
        :return: {社区标签，社区节点集}字典。
        '''
        print('寻找无社区节点...')
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
                print('社区', c, '空了')
        print('DEBUG:', nolabels, '节点集没有标签，', len(del_com),
              ' 社区是其他社区的子集或等于其他社区')
        return coms

    def communities_changed(self, communities, min_communities) :
        if min_communities is None:
            return True
        else :
            for community, value in communities.items() :
                if community not in min_communities :
                    return True
                else :
                    if not not (min_communities[community] - value) :
                        return True
            return False

    def print_communities_to_file(self, communities, output_path):
        output_file = open(output_path, 'w')
        for cmu in communities:
            for member in cmu:
                output_file.write(member + " ")
            output_file.write("\n")
        output_file.close()
        return

    def get_intersect_idx(self, intersect_idx_raw):
        n = len(intersect_idx_raw)
        A = set(intersect_idx_raw[n - 1])
        for i in range(n - 1):
            A = A | set(intersect_idx_raw[i])
        return A

    def get_processed_data(self, hosts, i):
        n = len(hosts)
        # print('n',n)
        intersect_guest_data = []
        # print('i:',i)
        for k in range(i):
            intersect_guest_data.append(hosts[k].intersect_host_data[i - 1])
            # print('k1:',k)
        for k in range(i + 1, n):
            # print('k2:',k)
            # if k is not None:
            intersect_guest_data.append(hosts[k].intersect_host_data[i])
        return intersect_guest_data