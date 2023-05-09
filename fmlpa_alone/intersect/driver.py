#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/27
# @Author  : Kun Guo
# @Version : 1.0
# from intersect_mp.guest import IntersectGuest
# from intersect_mp.host import IntersectHost
from intersect.guest import IntersectGuest
from intersect.host import IntersectHost

class Intersect(object):
    '''
    A class for privacy preserving entity match. Algorithm is designed according to paper
    "G. Liang and S. S. Chawathe, “Privacy-Preserving Inter-database Operations,” in Lecture Notes in Computer Science
     (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics), vol. 3073, 2004,
      pp. 66–82."
    '''
    def run(self, dataset, host_data):
        '''
        :param dataset_host: user id list from host
        :param dataset_guest: user id list from guest
        :return: intersection of their idx
        '''
        intersect_idx_raw_host_mp=[]
        n=len(dataset)
        for i in range(n):
            if host_data != dataset[i]:
                host = IntersectHost()
                guest = IntersectGuest(host.get_rsa_public_key())
                guest_idx = guest.send_guest_idx(dataset[i],i)
                guest_idx_host = host.process_guest_idx(guest_idx,i)
                host_idx = host.send_host_idx(host_data,i)
                (intersect_idx_enc, intersect_idx_raw_guest) = guest.process_host_guest_idx(host_idx, guest_idx_host,i)
                intersect_idx_raw_host = host.process_intersect_idx(intersect_idx_enc)
                print('end{}'.format(i))
                assert(intersect_idx_raw_host == intersect_idx_raw_guest)
                intersect_idx_raw_host_mp.append(intersect_idx_raw_host)
        # print(intersect_idx_raw_host_mp)
        return intersect_idx_raw_host_mp