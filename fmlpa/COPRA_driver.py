# -*- coding: utf-8 -*-
# @Time    : 2019/12/16
# @Author  : yz
# @Version : 1.0

# from corpaoml_al_mp.COPRA_host import COPRA_Host
# from corpaoml_al_mp.COPRA_coordinator import COPRA_Coordinator
from COPRA_host import COPRA_Host
from COPRA_coordinator import COPRA_Coordinator
import time

class COPRA_Driver(object):
    def run(self,Graph,A,n,v,attribute,scale,seed_node,k,mi):

        if seed_node == 'on':
            #种子节点方案初始化标签
            hosts_temp=[]
            Coordinator_temp=COPRA_Coordinator()
            # host是参与方，coordinator是协调方


            # nodedegree 和 choose_seednodes
            for i in range(n):
                hosts_temp.append(COPRA_Host(Graph[i],n))
                hosts_temp[i].send_nodedegree(Coordinator_temp)
            Coordinator_temp.choose_seednodes(scale)
            for i in range(n):
                Coordinator_temp.send_seednodes(i,hosts_temp[i])
            for i in range(n):
                Graph[i] = hosts_temp[i].assign_labels()
        
        G = Graph
        Coordinator=COPRA_Coordinator()
        hosts=[]

        # PSI 做ID matching
        for i in range(n): #  stage1:IDmatch、stage2:step1 生成密鑰隊
            if i == 0:
                hosts.append(COPRA_Host(G[i],n))
                hosts[i].get_intersect_id(G)
                hosts[i].params_init()
            else:
                hosts.append(COPRA_Host(G[i],n))
                hosts[i].get_intersect_id(G)
        
        #将HASH标签映射到整数空间
        # hton 是hash to num
        for i in range(n):
            hosts[i].send_intersect_Hid(Coordinator)

        Coordinator.get_global_intersect_Hid()

        Coordinator.hash_to_num(mi)
        Coordinator.send_hton_to_hosts(hosts)
        for i in range(n):
            hosts[i].transform_hton()
                
        for i in range(1,n): # stage2:step1 各方之間發送和接收公鑰
            hosts[0].send_paillier_params(hosts[i])
        hosts[0].send_pk_to_C(Coordinator)

        #on表示重叠用户节点个数
        if attribute == 'on':  
            for i in range(n): # stage2:step2 各方节点增加attr属性
                hosts[i].add_attr_to_node(A)
                
        min_com_dict = None
        cur_com_dict = None         
        iteration=0    
        while True: # stage2 step3-9
            Coordinator.clear_data()
            for i in range(n):
                hosts[i].clear_data()
            iteration += 1
            for i in range(n):# step3:各方取結點信息、結點加密后發送給Coordinator
                intersect_idx_raw = hosts[i].intersect_idx
                intersect_idx_combin = Coordinator.get_intersect_idx(intersect_idx_raw)#获得各方节点交集的并集

                intersect_host_data = []#获得第i方与其他各方的交集
                for j in range(len(intersect_idx_raw)):
                    intersect_host_data.append(hosts[i].get_intersect_host_data(
                        G[i], intersect_idx_raw[j],attribute,k))
#                print('intersect_host_data',intersect_host_data)
                other_host_data=hosts[i].get_other_host_data(G[i], intersect_idx_combin,attribute)#获得第i方非重叠节点的信息
                hosts[i].save_other_data(other_host_data)#保存到第i方本地
                # other_host_data 是return:{(vi,{lij, nlij}) 这种形式
                
                for j in range(len(intersect_idx_raw)):#加密
                    intersect_host_data_p = hosts[i].encrypt_host_data(
                        intersect_host_data[j], intersect_idx_raw[j],mi)
                    intersect_host_data[j] = intersect_host_data_p
                hosts[i].save_intersect_data(intersect_host_data)
                
            Coordinator.get_intersect_data_com(hosts)#构建所有节点的map1和节点所属方的map2,储存在 Coordinator
            # Coordinator.get_label()
            Coordinator.get_labels(v,hosts)
            
            for i in range(n): 
                Coordinator.send_nodelabelpair(i,hosts[i])
                
                #解密和標簽傳播
                hosts[i].label_propagate(G[i])
              
                hosts[i].populate_other_host_label(G[i],v)
                
            # #计算第一次迭代的度泄露
            # if iteration == 1:
            #     degree_leakage=[] 
            #     begin_time = time.perf_counter()
            #     for i in range(n):
            #         degree_leakage.append(hosts[i].cale_degree_leakage(seed_node))
            #     max_dl = max(degree_leakage)
            #     end_time = time.perf_counter()
                    
            cur_com_dict = Coordinator.get_communities(G)
            # 将字典的value改为社区大小。
            for com in cur_com_dict.keys():
                cur_com_dict[com] = len(cur_com_dict[com])
            # print('[DEBUG]', 'cur_com_dict com idx: ', cur_com_dict.keys())
            # print('[DEBUG]', 'last_com_dict com idx: ', last_com_dict.keys() if last_com_dict is not None else '')
            if (not Coordinator.communities_changed(cur_com_dict, min_com_dict)
                or iteration>30):
                break
            min_com_dict = cur_com_dict
        Graph = Coordinator.merge_graph(G)
        coms = Coordinator.determine_final_communities(Graph)
        print('社区长度',len(coms.values()))
        return coms.values()
            