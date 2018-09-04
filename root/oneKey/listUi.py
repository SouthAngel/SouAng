#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-04 22:04 
from PySide2 import QtWidgets, QtGui, QtCore
from SouAng.smod import sgui


class IndexMain(sgui.DragMove, QtWidgets.QFrame):

    def __init__(self):
        super(IndexMain, self).__init__()
        sgui.intoMayaMain(self)
        self.initSet()

    def initSet(self):
        self.setDrived([self])
        self.setFrameShape(self.Panel)
        self.setFrameShadow(self.Sunken)
        self.setObjectName('testGreen')
        sgui.setStyle(self)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popMenu)
        print('initSet')

    def popMenu(self, pos):
        menu = QtWidgets.QMenu()
        actions = (
                ('Close', self.close),
                )
        for each in actions:
            action = QtWidgets.QAction(each[0], self)
            action.triggered.connect(each[1])
            menu.addAction(action)
        menu.exec_(self.mapToGlobal(pos))

    def keyReleaseEvent(self, event):
        self.close()
        print("%s is tab in"%event.text())

    def keyPressEvent(self, event):
        self.close()
        print("%s is tab in"%event.text())
