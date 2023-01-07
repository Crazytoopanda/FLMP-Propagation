import pandas as pd
def load_data(path):
    with open(path, "r") as f:
        text = f.read()
    com = []
    for line in text.split("\n"):
        arr = line.strip().split()
        arr = set(arr)
        # arr = list(map(int, arr))
        com.append(arr)
    return com
if __name__ == '__main__':
    datatype='artificial'
    artificial_file_name='mu'
    file_name='0.5'
    real_path = '../data/' + datatype + '/' + artificial_file_name + '/community' + file_name + '.txt'
    write_path = '../data/' + datatype + '/' + artificial_file_name + '_re_hqq_1231_pig_copra.txt'
    com1 = load_data(real_path)
    com2 = load_data(write_path)
    print('长度')
    print('com1:{0},com2:{1}'.format(len(com1),len(com2)))
    print('元素长度')
    for i in range(len(com1)):
        print('com1的第{0}个长度：{1}'.format(i,len(com1[i])))
    print('-----------')
    for i in range(len(com2)):
        print('com2的第{0}个长度：{1}'.format(i,len(com2[i])))
