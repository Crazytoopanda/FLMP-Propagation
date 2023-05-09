#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/27
# @Author  : Kun Guo
# @Version : 1.0
import hashlib

class IntersectTools(object):
    @staticmethod
    def hash(value):
        return hashlib.sha3_256(bytes(str(value), encoding='utf-8')).hexdigest()