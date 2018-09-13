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
