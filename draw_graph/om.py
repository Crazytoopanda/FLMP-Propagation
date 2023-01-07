#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021-01-04 10:00
# @Author : wmy
import matplotlib
import matplotlib.ticker as mticker 
import matplotlib.pyplot as plt
import numpy as np
del matplotlib.font_manager.weight_dict['roman']

plt.rc('font', family='Times New Roman')  # 全局字体
matplotlib.rcParams.update({'font.size': 20})  # 改变所有字体大小

plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

# tick_label = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7']  # 横坐标标签
# tick_label = ['1k','2k','3k','4k','5k']
tick_label = ['1','2','3','4','5']
# tick_label = ['2','4','6','8','10']
bar_width = 0.1  # 柱宽
plt.rcParams['figure.figsize'] = (8.0, 4.5)
# datasets
x = np.arange(0, len(tick_label), 1)
# x = np.arange(0.1, (len(tick_label) + 1) * 0.1, 0.1)
y1 = [24.9122 ,36.9361 ,51.2902 ,63.6051 ,78.6239 ]  # ONMI:CPM_HFL
y2 = [240.4009 ,321.1991 ,504.2153 ,623.5709 ,786.0102 ]  # ONMI:CPM_SOLO-2方
y3 = [521.8564 ,627.6251 ,964.9684 ,1315.2358 ,1321.9968 ]  # ONMI:CPM_SOLO-4方
y4 = [793.6508 ,1231.8036 ,1741.4045 ,2050.7940 ,2609.8593 ]  # ONMI:CPM_SOLO-6方
y5 = [1087.0638 ,1790.4633 ,2390.6293 ,2780.9167 ,3487.2501 ]  # ONMI:CPM_SOLO-8方
y6 = [1285.2952 ,2010.8230 ,2721.1503 ,2830.0238 ,4050.3574 ]  # ONMI:CPM_SOLO-10方

# 画图

colors = ['#666699', '#FEC211', '#CC3333', '#6699CC', '#3BC371', '#FF6666']

alpha = 0.8  # 色深
plt.plot(x, y1, marker='s', color=colors[0], label='SMLPA', alpha=alpha)
plt.plot(x, y2, marker='o', color=colors[1], label='FMLPA-2', alpha=alpha)
plt.plot(x, y3, marker='x', color=colors[2], label='FMLPA-4', alpha=alpha)
plt.plot(x, y4, marker='>', color=colors[3], label='FMLPA-6', alpha=alpha)
plt.plot(x, y5, marker='+', color=colors[4], label='FMLPA-8', alpha=alpha)
plt.plot(x, y6, marker='<', color=colors[5], label='FMLPA-10', alpha=alpha)

# plt.xlabel("Number of memberships of the overlapping vertices")  # 横坐标标题
font0 = {
    'style' : 'italic',
}

plt.xlabel("om",font0)  # 横坐标标题
plt.ylabel("Runtime")  # 纵坐标标题
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f s'))
# plt.xlim(xmin=0.1, xmax=0.7)  # 横坐标范围
plt.ylim(ymin=0, ymax=4100)  # 纵坐标范围
plt.xlim(xmin=2)
plt.xticks(x + bar_width * 0 / 2, tick_label)

plt.rcParams.update({'font.size': 17})
plt.legend(loc='upper left',ncol=2,labelspacing=0.1,columnspacing=0.3)  # 显示图例
plt.savefig('figure omt.pdf', format='pdf',bbox_inches='tight')  # 保存
plt.show()  # 显示图形
