"""
测试联邦化COPRA算法

@author: Lfa
update: 2022/9/26
"""

import time
import onmi
import EQ
from COPRA_read_data import COPRA_Read_Data
from COPRA_driver import COPRA_Driver
from COPRA_coordinator import COPRA_Coordinator

class Test_COPRA():
    def test_intersect(self, datatype, seed_node, attribute, param, party, file_name, scale, k, mi):
        edge_path = []
        if datatype == 'artificial':
            for i in range(int(party)):
                edge_path.append(
                    '../data/' + datatype + '/' + param + '/' + party + '/network' + file_name + '_{}.txt'.format(i))
            feat_path = '../data/' + datatype + '/' + param + '/feat/network' + file_name + '_bd_feat.txt'
            write_path = '../data/' + datatype + '/' + param + '/' + party + '/network' + file_name + '_' + party + '_re.txt'
            real_path = '../data/' + datatype + '/' + param + '/' + party + '/community' + file_name + '.txt'
        else:
            for i in range(int(party)):
                edge_path.append('../data/' + datatype + '/' + party + '/' + file_name + '_{}.txt'.format(i))

            # edge_path 原始图数据的存放位置
            # feat_path 属性的存放位置
            # real_path 存放答案的位置
            feat_path = '../data/' + datatype + '/feat/' + file_name + '.feat'
            write_path = '../data/' + datatype + '/' + party + '/' + file_name + '_' + party + '_re.txt'
            real_path = '../data/' + datatype + '/' + party + '/' + file_name + '.circles'
            graph_path = '../data/' + datatype + '/' + file_name + '.edges'

        begin_time = time.perf_counter()
        G = []
        nodeset = []

        # party是2|4|8|10 这种
        n = int(party)
        Coordinator = COPRA_Coordinator()
        load_data = COPRA_Read_Data()
        for i in range(n):
            G.append(load_data.read_graph_from_file(edge_path[i], seed_node))
            # nodeset是所有多个网络里的所有节点 e.g. n=2 有两个网络
            nodeset.append(G[i].nodes())
        sum1 = 0
        sum2 = 0
        for small_g in G:
            sum1 += small_g.number_of_edges()
            sum2 += small_g.number_of_nodes()

        if datatype == 'real':
            # 用于计算模块度
            Graph = load_data.read_graph_from_file(graph_path, seed_node)

        # 执行COPRA主要逻辑代码的地方

        # 读取属性矩阵
        A = load_data.read_attr_from_file(feat_path)
        Driver = COPRA_Driver()
        communities = Driver.run(G, A, n, 2, attribute, scale, seed_node, k, mi)
        end_time = time.perf_counter()
        total_time = end_time - begin_time

        Coordinator.print_communities_to_file(communities, write_path)

        onmi_ = onmi.cale_onmi(real_path, write_path)
        if datatype == 'real':
            EQ_ = EQ.cal_EQ(communities, Graph)
            print('eq：', EQ_)
        else:
            EQ_ = 0
        print('时间：', total_time)
        return total_time, [onmi_, EQ_]

def write_file(data, location):
    output_file = open(location, 'a')
    output_file.write(str(data))
    output_file.close()
    return

if __name__ == '__main__':
    datatype = 'artificial'
    # datatype = 'real'
    seed_node = 'off'
    scale = 0.5
    k = 0.5
    mi = 5
    attribute = 'on'
    # attribute = 'off'
    param = 'om'
    parties = ['10', "8", "6", "4", "2"]
    # party = "4"
    # party = "6"
    # party = "8"
    # party = '10'
    result = []
    write_file_path  = "../data/om2.txt"
    filenames = ['4', '5']
    # filenames = ["1239671"]
    for party in parties:
        for file_name in filenames:
            app = Test_COPRA()
            timex, [onmi_, eq_] = app.test_intersect(datatype, seed_node, attribute, param, party, file_name, scale, k, mi)
            strs = str(eq_) + " " + str(onmi_) + " " + str(timex) + " | "
            write_file(strs, write_file_path)
        write_file("\n", write_file_path)
    print(result)
    # file_name = '5747502'
    # file_name = '7682452'

