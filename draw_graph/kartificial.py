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
y_major_locator = MultipleLocator(2000)  # 把y轴的刻度间隔设置为10，并存在变量里
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
y1 = [2703.7164 ,1658.6820 ,982.5357 ,569.4648 ,509.4757 ,407.1301 ,414.2388 ,324.9800 ,341.6852 ,326.2504]  # ONMI:CPM_HFL
y2 = [5032.1763 ,2458.8185 ,1732.9687 ,1196.4116 ,1196.1285 ,943.1398 ,573.0245 ,525.9248 ,535.7192 ,590.5584 ]  # ONMI:CPM_SOLO-2方
y3 = [8327.6548 ,3883.2213 ,2743.1738 ,1748.7793 ,1328.9032 ,1364.6642 ,949.8722 ,767.5393 ,836.7230 ,768.0989]  # ONMI:CPM_SOLO-4方
y4 = [10059.3554 ,4860.6609 ,3497.9611 ,2112.0896 ,1861.0330 ,1370.2251 ,1377.7432 ,945.5279 ,1120.7064 ,868.5688 ]  # ONMI:CPM_SOLO-6方
y5 = [10501.0389 ,5301.1239 ,4421.8921 ,3077.2388 ,2593.4650 ,1822.6367 ,1216.3347 ,1580.5284 ,1204.3560 ,1046.7097  ]  # ONMI:CPM_SOLO-8方
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
plt.ylim(ymin=0, ymax=11000)  # 纵坐标范围
plt.xlim(xmin=0.1,xmax=1)
plt.xticks(x + bar_width * 0 / 2, tick_label)

plt.rcParams.update({'font.size': 25})
plt.legend(loc='upper right',ncol=1,labelspacing=0.1,columnspacing=0.3)  # 显示图例
plt.savefig('figure kartificial.pdf', format='pdf',bbox_inches='tight')  # 保存
plt.show()  # 显示图形
