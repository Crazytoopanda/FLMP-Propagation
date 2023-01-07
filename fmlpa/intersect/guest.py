#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/26
# @Author  : Kun Guo
# @Version : 1.0

import rsa
import random
import gmpy2
# from intersect_mp.tools import IntersectTools
from intersect.tools import IntersectTools

class IntersectGuest(object):
    def __init__(self, rsa_public_key, random_bit = 1024):
        super().__init__()
        self.rsa_public_key = rsa_public_key
        self.random_bit = random_bit
        self.random_r = None
        self.dataset = None

    def send_guest_idx(self, dataset, i):
        '''
        :param dataset [guest_user_id]
        :return: [r^e % n * hash(guest_user_id)]
        '''
        print('Send guest{} idx to host'.format(i))
        self.dataset = dataset
        n = self.rsa_public_key.n
        e = self.rsa_public_key.e
        self.random_r = list(map(lambda x: random.SystemRandom().getrandbits(self.random_bit), dataset))
        hid = list(map(lambda x: int(IntersectTools.hash(x), 16), dataset))
        # guest_idx = [r^e % n * hash(guest_user_id)]
        guest_idx = list(map(lambda x: x[1] * gmpy2.powmod(x[0], e, n), zip(self.random_r, hid)))
        return guest_idx

    def process_host_guest_idx(self, host_idx, guest_idx_host, i):
        '''
        :param host_idx = [hash(hash(host_uer_id)^d % n)]
        :param guest_idx_host = [r * (hash(guest_user_id)^d % n)]
        :return: (encrypted_intersect_idx, raw_intersect_idx), encrypted_intersect_idx = hash(hash(intersect_user_id)^d % n)
        '''
        print('Process host and guest{0} encrypted idx at guest{0}'.format(i))
        n = self.rsa_public_key.n
        # guest_idx_dec = ([hash(hash(guest_user_id)^d % n)]
        guest_idx = list(map(lambda x: IntersectTools.hash(gmpy2.divm(x[0], x[1], n)), zip(guest_idx_host, self.random_r)))
        # intersect_idx_map = {encrypted guest id : raw guest id}
        intersect_idx_map = dict(zip(guest_idx, self.dataset))
        intersect_idx_enc = set(host_idx) & set(guest_idx)
        intersect_idx_raw = set(map(lambda x: intersect_idx_map[x], intersect_idx_enc))
        return (intersect_idx_enc, intersect_idx_raw)