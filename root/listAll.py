#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-27 14:17 
import time

def testSpeed():
    list_t = []
    dict_t= {}
    index_pos = 500000
    for i in xrange(1000000):
        list_t.append('value_%s'%i)
        dict_t['key_%s'%i] = 'value_%s'%i
    lc_b = time.time()
    for j in xrange(500):
        rs = list_t[index_pos]
#         rs = 'value_%s'%index_pos in list_t
    lc_e = time.time()
    print(rs)
    print('listTime: %s'%(lc_e-lc_b))
    ld_b = time.time()
    for j in xrange(500):
        rs = dict_t['key_%s'%index_pos]
#         rs = 'key_%s'%index_pos in dict_t
    ld_e = time.time()
    print(rs)
    print('dictTime: %s'%(ld_e-ld_b))

if __name__ == '__main__':
    testSpeed()
