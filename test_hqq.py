import networkx as nx
import pandas as pd
# edge_path=''
# file_name_list = ['1239671' ,'2363991','5747502','7682452']
# file_name_list = ['0.1' ,'0.2','0.3','0.4','0.5']
# file_name_list = ['1k', '2k', '3k', '4k', '5k']
# file_name_list = ['1', '2', '3', '4', '5']
file_name_list = ['100', '200', '300', '400', '500']


isReal=False
datatype='artificial'
file='on'

if isReal:
    for file_name in file_name_list:
        df = pd.DataFrame(columns=['id', 'degree'])
        edge_path = './data/' + datatype + '/' + file_name + '.edges'
        g = nx.read_edgelist(edge_path, nodetype=int)
        dict_ori=nx.degree(g)
        # dict_ori=nx.degree_histogram(g)
        # print(dict_ori)

        for i in dict_ori:
            a={'id':i[0],'degree':i[1]}
            df=df.append(a,ignore_index=True)

        print(df['degree'].value_counts())
        # print(df.duplicated().count())
        df.to_csv('./'+file_name+'.csv')
        # print(type(dict_ori))
        # dict_new = {value: key for key, value in dict_ori.items()}
        # print(dict_new)
else:
    for file_name in file_name_list:
        df = pd.DataFrame(columns=['id', 'degree'])
        edge_path = './data/' + datatype + '/' + file + '/network' + file_name + '.txt'
        g = nx.read_edgelist(edge_path, nodetype=int)
        # print(nx.degree(g))
        dict_ori = nx.degree(g)
        # dict_ori=nx.degree_histogram(g)
        # print(dict_ori)
        for i in dict_ori:
            a = {'id': i[0], 'degree': i[1]}
            df = df.append(a, ignore_index=True)

        print(df['degree'].value_counts())
        # print(df.duplicated().count())
        # df.to_csv('./' + file_name + '.csv')
