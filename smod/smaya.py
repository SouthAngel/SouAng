#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-23 23:27 
import random
from maya import cmds, mel

def randVector(rad=None, xyz=None):
    if not rad:
        rad = (-12, 12)
    if not xyz:
        xyz= (rad, rad, rad)
    mxyz = []
    for i in xyz:
        mxyz.append(random.uniform(i[0], i[1]))
    return mxyz
    
# Popup dialog Warning
def simpleWarn(message='Get some wrong!'):
    cmds.confirmDialog(title="Warn",message=message,button="OK")

def gEvalPy(script):
    return mel.eval('python("%s");'%script.replace('\n', '\\n'))
