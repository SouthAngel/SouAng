#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-20 19:43 
from maya import cmds


# Node math
def isText(inputObj):
    if isinstance(inputObj, unicode) or isinstance(inputObj, str):
        return 1
    else:
        return 0

def setOrConnect(attr1, attr2):
    if isText(attr1):
        cmds.connectAttr(attr1, attr2, f=1)
    else:
        cmds.setAttr(attr2, attr1)

def add( *args ):
    if not args:
        return ''
    node = cmds.createNode('plusMinusAverage')
    if isText(args[0]):
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
    if isText(attr1):
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

# Distance node
def distanceObjs(obj1, obj2):
    loc = (cmds.spaceLocator()[0], cmds.spaceLocator()[0])
    distance_node = cmds.createNode('distanceBetween')
    cmds.parent(loc[0], obj1)
    cmds.parent(loc[1], obj2)
    cmds.setAttr('%s.t'%loc[0], 0, 0, 0)
    cmds.setAttr('%s.t'%loc[1], 0, 0, 0)
    cmds.connectAttr('%s.worldPosition[0]'%loc[0], '%s.point1'%distance_node, f=1)
    cmds.connectAttr('%s.worldPosition[0]'%loc[1], '%s.point2'%distance_node, f=1)
    return distance_node, loc[0], loc[1]

# Constraint node
def getWorldPos(obj):
    p_node = cmds.createNode('pointConstraint')
    cmds.connectAttr('%s.translate'%obj, '%s.target[0].targetTranslate'%p_node, f=1)
    cmds.connectAttr('%s.parentMatrix'%obj, '%s.target[0].targetParentMatrix'%p_node, f=1)
    cmds.connectAttr('%s.rotatePivot'%obj, '%s.target[0].targetRotatePivot'%p_node, f=1)
    cmds.connectAttr('%s.rotatePivotTranslate'%obj, '%s.target[0].targetRotateTranslate'%p_node, f=1)
    return '%s.constraintTranslate'%p_node


if __name__ == '__main__':
    print('Run in main')
    mult(['t1.tx'], ['t2.tx'])

