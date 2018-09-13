#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-08 09:17 
from maya import cmds
from smod import smaya


ATTR_TRS = (
        'translateX', 'translateY', 'translateZ',
        'rotateX', 'rotateY', 'rotateZ',
        'scaleX', 'scaleY', 'scaleZ',
        )


def randPos(rad=None, xyz=None):
    gen_pos = randVector(rad, xyz)
    cmds.move(gen_pos[0], gen_pos[1], gen_pos[2])

def zeroTR():
    sel = smaya.Sel().toTransform()
    for each in iter(sel):
        for i in xrange(6):
            cmds.setAttr('%s.%s'%(each, ATTR_TRS[i]), 0)

def resetToCenterFreeze():
    sel = cmds.ls(sl=1)
    for each in iter(sel):
        cmds.xform(each, cpc=1)
        cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)

def resetToZero():
    sel = cmds.ls(sl=1)
    for each in iter(sel):
        cmds.xform(each, ws=1, rp=[0, 0, 0], sp=[0, 0, 0])
        cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)

def matchWorldPos():
    sel = cmds.ls(sl=1)
    len_sel = len(sel)
    if len_sel > 1:
        end_sel = sel[len_sel-1]
        for i in xrange(len_sel-1):
            cmds.delete(cmds.parentConstraint(end_sel, sel[i], mo=0))

if __name__ == '__main__':
    print('Run in main')
    matchWorldPos()
