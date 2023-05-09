import networkx as nx
from matplotlib import pyplot as plt


def leader_rank(graph:nx.Graph) -> dict:
    """
    节点排序
    :param graph:复杂网络图Graph
    :return: 返回节点排序值
    """
    # 节点个数
    num_nodes = graph.number_of_nodes()
    # 节点
    nodes = graph.nodes()
    # 在网络中增加节点g并且与所有节点进行连接
    graph.add_node(0)
    for node in nodes:
        graph.add_edge(0, node)
    # LR值初始化
    LR = dict.fromkeys(nodes, 1.0)
    LR[0] = 0.0
    # 迭代从而满足停止条件
    while True:
        tempLR = {}
        for node1 in graph.nodes():
            s = 0.0
            for node2 in graph.nodes():
                if node2 in graph.neighbors(node1):
                    s += 1.0 / graph.degree([node2])[node2] * LR[node2]
            tempLR[node1] = s
        # 终止条件:LR值不在变化
        error = 0.0
        for n in tempLR.keys():
            error += abs(tempLR[n] - LR[n])
        if error < 1:
            break
        LR = tempLR
    # 节点g的LR值平均分给其它的N个节点并且删除节点
    avg = LR[0] / num_nodes
    LR.pop(0)
    for k in LR.keys():
        LR[k] += avg
    graph.remove_node(0) # 删除插入节点
    return LR

if __name__ == "__main__" :

    graph = {"A":set(["B", "D", "E", "G"]), \
             "B":set(["A", "C", "D"]), \
             "C":set(["B", "D"]), \
             "D":set(["A", "B", "C"]), \
             "E":set(["A", "G", "F"]), \
             "F":set(["E", "G"]), \
             "G":set(["A", "E", "F"])}
    G = nx.Graph(graph)
    for node, data in G.nodes(True) :
        data["label"] = 1
    LR = leader_rank(G).items()
    nx.draw(G, with_labels=True, arrows=True)
    plt.show()


