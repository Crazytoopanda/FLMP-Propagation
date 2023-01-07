#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021-01-04 10:00
# @Author : wmy
import matplotlib
import matplotlib.ticker as mticker 
import matplotlib.pyplot as plt
import numpy as np

plt.rc('font', family='Times New Roman')  # 全局字体
matplotlib.rcParams.update({'font.size': 20})  # 改变所有字体大小

plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

# tick_label = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7']  # 横坐标标签
# tick_label = ['1k','2k','3k','4k','5k']
tick_label = ['SMLPA','2','4','6','8','10']
bar_width = 0.1  # 柱宽
plt.rcParams['figure.figsize'] = (8.0, 4.5)
# datasets
x = np.arange(0, len(tick_label), 1)
# x = np.arange(0.1, (len(tick_label) + 1) * 0.1, 0.1)
y1 = [0.1494 ,5.2597 ,15.1909 ,34.6226 ,49.7603 ,82.9801 ]  # ONMI:CPM_HFL
y2 = [2.0711 ,47.0168 ,112.5747 ,205.1779 ,293.5425 ,362.6469 ]  # ONMI:CPM_SOLO-2方
y3 = [0.1451 ,9.3603 ,20.1072 ,30.6513 ,53.5946 ,77.2434 ]  # ONMI:CPM_SOLO-4方
y4 = [2.1067 ,43.8263 ,128.1875 ,168.6012 ,245.4387 ,417.3066 ]  # ONMI:CPM_SOLO-6方
y5 = [2.4469 ,67.4572 ,131.0350 ,210.5164 ,282.7787 ,423.9426 ]  # ONMI:CPM_SOLO-8方
# y6 = [604.4160 ,927.0779 ,1413.3379 ,1600.9370 ,2634.0928 ,2521.0292 ,4002.0559 ]  # ONMI:CPM_SOLO-10方

# 画图

colors = ['#666699', '#FEC211', '#CC3333', '#6699CC', '#3BC371', '#FF6666']

alpha = 0.8  # 色深
plt.plot(x, y1, marker='s', color=colors[0], label='t-1239671', alpha=alpha)
plt.plot(x, y2, marker='o', color=colors[1], label='t-2363991', alpha=alpha)
plt.plot(x, y3, marker='x', color=colors[2], label='t-5747502', alpha=alpha)
plt.plot(x, y4, marker='>', color=colors[3], label='t-7682452', alpha=alpha)
# plt.plot(x, y5, marker='+', color=colors[4], label='parking lot', alpha=alpha)
# plt.plot(x, y6, marker='<', color=colors[5], label='FMLPA-10', alpha=alpha)

plt.xlabel("Number of participants")  # 横坐标标题
plt.ylabel("Runtime")  # 纵坐标标题
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f s'))
# plt.xlim(xmin=0.1, xmax=0.7)  # 横坐标范围
plt.ylim(ymin=0, ymax=450)  # 纵坐标范围
plt.xlim(xmin=2)
plt.xticks(x + bar_width * 0 / 2, tick_label)

plt.rcParams.update({'font.size': 22})
plt.legend(loc='upper left',ncol=1,labelspacing=0.1,columnspacing=0.3)  # 显示图例
plt.savefig('real_time.pdf', format='pdf',bbox_inches='tight')  # 保存
plt.show()  # 显示图形
