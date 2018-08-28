#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-28 20:27 
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


WIN_MAYA_MAIN = wrapInstance(long(mui.MQtUtil.mainWindow()), QtWidgets.QMainWindow)


def intoMayaMain(win):
    win.setParent(WIN_MAYA_MAIN)
