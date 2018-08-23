#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-23 21:50 
from maya import cmds
from smod.spy import smaya

def randPos(rad=None, xyz=None):
    rand_vector = smaya.randVector(rad, xyz)
    cmds.move(rand_vector[0], rand_vector[1], rand_vector[2])
