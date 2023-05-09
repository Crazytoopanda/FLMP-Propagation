#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/27
# @Author  : Kun Guo
# @Version : 1.0
import unittest
import numpy as np
# from intersect_mp.driver import Intersect
from driver import Intersect
import time


class TestIntersect(unittest.TestCase):
    def test_intersect(self):
        begin_time = time.clock()
        n=4
        dataset0= np.append([1,2,3,4,5], np.random.randint(10, int(1e6), int(1e3)))
        dataset1= np.append([2,3,5,7,9], np.random.randint(10, int(1e6), int(1e3)))
        dataset2= np.append([4,3,5,8,9], np.random.randint(10, int(1e6), int(1e3)))
        dataset3= np.append([1,3,5,7,8], np.random.randint(10, int(1e6), int(1e3)))
        dataset= np.array([dataset0,dataset1,dataset2,dataset3])
        intersect = Intersect()
        intersect_idx_raw = intersect.run(dataset, n)
        end_time = time.clock()
        # print('Time cost: {:.1f} second(s)'.format(end_time - begin_time))
        # print('intersect_idx_raw = ', intersect_idx_raw)

if __name__ == '__main__':
    unittest.main()