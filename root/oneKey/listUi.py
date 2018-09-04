#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-04 22:04 
import copy
from PySide2 import QtWidgets, QtGui, QtCore
from SouAng.smod import sgui
from . import functions


class IndexMain(sgui.DragMove, QtWidgets.QFrame):

    def __init__(self):
        super(IndexMain, self).__init__()
        self.view_list = IndexListView()
        self.line_search = QtWidgets.QLineEdit()
        sgui.intoMayaMain(self)
        self.initSet()

    def initSet(self):
        lo = QtWidgets.QVBoxLayout()
        lo.addWidget(self.line_search)
        lo.addWidget(self.view_list)
        self.setLayout(lo)
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


class IndexListView(QtWidgets.QListView):

    def __init__(self):
        super(IndexListView, self).__init__()
        self.setModel(IndexListModel())
        self.setViewMode(self.IconMode)
        self.setMovement(self.Static)
        self.setSpacing(4)
#         self.setGridSize(QtCore.QSize(32, 32))


class IndexListModel(QtGui.QStandardItemModel):

    def __init__(self):
        super(IndexListModel, self).__init__()
        self.dict_config = functions.ONEKEYLIST
        self.included = {}
        self.findKeys('')

    def update(self):
        self.clear()
        for each in self.included.iterkeys():
            item = QtGui.QStandardItem(each)
            self.appendRow(item)
        print('update')

    def findKeys(self, keyWord):
        self.included.clear()
        if keyWord:
            for k, v in self.dict_config.iteritems():
                if k.startswith(keyWord):
                    self.included[k] = v
        else:
            self.included = copy.deepcopy(self.dict_config)
        self.update()
