#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-20 19:43 
from maya import cmds


def setOrConnect(attr1, attr2):
    if isinstance(attr1, str):
        cmds.connectAttr(attr1, attr2, f=1)
    else:
        cmds.setAttr(attr2, attr1)

def add( *args ):
    if not args:
        return ''
    node = cmds.createNode('plusMinusAverage')
    if isinstance(args[0], str):
        ele_num = 1
    else:
        ele_num = len(args[0])
    for i in xrange(len(args)):
        if ele_num == 1:
            attr = '%s.input1D[%s]'%(node, i)
            setOrConnect(args[i], attr)
        else:
            attr = '%s.input%sD[%s]'%(node, ele_num, i)
            setOrConnect(args[i], attr)
    return node

def sub( *args ):
    plus_m = add(*args)
    cmds.setAttr('%s.operation'%plus_m, 2)
    return plus_m

def ave( *args ):
    plus_m = add(*args)
    cmds.setAttr('%s.operation'%plus_m, 3)
    return plus_m

def mult(attr1, attr2):
    node = cmds.createNode('multiplyDivide')
    if isinstance(attr1, str):
        setOrConnect(attr1, '%s.input1'%node)
        setOrConnect(attr2, '%s.input2'%node)
    else:
        ele_info = 'XYZ'
        for i in xrange(len(attr1)):
            setOrConnect(attr1[i], '%s.input1%s'%(node, ele_info[i]))
            setOrConnect(attr2[i], '%s.input2%s'%(node, ele_info[i]))
    return node

def div(attr1, attr2):
    node = mult(attr1, attr2)
    cmds.setAttr('%s.operation'%node, 2)
    return node
    
def pow(attr1, attr2):
    node = mult(attr1, attr2)
    cmds.setAttr('%s.operation'%node, 2)
    return node


if __name__ == '__main__':
    print('Run in main')
    mult(['t1.tx'], ['t2.tx'])

