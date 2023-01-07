import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

plt.rcParams['figure.figsize'] = (8,4.5)
plt.rc('font', family='Times New Roman')  # 全局字体
matplotlib.rcParams.update({'font.size': 25})  # 改变所有字体大小

plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

ax = plt.gca()

y_major_locator = MultipleLocator(600)  # 把y轴的刻度间隔设置为10，并存在变量里
ax.yaxis.set_major_locator(y_major_locator)  # 把y轴的主刻度设置为10的倍数

N = 6
ind = np.arange(N)  # [ 0  1  2  3  4  5  6  7  8  9 10 11 12]
plt.xticks(ind, ('Standalone', '2', '4', '6', '8', '10'))

plt.ylabel('Running time (s)')
# plt.yticks(np.arange(0, 200, 50))

Bottom = (0.0000,377.2355,797.1240,1315.5691,1366.2657,2097.6861)  # Encryption/Decryption
Center1 = (48.5982 ,97.3943,207.9431,294.1593,275.7019,534.9274)  # Label propagation
Center2 = (0.0000,0.3654,0.5613,0.8126,0.9534,1.3699) # perturbation
Top = (0.0000,0.0260,0.0313,0.0625,0.0469,0.1094)  # Communication cost

d1 = []
for i in range(0, len(Bottom)):
    sum = Bottom[i] + Center1[i]
    d1.append(sum)

d2 = []
for i in range(0, len(d1)):
    sum = d1[i] + Center2[i]
    d2.append(sum) 


width = 0.35  # 设置条形图一个长条的宽度

p1 = plt.bar(ind, Bottom, width, color='#5B9BD5')
p2 = plt.bar(ind, Center1, width, bottom=Bottom, color='#A5A5A5')
p3 = plt.bar(ind, Center2, width, bottom=d1, color='#800080')
p4 = plt.bar(ind, Top, width, bottom=d2, color='#ED7D31')
matplotlib.rcParams.update({'font.size': 21})  # 改变所有字体大小
plt.ylim(ymin=0, ymax=2700)  # 纵坐标范围

ax.set_xlabel("Number of participants")  # 横坐标标题
# plt.legend((p1[0], p2[0], p3[0]), ('ID matching', 'perturbation', 'others'), loc=0)
# plt.legend((p1[0], p2[0]), ('encryption', 'others', 'others'), loc=0)
matplotlib.rcParams.update({'font.size': 18})
plt.legend((p1[0], p2[0], p3[0],p4[0]), ('Encryption/Decryption', 'Label propagation','Perturbation', 'Communication cost'), loc='upleft')

plt.savefig('figure time_mu0.5.pdf', format='pdf', bbox_inches='tight')  # 保存

plt.show()
