#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-27 09:21 
from maya import cmds, mel
from SouAng.smod import ssys

# Bind to mel command
class BindObj(object):

    def reloadAll(self):
        ssys.SuperReload().removeAll()

    def testPrint(self):
        print("Test function")


# Bind method
def bindGlobalMel():
    print('Begin bind Mel')
    def bindScript(script_mel, script_py):
        mel.eval('global proc %s(){python("import SouAng.root.bindGlobalMel as bind\\nbind.BindObj().%s()");}'%(script_mel, script_py))
    for each in filter(lambda x: x[:2] != '__', BindObj.__dict__.keys()):
        print('Bind %s'%each)
        bindScript(each, each)
