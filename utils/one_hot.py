# @Time : 2021/2/27 12:08 上午 

# @Author : yeenjie

# @File : one_hot.py

# @Software: PyCharm
from paillier.CipherPub import CipherPub
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from paillier.PalillierCmp import PalillierCmp


def one_hot(len, number):
    l = [0] * len
    l[number] = 1
    return l

def p_dot(oh, p_list, public_key):
    l = [0]*len(oh)
    idx = 0
    # print(p_list)
    for i in oh:
        p_i = p_list[idx]
        l[idx] = PalillierCmp.mul(p_i, i, public_key)
        idx = idx + 1
    return l

def list_add(l1, l2, public_key):
    rl = [0] * len(l1)
    for i in range(len(l1)):
        rl[i] = PalillierCmp.add(l1[i],l2[i],public_key)
    return rl


if __name__ == '__main__':
    oh = one_hot(10, 2)
    print(oh)