#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-24 10:02 
from SouAng.smod import ssys
ssys.SuperReload().store()
from SouAng.root import smenuSet

def startWithLevel():
    user_set_config = ssys.Gconfig().read()
    start_level = user_set_config['start_level']
    if start_level == 0:
        return 0
    if start_level == 1:
        return 1
    initUi = smenuSet.InitUi()
    initUi.buildMenu()
    if start_level == 2:
        return 2
    initUi.buildShelf()
    if start_level == 3:
        return 3

def reloadAll():
    ssys.SuperReload().removeAll()

def run():
    startWithLevel()
