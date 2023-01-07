# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 14:13
# @Author  : wmy
import hashlib
import math

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from scipy.stats import cosine

from utils.onmi import onmi
from utils.overlapping_modularity import cal_EQ

"""
工具类
"""


def hash(node):
    """
    对值进行hash散列
    :param node:
    :return: node的hash散列值
    """
    return hashlib.sha3_256(bytes(str(node), encoding='utf-8')).hexdigest()


def find_maximal_cliques(G):
    """
    计算G的极大团
    :param G:
    :return:maximal cliques
    """
    if len(G) == 0:
        return

    adj = {u: {v for v in G[u] if v != u} for u in G}
    Q = [None]

    subg = set(G)
    cand = set(G)

    u = max(subg, key=lambda u: len(cand & adj[u]))  # 找度最大的点
    ext_u = cand - adj[u]  # 可扩展点集

    stack = []

    try:
        while True:
            if ext_u:
                q = ext_u.pop()
                cand.remove(q)
                Q[-1] = q
                adj_q = adj[q]
                subg_q = subg & adj_q
                if not subg_q:  # 如果subg_q为空
                    yield Q[:]
                else:
                    cand_q = cand & adj_q
                    if cand_q:
                        stack.append((subg, cand, ext_u))
                        Q.append(None)
                        subg = subg_q
                        cand = cand_q
                        u = max(subg, key=lambda u: len(cand & adj[u]))
                        ext_u = cand - adj[u]
            else:
                Q.pop()
                subg, cand, ext_u = stack.pop()
    except IndexError:
        pass


def jaccard_sim(set1, set2):
    """
    计算jaccard相似度
    参考文献：P. Jaccard, “Etude de la distribution florale dans une portion des Alpes
            et du Jura,” Bull. del la Socit Vaudoise des Sci. Naturelles, vol. 37,
            no. 1901, pp. 547–579, 1901.
    :param set1:
    :param set2:
    :return:
    """
    inte_n = set(set1).intersection(set2)
    unin_n = set(set1).union(set2)
    js = 0
    if len(unin_n) > 0:
        js = len(inte_n) / len(unin_n)
    return js


def salton_index(set1, set2):
    """
    计算salton索引
    参考文献：G. Salton and M. J. McGill, Introduction to Modern Information
            Retrieval. New York, NY, USA: McGraw-Hill, 1986.
    :param set1:
    :param set2:
    :return:
    """
    inte_n = len(set(set1).intersection(set2))
    si = inte_n / (math.sqrt(len(set1) * len(set2)))
    return si


def hamming_distance(vec1, vec2):
    """
    使用汉明距离计算两个向量的相似度
    :param vec1:
    :param vec2:
    :return:
    """
    hd = 0
    for i in range(len(vec1)):
        if vec1[i] == vec2[i]:
            hd += 1
    hd = hd / len(vec1)
    hd = round(hd, 8)  # Eight decimal places
    return hd


def cos_sim(vec1, vec2):
    """
    计算余弦相似度
    :param vec1:
    :param vec2:
    :return:
    """
    cs = cosine(vec1, vec2)
    return cs


def read_comms(comms_path):
    """
    读取真实社区
    :param comms_path:
    :return:comms:一行代表一个社区
    """
    comms = []
    with open(comms_path, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n').strip()
            arr = line.split()
            arr = set(map(int, arr))
            comms.append(arr)
    return comms


def read_features(feat_path):
    """
    读取节点属性向量
    :return:feat_dict:字典形式返回
    """
    feat_dict = dict()
    with open(feat_path, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n').strip()
            arr = line.split()
            arr = list(map(int, arr))
            node = arr[0]
            vec = arr[1:]
            feat_dict[node] = vec
    return feat_dict


def calc_ONMI(real_comms, pred_comms):
    """
    计算 ONMI
    :param real_comms:
    :param pred_comms:
    :return:
    """
    return onmi(real_comms, pred_comms)


def calc_EQ(edge_path, comms):
    """
    计算 EQ
    :param edge_path:
    :param comms:
    :return:
    """
    g = nx.read_edgelist(edge_path)  # g 节点类型:str
    for idx, comm in enumerate(comms):
        comm = [str(node) for node in comm]  # 社区节点类型:int ->str
        comms[idx] = comm
    return cal_EQ(comms, g)


def draw(g):
    """
    画图
    :param g:
    """
    nx.draw(g, with_labels=True)
    plt.show()


def to_excel(res_dict, path):
    """
    字典保存为excel
    :param res_dict:
    :param path:
    """
    results_df = pd.DataFrame(res_dict)
    results_df.to_excel(path, index=False)
    print('the result has been saved as {0}'.format(path))


def get_max_idxs(li):
    """
    计算列表最大值对应的索引列表，若列表全为0，则返回空列表
    :param li:
    :return:
    """
    max_idxs = []
    if sum(li) == 0:
        return max_idxs
    max_n = max(li)
    for i in range(len(li)):
        if li[i] == max_n:
            max_idxs.append(i)
    return max_idxs


def save_comms(pred_comms, comms_path):
    """
    保存社区
    :param pred_comms:
    :param comms_path:
    """
    with open(comms_path, 'w') as f:
        for comm in pred_comms:
            for node in comm:
                f.write(str(node) + ' ')
            f.write('\n')
    print('comms have been saved.')
