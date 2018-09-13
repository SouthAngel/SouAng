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

def testFun3():
    print('Function 3')

def testFun4():
    print('Function 4')

def testFun5():
    print('Function 5')

def zeroTR():
    postion.zeroTR()

def reloadAll():
    ssys.SuperReload().removeAll()


ONEKEYLIST = {
        'testFuctionscript1' : (testFun1, 'Function 1'),
        'testFuctionscript2' : (testFun2, 'Function 2'),
        'testFuctionscript3' : (testFun3, 'Function 3'),
        'testFuctionscript4' : (testFun4, 'Function 4'),
        'testFuctionscript5' : (testFun5, 'Function 5'),
        'Reset Pos' : (zeroTR, 'Reset pos'),
        'Reload All' : (reloadAll, 'Super reload'),
        }

