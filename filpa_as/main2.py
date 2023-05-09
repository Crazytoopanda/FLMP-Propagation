"""
测试联邦化COPRA算法

@author: Lfa
update: 2023/4/25
"""
import multiprocessing
import threading
from Test_COPRA import *


def threading_Main(i):
    datatype = 'artificial'
    # datatype = 'real'
    seed_node = 'off'
    scale = 0.5
    k = 0.5
    mi = 5
    attribute = 'on'
    # attribute = 'off'
    params = ['alone_mu0.1', 'alone_mu0.3', 'alone_mu0.4', 'alone_mu0.5']
    parties = ["4"]
    # party = "4"
    # party = "6"
    # party = "8"
    # party = '10'
    result = []
    write_file_path = "../data/1"
    filenames = ["10k"]
    # filenames = ["1239671"]
    for party in parties:
        for file_name in filenames:
            app = Test_COPRA()
            timex, [onmi_, eq_] = app.test_intersect(datatype, seed_node, attribute, params[i], party, file_name, scale,
                                                     k, mi)
            strs = str(eq_) + " " + str(onmi_) + " " + str(timex) + " | "
            write_file(strs, write_file_path + params[i])
        write_file("\n", write_file_path + params[i])
    print(result)
    # file_name = '5747502'
    # file_name = '7682452'


def write_file(data, location):
    output_file = open(location, 'a')
    output_file.write(str(data))
    output_file.close()
    return

if __name__ == '__main__':
    threading_Main(2)