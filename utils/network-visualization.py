import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# 给节点上颜色用，相同社区上一个颜色
def get_node_label(community_file):
    cmus = []
    with open(community_file, 'r') as f:
        for row in f:
            cmu = row.split()
            cmus.append(cmu)
    
    node_label = {}
    for cmu_id, nodes in enumerate(cmus):
        node_label.update({node: cmu_id for node in nodes})

    return node_label




# 网络的边集文件
# net_file = './data/facebook1/facebook414.txt'
# # 划分出的社区文件
# cmu_file = './data/facebook1/real_facebook414.txt'

net_file = './data/dolphin/dolphin.txt'
# 划分出的社区文件
cmu_file = './data/dolphin/real_dolphin.txt'

G = nx.read_edgelist(net_file)
node_label = get_node_label(cmu_file)
values = [node_label.get(node) for node in G.nodes()]

# plt.title('football real cmu')
plt.xticks(np.arange(0, 1.2, step=0.2))
plt.yticks(np.arange(0, 1.2, step=0.2))

# 真实社区可视化。
plt.axes([0.1, 0.1, 0.8, 0.8])
pos = nx.spring_layout(G)
plt.axis("off")
nx.draw_networkx(G, pos=pos, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=False, edge_color='w')

plt.savefig('dolphin3.pdf') # 保存成PDF放大后不失真（默认保存在了当前文件夹下）
plt.show()