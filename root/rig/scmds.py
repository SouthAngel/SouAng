#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-19 17:11 
from maya import cmds
import pymel.core as pm
from ..functionsCollection import postion


def buttonF1():
    print('F1')

def buttonF2():
    print('F2')

def buttonF3():
    print('F3')

def buttonlF1(text):
    print('F1', text)

def buttonlF2(text):
    print('F2', text)

def buttonlF3(text):
    print('F3', text)



BUTTON_LIST = (
        ('Zero Postion', postion.zeroTR, ''),
        ('Center And Freeze', postion.resetToCenterFreeze, ''),
        ('World Center And Freeze', postion.resetToZero, ''),
        ('Zero Postion', postion.zeroTR, ''),
        ('Zero Postion', postion.zeroTR, ''),
        ('Zero Postion', postion.zeroTR, ''),
        )
BUTTONLINE_LIST = (
        ('F1', buttonlF1, ''),
        ('F2', buttonlF2, ''),
        ('F3', buttonlF3, ''),
        )
