#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021-01-04 10:00
# @Author : wmy
import matplotlib
import matplotlib.ticker as mticker 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
del matplotlib.font_manager.weight_dict['roman']

plt.rc('font', family='Times New Roman')  # 全局字体
matplotlib.rcParams.update({'font.size': 20})  # 改变所有字体大小

plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内


ax = plt.gca()
y_major_locator = MultipleLocator(300)  # 把y轴的刻度间隔设置为10，并存在变量里
ax.yaxis.set_major_locator(y_major_locator)  # 把y轴的主刻度设置为10的倍数

tick_label = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7','0.8','0.9','1']  # 横坐标标签
# tick_label = ['1k','2k','3k','4k','5k']
# tick_label = ['100','200','300','400','500']
# tick_label = ['2','4','6','8','10']
bar_width = 0.1  # 柱宽
plt.rcParams['figure.figsize'] = (8.0, 4.5)
# datasets
x = np.arange(0, len(tick_label), 1)
# x = np.arange(0.1, (len(tick_label) + 1) * 0.1, 0.1)
y1 = [186.1400,88.1385,65.1745,35.5146,30.6487,25.3246,20.3751,16.9869,13.3532,12.3390]  # ONMI:CPM_HFL
y2 = [509.7243,270.1925,173.1197,124.1446,95.3787,74.2264,67.0521,55.1534,46.7007,39.4332]  # ONMI:CPM_SOLO-2方
y3 = [860.6468,427.5185,296.5223,204.8476,145.2525,139.6902,109.9630,81.4286,72.5567,73.7065]  # ONMI:CPM_SOLO-4方
y4 = [1261.8210,676.9848,374.9989,328.9631,232.0336,214.6959,149.5580,140.7647,123.8789,110.1971]  # ONMI:CPM_SOLO-6方
y5 = [1398.4230,722.0722,482.4217,437.4185,330.6018,266.5083,220.1169,196.0154,174.1071,168.9830]  # ONMI:CPM_SOLO-8方
# y6 = [1940.5914 ,1715.5246 ,1810.5976 ,1846.7895 ,1789.4154 ]  # ONMI:CPM_SOLO-10方

# 画图

colors = ['#666699', '#FEC211', '#CC3333', '#6699CC', '#3BC371', '#FF6666']

alpha = 0.8  # 色深
plt.plot(x, y1, marker='s', color=colors[0], label='FMLPA-2', alpha=alpha)
plt.plot(x, y2, marker='o', color=colors[1], label='FMLPA-4', alpha=alpha)
plt.plot(x, y3, marker='x', color=colors[2], label='FMLPA-6', alpha=alpha)
plt.plot(x, y4, marker='>', color=colors[3], label='FMLPA-8', alpha=alpha)
plt.plot(x, y5, marker='+', color=colors[4], label='FMLPA-10', alpha=alpha)
# plt.plot(x, y6, marker='<', color=colors[5], label='FMLPA-10', alpha=alpha)
font0 = {
'style' : 'italic'
}
plt.xlabel("K",font0)  # 横坐标标题
plt.ylabel("Runtime")  # 纵坐标标题
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f s'))
# plt.xlim(xmin=0.1, xmax=0.7)  # 横坐标范围
plt.ylim(ymin=0, ymax=1500)  # 纵坐标范围
plt.xlim(xmin=0.1,xmax=1)
plt.xticks(x + bar_width * 0 / 2, tick_label)

plt.rcParams.update({'font.size': 25})
plt.legend(loc='upper right',ncol=1,labelspacing=0.1,columnspacing=0.3)  # 显示图例
plt.savefig('figure k_2363991.pdf', format='pdf',bbox_inches='tight')  # 保存
plt.show()  # 显示图形
