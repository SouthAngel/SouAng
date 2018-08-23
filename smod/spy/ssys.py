#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-23 16:48 
import sys, re


# Path add for sys
def safeAddSysPath(path):
    if path not in sys.path:
        sys.path.insert(0, path)

# Path deal
def splitPath_(path):
    return re.findall(r'[^:\\/\.]+', path)

def splitPath(path, n=-1):
    return splitPath_(path)[n]

def splitPathEx(path, s=-2, e=-1):
    list_path_split = splitPath_(path)
    list_s_split = re.findall(r'[:\\/\.]+', path)
    len_block = len(list_path_split)
    if s < 0:
        s += len_block
    if e < 0:
        e += len_block
    path_res = ''
    for i in xrange(s, e):
        if i != e-1:
            path_res += list_path_split[i] + list_s_split[i]
        else:
            path_res += list_path_split[i]
    return path_res

# Tool path
TOOLNAME= 'SouAng'

def toolPathUnder_():
    return __file__.split(TOOLNAME)[0]

def toolPathUnder():
    return toolPathUnder_()[:-1]

def toolPath():
    return toolPathUnder_() + TOOLNAME


def toolPath():
    return toolPathUnder_() + '.' + TOOLNAME

# Try decorator
def trywarp( fun ):
    def _mid( *args, **kwargs ):
        try:
            res_fun = fun( args, kwargs )
            return res_fun
        except Exception as e:
            print(str(e))
            raise RuntimeError(e)
    return _mid
