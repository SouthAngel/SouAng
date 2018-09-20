#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-20 22:01 
from maya import cmds
from SouAng.smod import smaya
from SouAng.root.rig import nodeMath

def distanceObjs(obj1, obj2):
    loc = (cmds.spaceLocator(), cmds.spaceLocator())
    distance_node = cmds.createNode('distanceBetween')
    cmds.parent(loc[0], obj1)
    cmds.parent(loc[1], obj2)
    cmds.setAttr('%s.t'%loc[0], 0, 0, 0)
    cmds.setAttr('%s.t'%loc[1], 0, 0, 0)
    cmds.connectAttr('%s.worldPosition[0]'%los[0], '%s.point1'%distance_node, f=1)
    cmds.connectAttr('%s.worldPosition[1]'%los[1], '%s.point2'%distance_node, f=1)
    return distance_node, loc[0], loc[1]

def ikStretch():
    sel = cmds.ls(sl=1)
    if len(sel) < 2:
        return 0
    ik_con = sel[0]
    getJoints = smaya.filterType(cmds.listHistory(sel[1], ac=1), 'joint')
    if len(getJoints) != 3:
        return 0
    baseAttr = ('upBaseDistance', 'downBaseDistance')
    joints = (getJoints[0], getJoints[2], getJoints[1])
    cmds.addAttr(ik_con, ln=baseAttr[0], at='double', dv=cmds.getAttr('%s.tx'%joints[1]))
    cmds.addAttr(ik_con, ln=baseAttr[1], at='double', dv=cmds.getAttr('%s.tx'%joints[2]))
    length_node = nodeMath.add('%s.%s'%(ik_con, baseAttr[0], '%s.%s'%(ik_con, baseAttr[1])))
    print(joints)
    

def runThis():
    ikStretch()
    print('Run in test file!')

if __name__ == '__main__':
    print('Run in main')
    runThis()
