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

tick_label = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7']  # 横坐标标签
# tick_label = ['1k','2k','3k','4k','5k']
# tick_label = ['2','4','6','8','10']
bar_width = 0.1  # 柱宽
plt.rcParams['figure.figsize'] = (8.0, 4.5)
# datasets
x = np.arange(0, len(tick_label), 1)
# x = np.arange(0.1, (len(tick_label) + 1) * 0.1, 0.1)
y1 = [30.5450 ,35.1823 ,34.5321 ,30.2456 ,48.5982 ,49.4823 ,63.1097 ]  # ONMI:CPM_HFL
y2 = [253.8079,324.8109,352.8298,449.0027,475.0213,700.8744,928.0316]  # ONMI:CPM_SOLO-2方
y3 = [400.8483,541.2528,541.5164,870.9951,1005.6597,1175.2413,1486.9478]  # ONMI:CPM_SOLO-4方
y4 = [445.1711,642.2352,945.7657,1101.0227,1610.6035,1962.6539,2043.2846]  # ONMI:CPM_SOLO-6方
y5 = [560.8644,887.7444,1191.3171,1674.1560,1642.9679,2352.7269,2917.5784]  # ONMI:CPM_SOLO-8方
y6 = [604.4160,927.0779,1413.3379,1600.9370,2634.0928,2521.0292,4002.0559]  # ONMI:CPM_SOLO-10方

# 画图

colors = ['#666699', '#FEC211', '#CC3333', '#6699CC', '#3BC371', '#FF6666']

alpha = 0.8  # 色深
plt.plot(x, y1, marker='s', color=colors[0], label='SMLPA', alpha=alpha)
plt.plot(x, y2, marker='o', color=colors[1], label='FMLPA-2', alpha=alpha)
plt.plot(x, y3, marker='x', color=colors[2], label='FMLPA-4', alpha=alpha)
plt.plot(x, y4, marker='>', color=colors[3], label='FMLPA-6', alpha=alpha)
plt.plot(x, y5, marker='+', color=colors[4], label='FMLPA-8', alpha=alpha)
plt.plot(x, y6, marker='<', color=colors[5], label='FMLPA-10', alpha=alpha)

# plt.xlabel("Mixing parameter")  # 横坐标标题
font0 = {
    'style' : 'italic',
}

plt.xlabel("mu",font0)  # 横坐标标题
plt.ylabel("Runtime")  # 纵坐标标题
# plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f MB'))
# plt.xlim(xmin=0.1, xmax=0.7)  # 横坐标范围
plt.ylim(ymin=0, ymax=4100)  # 纵坐标范围
plt.xlim(xmin=0.7)
plt.xticks(x + bar_width * 0 / 2, tick_label)

plt.rcParams.update({'font.size': 19})
plt.legend(loc='upper left',ncol=2,labelspacing=0.1,columnspacing=0.3)  # 显示图例
plt.savefig('figure mut.pdf', format='pdf',bbox_inches='tight')  # 保存
plt.show()  # 显示图形
