#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/26
# @Author  : Kun Guo
# @Version : 1.0

import rsa
import gmpy2
# from intersect_mp.tools import IntersectTools
from intersect.tools import IntersectTools

class IntersectHost(object):
    def __init__(self, rsa_key_bits = 1024):
        self.rsa_public_key, self.rsa_secret_key = rsa.newkeys(rsa_key_bits)
        # host_idx_map = {encrypted host id : raw host id}
        self.host_idx_map = None

    def get_rsa_public_key(self):
        return self.rsa_public_key

    def process_guest_idx(self, guest_idx, i):
        '''
        :param guest_idx  = [r^e % n * hash(guest_user_id)]
        :return: [r * (hash(guest_user_id)^d % n)]
        '''
        print('Process guest{} idx at host'.format(i))
        n = self.rsa_public_key.n
        d = self.rsa_secret_key.d
        guest_idx_host = list(map(lambda x: gmpy2.powmod(int(x), d, n), guest_idx))
        return guest_idx_host

    def send_host_idx(self, dataset, i):
        '''
        :param dataset [host_user_id]
        :return: [hash(hash(host_uer_id)^d % n)]
        '''
        print('Send host idx to guest{}'.format(i))
        n = self.rsa_public_key.n
        d = self.rsa_secret_key.d
        host_idx = list(map(lambda x: IntersectTools.hash(gmpy2.powmod(int(IntersectTools.hash(x), 16), d, n)), dataset))
        self.host_idx_map = dict(zip(host_idx, dataset))
        return host_idx

    def process_intersect_idx(self, intersect_idx_enc):
        '''
        :param intersect_idx_enc = hash(hash(intersect_user_id)^d % n)
        :return: {raw intersect idx}
        '''
        print('Process intersection at host')
        intersect_idx_raw = set(map(lambda x: self.host_idx_map[x], intersect_idx_enc))
        return intersect_idx_raw