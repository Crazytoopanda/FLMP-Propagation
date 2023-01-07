# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 15:46:06 2021

@author: asus
"""


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
del matplotlib.font_manager.weight_dict['roman']

"""
CPM_SOLO在真实数据集上的精度实验(柱状图)

"""
plt.rc('font', family='Times New Roman')  # 全局字体
matplotlib.rcParams.update({'font.size': 20})  # 改变所有字体大小

plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

# tick_label = ['1239671','2363991','5747502','7682452','parking lot']  # 横坐标名称
tick_label = ['100','200','300','400','500']
# tick_label = ['0.1','0.2','0.3','0.4','0.5','0.6','0.7']
bar_width = 0.1  # 柱宽
plt.rcParams['figure.figsize'] = (8.0, 4.5)

# datasets

x = np.arange(0, len(tick_label), 1)
y1 = [0.268,0.271,0.2591,0.2549,0.2457]  #Z ONMI:CPM_HFL
y2 = [0.268,0.271,0.2591,0.2549,0.2457]  # ONMI:CPM_SOLO-2方
y3 = [0.268,0.271,0.2591,0.2549,0.2457]   # ONMI:CPM_SOLO-4方
y4 = [0.268,0.271,0.2591,0.2549,0.2457]  # ONMI:CPM_SOLO-6方
y5 = [0.268,0.271,0.2591,0.2549,0.2457]   # ONMI:CPM_SOLO-8方
y6 = [0.268,0.271,0.2591,0.2549,0.2457]   # ONMI:CPM_SOLO-10方
y7 = [0.068,0.067,0.0648,0.0629,0.0621]   # PIG-ACOPRA

# 画图
colors = ['#666699', '#FEC211', '#CC3333', '#6699CC', '#3BC371', '#FF6666',
          '#5F9EA0','#DEB887']
alpha = 0.7  # 色深
plt.bar(x, y1, width=bar_width, color=colors[0], align='center', label='ACOPRA', alpha=alpha, edgecolor='black',
        hatch="//")
plt.bar(x + bar_width, y2, width=bar_width, color=colors[1], align='center', label='FMLPA-2', alpha=alpha, edgecolor='black')
plt.bar(x + bar_width*2, y3, width=bar_width, color=colors[2], align='center', label='FMLPA-4', alpha=alpha, edgecolor='black',
        hatch='-')
plt.bar(x + bar_width*3, y4, width=bar_width, color=colors[3], align='center', label='FMLPA-6', alpha=alpha, edgecolor='black')
plt.bar(x + bar_width*4, y5, width=bar_width, color=colors[4], align='center', label='FMLPA-8', alpha=alpha, edgecolor='black',
        hatch="\\\\")
plt.bar(x + bar_width*5, y6, width=bar_width, color=colors[5], align='center', label='FMLPA-10', alpha=alpha, edgecolor='black')
plt.bar(x + bar_width*6, y7, width=bar_width, color=colors[6], align='center', label='PIG-ACOPRA', alpha=alpha, edgecolor='black',
        hatch="//")
# plt.xlabel("real-world network")  # 横坐标标题

# plt.xlabel("Number of overlapping vertices")  # 横坐标标题
font0 = {
'style' : 'italic'
}
plt.xlabel("on",font0)  # 横坐标标题
# plt.xlabel("Artificial network")
plt.ylabel("EQ")  # 纵坐标标题
plt.ylim(ymin=0, ymax=0.4)  # 纵坐标范围
plt.xticks(x + bar_width * 5 / 2, tick_label)  # 设置横坐标名称和位置

plt.rcParams.update({'font.size': 18})
plt.legend(loc='upper left',ncol=2,labelspacing=0.1,columnspacing=0.3, prop = {'size':13})  # 显示图例
# plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0,)
plt.savefig('figure on_eq.pdf', format='pdf',bbox_inches='tight')  # 保存
plt.show()  # 显示图形
