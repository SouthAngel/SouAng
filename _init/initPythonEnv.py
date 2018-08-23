#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-23 16:48 
import sys
from maya import mel

def safeAddSysPath(path):
    if path not in sys.path:
        sys.path.insert(0, path)

if __name__ == "__main__":
    safeAddSysPath(mel.eval("SouAngEntrance(0)"))

