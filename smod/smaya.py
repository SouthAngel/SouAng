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

# Node and attribute
def splitAttrName(name_attr):
    pos_dot = name_attr.find('.')
    return name_attr[:pos_dot], name_attr[pos_dot+1:]

def mAttr(node, attr):
    return '%s.%s'%(node, attr)


# selected
class Sel(object):

    def __init__(self, list_sel=None):
        super(Sel, self).__init__()
        if list_sel:
            self.sel = list_sel
        else:
            self.sel = cmds.ls(sl=1)

    def toTransform(self):
        res = []
        for each in iter(self.sel):
            if cmds.nodeType(each) == 'transform':
                res.append(each)
            else:
                res.extend(cmds.listRelatives(each, p=1))
        return res

    def toShape(self, inm=0):
        res = []
        for each in iter(self.sel):
            if cmds.nodeType(each) == 'mesh':
                res.append(each)
            else:
                res.extend(cmds.listRelatives(each, ad=1, type='mesh'))
        if inm:
            res = self.filterIn(res)
        return res

    @staticmethod
    def filterIn(objs):
        return filter(lambda x: cmds.getAttr('%s.intermediateObject'%x) != 1, objs)


