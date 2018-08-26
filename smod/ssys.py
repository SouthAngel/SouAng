#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-23 16:48 
import sys
import os
import re
import cPickle
import importlib


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


# Store path
class StorePath(object):
    TOOLNAME = 'SouAng'
    FOLDER_NEAM_TEMP = '.' + TOOLNAME
    SYS_MOD = os.path.dirname(__file__)
    TOOL = __file__.split(TOOLNAME)[0] + TOOLNAME
    TOOL_PARENT = __file__.split(TOOLNAME)[0][:-1]
    TEMP = os.path.join(TOOL_PARENT, FOLDER_NEAM_TEMP)


# Super reload
class SuperReload(object):
    FILE_NAME = 'modules.rel'

    def __init__(self, path_file=None):
        super(SuperReload, self).__init__()
        self.file = os.path.join(StorePath.TEMP, self.FILE_NAME)
        if path_file:
            self.file = path_file

    def store(self):
        if not os.path.isdir(StorePath.TEMP):
            os.mkdir(StorePath.TEMP)
        with open(self.file, 'wb') as opf:
            cPickle.dump(sys.modules.keys(), opf)

    def removeAll(self):
        if not os.path.isfile(self.file):
            raise RuntimeError("Initialize has not store using modules!")
        with open(self.file, 'rb') as opf:
            mod_keys = cPickle.load(opf)
        for k in sys.modules.keys():
            if k not in mod_keys:
                del sys.modules[k]
                print("Remove <%s>"%k)

    @staticmethod
    def reload(k_m, reg=0):
        dic_mods = sys.modules
        if reg:
            for k in dic_mods.keys():
                if re.match(k_m, k):
                    reload(dic_mods[k])
                    print('Reload <%s>'%k)
        else:
            if k_m in dic_mods.keys():
                reload(dic_mods[k_m])
                print('Reload <%s>'%k)
            else:
                print('Not found <%s> in modules'%k_m)


# Gloabl config file parsing
class Gconfig(object):
    FILE_NAME = '.config'
    file = os.path.join(StorePath.TOOL, FILE_NAME)
    CONFIG = {}

    def __init__(self):
        super(Gconfig, self).__init__()

    def read(self):
        config_fp = open(self.file, 'rb')
        iter_read = config_fp.readline()
        while iter_read:
            self.parsLine(iter_read)
            iter_read = config_fp.readline()
        config_fp.close()
        return self.CONFIG

    def parsLine(self, line):
        line = line.strip()
        if not line.startswith("#"):
            split_ = line.split("=")
            if len(split_) == 2:
                split_ = map(lambda x: x.strip(), split_)
                self.CONFIG[split_[0]] = split_[1]

