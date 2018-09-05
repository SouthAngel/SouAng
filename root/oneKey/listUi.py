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
        self.line_search = SearchLine()
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
        self.setFixedSize(486, 184)
        sgui.setStyle(self)
        sgui.moveRelative((0.52, 0.68), self)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popMenu)
        self.line_search.textChanged.connect(self.view_list.mod.findKeys)
        print('initSet')

    def popMenu(self, pos):
        menu = QtWidgets.QMenu()
        actions = (
                ('Close', self.close),
                ('UiConfig', self.configUi),
                )
        for each in actions:
            action = QtWidgets.QAction(each[0], self)
            action.triggered.connect(each[1])
            menu.addAction(action)
        menu.exec_(self.mapToGlobal(pos))

    def configUi(self):
        print(self.size(), self.pos())

    def show(self):
        super(IndexMain, self).show()
        self.line_search.setFocus()


class SearchLine(QtWidgets.QLineEdit):

    def __init__(self):
        super(SearchLine, self).__init__()

    def focusOutEvent(self, event):
        super(SearchLine, self).focusOutEvent(event)
        self.parent().close()


class IndexListView(QtWidgets.QListView):

    def __init__(self):
        super(IndexListView, self).__init__()
        self.mod = IndexListModel()
        self.setModel(self.mod)
        self.setViewMode(self.IconMode)
        self.setMovement(self.Static)
        self.setSpacing(4)
        self.mod.findKeys('')
        self.setResizeMode(self.Adjust)
#         self.setGridSize(QtCore.QSize(32, 32))
        self.clicked.connect(self.on_clicked)

    def on_clicked(self, index):
        self.mod.included[index.data()][0]()


class IndexListModel(QtGui.QStandardItemModel):

    def __init__(self):
        super(IndexListModel, self).__init__()
        self.dict_config = functions.ONEKEYLIST
        self.included = {}

    def update(self):
        self.clear()
        brush_bg = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        for each in self.included.iterkeys():
            item = QtGui.QStandardItem(each)
            item.setToolTip(self.included[each][1])
            item.setSelectable(0)
            item.setBackground(brush_bg)
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
