#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-24 10:40 
import sys, os

def saSetUp(path):
    path_get = path[:-22]
    path_store_file = path_get + '/.path'
    path_get_norm = os.path.normpath(path_get)
    path_using = os.path.dirname(path_get_norm)
    if path_using not in sys.path:
        sys.path.insert(0, path_using)
    
    import SouAng
    SouAng.run(1)
