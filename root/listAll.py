#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-27 14:17 
from PySide2 import QtWidgets, QtGui, QtCore
from SouAng.smod import sgui


class ListMainWin(QtWidgets.QDialog):

    def __init__(self):
        super(ListMainWin, self).__init__()
        self.layout_m = QtWidgets.QHBoxLayout()
        self.setInit()

    def setInit(self):
        sgui.intoMayaMain(self)


class ListTreeView(QtWidgets.QTreeView):

    def __init__(self):
        super(ListTreeView, self).__init__()
        self.customContextMenuRequested.connect(self.on_right_clicked)

    def on_right_clicked(self):
        print('on_right_clicked')


SWIN = ListMainWin()


if __name__ == '__main__':
    SWIN.show()
