from collections import defaultdict

import networkx as nx

"""
    paper:<<Detect overlapping and hierarchical community structure in networks>>
    G:vertex-neighbors {vertex:list(neighbors)}
"""


def cal_EQ(cover, G):
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

    return round(total / (2 * m), 4)


def load_comm(path):
    with open(path, "r") as f:
        text = f.read()
    com = []
    for line in text.split("\n"):
        arr = line.strip().split()
        # arr = list(map(int, arr))
        com.append(arr)
    return com


if __name__ == "__main__":
    G = nx.read_edgelist('../datasets/attribute/n/2/network1k.txt')
    com = load_comm('../datasets/attribute/n/2/community1k.txt')
    mod = cal_EQ(com, G)
    print(mod)
    # G = nx.read_edgelist('../../corpa/genuine/dolphin.txt')
    # com = load_corpa('../../corpa/genuine/corpaoml_am_dolphin_community.txt')
    # mod = cal_EQ(com, G)
    # print(mod)
    # G = nx.read_edgelist('../../corpa/genuine/polbooks.txt')
    # com = load_corpa('../../corpa/genuine/corpaoml_am_polbooks_community.txt')
    # mod = cal_EQ(com, G)
    # print(mod)
    # G = nx.read_edgelist('../../corpa/genuine/SFI.txt')
    # com = load_corpa('../../corpa/genuine/corpaoml_am_SFI_community.txt')
    # mod = cal_EQ(com, G)
    # print(mod)
    # G = nx.read_edgelist('../../corpa/genuine/football.txt')
    # com = load_corpa('../../corpa/genuine/corpaoml_am_football_community.txt')
    # mod = cal_EQ(com, G)
    # print(mod)
    # G = nx.read_edgelist('../../corpa/genuine/jazz.txt')
    # com = load_corpa('../../corpa/genuine/corpaoml_am_jazz_community.txt')
    # mod = cal_EQ(com, G)
    # print(mod)
