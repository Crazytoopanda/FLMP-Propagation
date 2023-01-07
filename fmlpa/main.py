# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 00:56:26 2020

@author: asus
"""


from test_COPRAoFL import Test
import xlsxwriter

app = Test
run_num = 1
attrs = ['on']  
seed_node ='off'
# datatype = 'real'
datatype = 'artificial'
label_assign = [0.07]
# label_assign = [0.1]
# k = 50
k =0.5
mi = 5 #混合系数，表示用户节点与外部社区相连的概率


# file_names = ['1239671','2363991','5747502','7682452']
# file_names = ['1239671','5747502','7682452']
# file_names = ['7682452']
file_names = ['0.1','0.2','0.3','0.4','0.5','0.6','0.7']
parties = ['2','4','6','8','10']#We first used the Metis tool (Gonzalez et al. 2012) to split the vertices of an original network into 2, 4, 6, 8 and 10 subnet- works.
# parties = ['2']#We first used the Metis tool (Gonzalez et al. 2012) to split the vertices of an original network into 2, 4, 6, 8 and 10 subnet- works.
# parties = ['10']

            
# label_assign = [0.005,0.006,0.007,0.008,0.009,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5]
# params = ['mu','n','om','on']
params = ['mu']
# parties = ['2','4','6','8','10']
# file_names = [
#     ['5k']
              #   ['0.1','0.2','0.3','0.4','0.5','0.6','0.7'],
              #   ['1k','2k','3k','4k','5k'],
              #   ['1','2','3','4','5'],
              #   ['100','200','300','400','500']
               # ]

time_list = []
onmi_list = []
EQ_list = []
if datatype == 'artificial':
    for la in label_assign:
        for attr in attrs:
            i = 0
            for param in params:
                for party in parties:
                    # for file_name in file_names[i]:
                    for file_name in file_names:
                        tl=0
                        ol=0
                        dl=0
                        eq=0
                        for r_index in range(run_num):
                            print('running',param,party,file_name,'for',r_index)
                            print('filename:'+file_name)
                            # 不把k改成r_index后面也会报错
                            time,re = app.test_intersect(datatype, seed_node, attr, param, party, file_name,la,k,mi)
                            # time:total_time  re:[onmi_,EQ_]
                            tl = tl + time
                            ol = ol + re[0]
                            eq = eq + re[1]

                        time_list.append(tl/run_num)
                        onmi_list.append(ol/run_num)
                        EQ_list.append(eq/run_num)
                i = i + 1
else:
    for la in label_assign:
        for attr in attrs:
            for party in parties:
                for file_name in file_names:
                    tl=0
                    ol=0
                    dl=0
                    eq=0
                    for r_index in range(run_num):
                        print('running',party,file_name,'for',r_index)
                        time,re = app.test_intersect(datatype, seed_node, attr, None, party, file_name,la,k,mi)
                        # time:total_time  re:[onmi_,EQ_]
                        tl = tl + time
                        ol = ol + re[0]
                        eq = eq + re[1]
                        # /run_num 求多次平均
                    time_list.append(tl/run_num)
                    onmi_list.append(ol/run_num)
                    EQ_list.append(eq/run_num)
# print(time_list,onmi_list)
# time_list = [1,2,3,4,5]
# onmi_list = [1,2,3,4,5]
workbook = xlsxwriter.Workbook('test-fmlpa.xlsx')
worksheet = workbook.add_worksheet('data')
for i in range(len(time_list)):
    # 每个文件一行
    worksheet.write(i,0,time_list[i])
    worksheet.write(i,1,onmi_list[i])
    worksheet.write(i,2,EQ_list[i])
    worksheet.write(i,3,file_names[i])
workbook.close()
