# @Time : 2021/3/9 1:21 下午 

# @Author : yeenjie

# @File : utils.py 

# @Software: PyCharm

def my_hash(node, len):
    return abs(hash(str(node))) % (10 ** len)