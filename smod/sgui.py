#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-28 20:27 
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from shiboken2 import wrapInstance


WIN_MAYA_MAIN = wrapInstance(long(mui.MQtUtil.mainWindow()), QtWidgets.QMainWindow)


def intoMayaMain(win):
    win.setParent(WIN_MAYA_MAIN)


class VeiwPlus(QtWidgets.QAbstractItemView):

    def __init__(self):
        super(ModelVeiwPlus, self).__init__()

    @staticmethod
    def findIndexSibling(index, col):
        return index.sibling(index.row(), col)

    def selectedContent(self, lineOne=-1):
        sel = self.selectedIndexes()
        if lineOne == -1:
            return map(lambda x: x.data(), sel)
        else:
            return self.findIndexSibling(sel[0], lineOne).data()

