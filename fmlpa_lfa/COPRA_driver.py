"""
COPRA_Reviewer联邦化driver

@author: Lfa
update: 2022/9/22
"""
import networkx as nx

from COPRA_coordinator import COPRA_Coordinator
from COPRA_host import COPRA_Host

class COPRA_Driver():
    def run(self, G:nx.Graph, A, n, v, attribute, scale,
            seed_node, k, mi):

        if attribute == "on":
            # host为参与方，coordinator是协调方
            hosts_temp = []
            coordinator_temp = COPRA_Coordinator()

            for i in range(n):
                hosts_temp.append(COPRA_Host(G[i], n))
                # 将该参与方图的节点度发送至协调方
                hosts_temp[i].send_nodedegree(coordinator_temp)
            coordinator_temp.choose_seednodes(scale)
            for i in range(n):
                coordinator_temp.send_seednodes(i,hosts_temp[i])
            for i in range(n):
                G[i] = hosts_temp[i].assign_labels()

        graph = G.copy()
        coordinator = COPRA_Coordinator()
        hosts = []

        # PSI做ID matching
        # stage1: IDmatch
        # 生成密钥对
        for i in range(n):
            hosts.append(COPRA_Host(graph[i], n))
            hosts[i].get_intersect_id(graph)
            if i == 0:
                hosts[i].params_init()

        # 将HASH标签映射到整数空间
        # hton 是 hash to num
        for i in range(n):
            hosts[i].send_intersect_Hid(coordinator)
        coordinator.get_global_intersect_Hid()
        coordinator.hash_to_num(mi)
        coordinator.send_hton_to_hosts(hosts)
        for i in range(n):
            hosts[i].transform_hton()

        # stage2: step1 各方之间发送和接受公钥
        for i in range(1, n):
            hosts[0].send_paillier_params(hosts[i])
        hosts[0].send_key_to_coordinator(coordinator)

        # on表重叠用户节点个数
        if attribute == "on":
            # stage2: step2 各方节点增加attribute属性
            for i in range(n):
                hosts[i].add_attribute_to_node(A)

        min_communities = None
        cur_communities = None
        time_iteration = 0
        while True:
            # 所有参与方以及协调方初始化，迭代次数+=1
            coordinator.clear_data()
            for i in range(n):
                hosts[i].clear_data()
            time_iteration += 1

            # stage2: step3 各方取节点信息、节点加密后发送给协调方
            for i in range(n):
                intersect_idx_raw = hosts[i].intersect_idx
                intersect_idx_combin = coordinator. \
                    get_intersect_idx(intersect_idx_raw)

                # 获得第i方与其他方的交集
                intersect_host_data = []
                for j in range(len(intersect_idx_raw)):
                    intersect_host_data.append(hosts[i].get_intersect_host_data(
                        graph[i], intersect_idx_raw[j], attribute, k
                    ))

                # 获得第i方非重叠节点集
                other_host_data = hosts[i].get_other_host_data(
                    graph[i], intersect_idx_combin, attribute)
                # 保存第i方本地
                hosts[i].save_other_data(other_host_data)

                # 加密！！
                for j in range(len(intersect_idx_raw)):
                    intersect_host_data_temp = hosts[i].encrypt_host_data(
                        intersect_host_data[j], intersect_idx_raw[j], mi
                    )
                    intersect_host_data[j] = intersect_host_data_temp
                hosts[i].save_intersect_data(intersect_host_data)

            # 构建所有节点的map1以及节点所属方的map2，存储到协调方
            coordinator.get_intersect_data_communities(hosts)
            coordinator.get_labels(v, hosts)

            # 解密以及标签传播
            for i in range(n):
                coordinator.send_nodelabelpair(i, hosts[i])
                hosts[i].label_propagate(graph[i])
                hosts[i].populate_other_host_label(graph[i], v)

            cur_communities = coordinator.get_communities(graph)
            for com in cur_communities.keys():
                cur_communities[com] = len(cur_communities[com])
            if time_iteration > 30 or (not coordinator.communities_changed
                        (cur_communities, min_communities)):
                break
            min_communities = cur_communities.copy()
        Graph = coordinator.merge_graph(graph)
        communities = coordinator.determine_final_communities(Graph)
        print("社区长度", len(communities.values()))
        return communities.values()

