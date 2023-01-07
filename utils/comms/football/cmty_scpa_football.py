# @Time : 2021/3/24 3:55 下午 

# @Author : yeenjie

# @File : cmty_scpa_dp.py.py 

# @Software: PyCharm
import csv

import networkx as nx

if __name__ == '__main__':
    G = nx.read_edgelist(r'football.txt')

    partition = dict()
    num_dict = dict()
    # 读入社区划分结果
    with open('football_cmty.txt', "r")as f:
        f_csv = csv.reader(f)
        i = 1
        for row in f_csv:
            idx = row[0].strip().split(' ')
            num_dict[i] = len(idx)
            for id in idx:
                partition[id] = i
            i = i + 1
    # print(num_dict)
    # exit()
    # print(sorted(num_dict.values()))
    # print(num_dict.index(44))
    # exit()
    # 选择社区编号
    ch = [5, 4, 3, 2, 1]
    ntd = []
    for node in partition.keys():
        if partition[node] not in ch:
            ntd.append(node)
    for node in ntd:
        partition.pop(node)
    for node in partition.keys():
        if partition[node] == ch[0]:
            partition[node] = 0
        elif partition[node] == ch[1]:
            partition[node] = 1
        elif partition[node] == ch[2]:
            partition[node] = 2
        else:
            partition[node] = 3

    H = G.copy()
    H.remove_nodes_from(v for v in G if v not in partition.keys())
    G = H

    # seed可以自由选择
    pos = nx.spring_layout(G, iterations=10, seed=10001)  # compute graph layout
    # plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
    plt.axis('off')

    nx.draw_networkx_nodes(G, pos, nodelist=partition.keys(), node_size=50, cmap=plt.cm.RdYlBu, alpha=0.8,
                           node_color=list(partition.values()))

    plt.savefig('cmty_scpa_an_parking lot.pdf', format='pdf', bbox_inches='tight')
    plt.show()
