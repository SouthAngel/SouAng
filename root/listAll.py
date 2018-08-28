#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-27 14:17 
from PySide2 import QtWidgets, QtGui, QtCore
from SouAng.smod import sgui
from SouAng.root import pluginListParser


class ListMainWin(QtWidgets.QDialog):

    def __init__(self):
        super(ListMainWin, self).__init__(sgui.WIN_MAYA_MAIN)
        self.layout_m = QtWidgets.QHBoxLayout()
        self.view_tree = ListTreeView()
        self.setInit()

    def setInit(self):
        self.layout_m.addWidget(self.view_tree)
        self.setLayout(self.layout_m)


class ListTreeView(QtWidgets.QTreeView):

    def __init__(self):
        super(ListTreeView, self).__init__()
        self.setModel(ListMod())
        self.header().hide()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_right_clicked)

    def on_right_clicked(self, *args):
        self.model().test()
        print('on_right_clicked', args)


class ListMod(QtGui.QStandardItemModel):

    def __init__(self):
        super(ListMod, self).__init__()

    def test(self):
        for row in xrange(10):
            for col in xrange(3):
                item = QtGui.QStandardItem()
                item.setText('row_%s>col_%s'%(row, col))
                self.setItem(row, col, item)
        print('test')

    def update(self):
        self.clear()
        pluginListParser.checkUpdata()
        db = pluginListParser.PluginData()
        stuct_grp = {'root': QtGui.QStandardItem('root')}
        self.setItem(stuct_grp['root'])
        for line in db.outputAll():
            if line[3] not in stuct_grp:
                list_split = xpath.split(pluginListParser.ParseXml.MARK_SPLIT_XPATH).pop()
                len_x = len(list_split)
                list_grps = [pluginListParser.ParseXml.MARK_SPLIT_XPATH.join(list_split[:i+1]) for i in xrange(len_x)]
                for i in xrange(1, len_x):
                    if list_grps[i] not in stuct_grp:
                        item_grp = QtGui.QStandardItem(list_split[i])
                        stuct_grp[list_split[i]] = item_grp
                        stuct_grp[list_split[i-1]].appendRow(item_grp)
                
        print('update')


SWIN = ListMainWin()


if __name__ == '__main__':
    SWIN.show()
