#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-05 02:29 
from SouAng.smod import ssys, smaya
from ..functionsCollection import postion


def testFun1():
    print('Function 1')

def testFun2():
    print('Function 2')

def resetToCenterFreeze():
    postion.resetToCenterFreeze()

def resetToZero():
    postion.resetToZero()

def matchWorldPos():
    postion.matchWorldPos()

def zeroTR():
    postion.zeroTR()

def reloadAll():
    ssys.SuperReload().removeAll()


ONEKEYLIST = {
        'testFuctionscript1' : (testFun1, 'Function 1'),
        'testFuctionscript2' : (testFun2, 'Function 2'),
        'Center Freeze' : (resetToCenterFreeze, 'Reset to object center and freeze pos'),
        'Reset Zero' : (resetToZero, 'Reset to world zero'),
        'Match Pos' : (matchWorldPos, 'Match object to world pos'),
        'Reset Pos' : (zeroTR, 'Reset pos'),
        'Reload All' : (reloadAll, 'Super reload'),
        }

