import copy
import time
from itertools import combinations
from queue import Queue

import networkx as nx

"""
迭代计算k团：先计算三角形，再计算k团
"""


def get_triangles(g):
    """
    计算图g的三角形集合
    :return:图g的三角形
    """
    g = copy.deepcopy(g)  # 深拷贝
    # 将节点按照度从小到大排序并放进队列
    degree_node = [(y, x) for x, y in g.degree]  # x -> node,y -> degree of node
    degree_node = sorted(degree_node)
    node_queue = Queue()
    for x, y in degree_node:
        node_queue.put(y)
    # 计算三角形
    triangles = set()
    while not node_queue.empty():
        node = node_queue.get()
        node_neighbors = list(g.neighbors(node))
        nbr_tuples = combinations(node_neighbors, 2)  # 当前节点邻居两两组合
        for nbr_tuple in nbr_tuples:
            if g.has_edge(nbr_tuple[0], nbr_tuple[1]):
                triangle = [node, nbr_tuple[0], nbr_tuple[1]]
                triangle = tuple(sorted(triangle))  # 三角形
                triangles.add(triangle)
        g.remove_node(node)
    return triangles


def get_k_cliques(g, k):
    """
    计算图g的k团集合
    :return:图g的k团集合
    """
    cliques = get_triangles(g)  # 当前分区子图g的三角形集合
    if k == 3:
        return cliques
    while k > 3:
        ext_cliques = copy.deepcopy(cliques)
        for clique in cliques:
            ext_cliques.remove(clique)
            nodes_neighbors = []
            for node in clique:  # k团所有顶点
                nodes_neighbors.append(g.neighbors(node))  # k团顶点的所有邻居
            candidates = set(nodes_neighbors[0]).intersection(*nodes_neighbors[1:])  # k团所有顶点的所有邻居的交集
            while candidates:
                # print(candidates)
                c = candidates.pop()
                ext_clique = set(copy.deepcopy(clique))
                ext_clique.add(c)
                ext_clique = tuple(sorted(ext_clique))
                ext_cliques.add(ext_clique)
        cliques = ext_cliques
        k -= 1
    cliques = [frozenset(x) for x in cliques]
    return cliques


if __name__ == "__main__":
    # g = nx.karate_club_graph
    g = nx.read_edgelist('network0.6.txt', nodetype=int)
    # print(g.edges())
    # exit()
    k = 4
    t1 = time.process_time()
    le = get_k_cliques(g, k)
    t2 = time.process_time() - t1
    print(t2)
    # print(le)
    print(len(le))

    t3 = time.process_time()
    real = [x for x in nx.enumerate_all_cliques(g) if len(x) == k]
    t4 = time.process_time() - t3
    print(t4)
    print(len(real))
    # print(real)
