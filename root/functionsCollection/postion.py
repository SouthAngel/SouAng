#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-23 21:50 
from maya import cmds
from smod.spy import smaya

def randPos(rad=None, xyz=None):
    gen_pos = randVector(rad, xyz)
    cmds.move(gen_pos[0], gen_pos[1], gen_pos[2])
