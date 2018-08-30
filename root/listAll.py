#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-08-30 23:29 
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
        self.setWindowTitle(u'Tools')


class ListTreeView(QtWidgets.QTreeView):

    def __init__(self):
        super(ListTreeView, self).__init__()
        self.setModel(ListMod())
        self.buildAll()
        self.setSelectionMode(self.SingleSelection)
        self.setSelectionBehavior(self.SelectRows)
        self.setAnimated(1)
        self.setIndentation(4)
#         self.header().hide()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.clicked.connect(self.on_clicked)
        self.customContextMenuRequested.connect(self.on_right_clicked)
        self.doubleClicked.connect(self.on_double_clicked)

    def hideColumns(self, list_col):
        for i in iter(list_col):
            self.hideColumn(i)
    
    @property
    def selectedContents(self):
        return map(lambda x: x.data(), self.selectedIndexes())

    def on_clicked(self):
        print('Click')

    def on_double_clicked(self):
        print(self.selectedContents)
        print('Double click')

    def on_right_clicked(self, cursorPos):
        list_content = (
                ('Open', self.tpr),
                ('Add favorite', self.tpr),
                ('To shelf', self.tpr),
                )
        menu = QtWidgets.QMenu(self)
        for each in list_content:
            action = QtWidgets.QAction(each[0], self)
            action.toggled.connect(each[1])
            menu.addAction(action)
        menu.exec_(self.mapToGlobal(cursorPos)+QtCore.QPoint(0, 22))

    def buildAll(self, *args):
        self.model().update()
        # Hide ID
        self.hideColumn(3)
        self.expandAll()

    def tpr(self, *args):
        print(self.sender())
        print(args)


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
        def initItem(item=None):
            item_w = QtGui.QStandardItem()
            if item:
                item_w.setText(item)
            item_w.setEditable(False)
            return item_w
        def fillLineItem(item=None, fill=6):
            list_res = [initItem() for i in xrange(fill-1)]
            if item:
                list_res.insert(0, item)
            else:
                list_res.insert(0, initItem())
            return list_res
        def resortList(list_num, list_input):
            return [list_input[i] for i in list_num]
        self.clear()
        pluginListParser.checkUpdata()
        db = pluginListParser.PluginData()
        line_root = fillLineItem(initItem('Root'))
        stuct_grp = {'root': line_root[0]}
        self.appendRow(line_root)
        for line in db.outputAll():
            # line (ID, NAME, NAME_CN, NAME_PATH, COMMAND, DESCRIPTION, ICON_PATH)
            #      (0 , 1   , 2      , 3        , 4      , 5          , 6        )
            list_split = line[3].split(pluginListParser.ParseXml.MARK_SPLIT_XPATH)
            list_split.pop()
            len_x = len(list_split)
            list_grps = [pluginListParser.ParseXml.MARK_SPLIT_XPATH.join(list_split[:i+1]) for i in xrange(len_x)]
            if list_grps[-1] not in stuct_grp:
                for i in xrange(1, len_x):
                    if list_grps[i] not in stuct_grp:
                        item_grp = fillLineItem(initItem(list_split[i]))
                        stuct_grp[list_grps[i]] = item_grp[0]
                        stuct_grp[list_grps[i-1]].appendRow(item_grp)
            line_plugin = []
            for each in resortList((1, 2, 6, 0), line):
                item_col = initItem()
                if not isinstance(each, unicode):
                    each = unicode(each)
                item_col.setText(each)
                line_plugin.append(item_col)
            stuct_grp[list_grps[-1]].appendRow(line_plugin)
        print('update')


SWIN = ListMainWin()


if __name__ == '__main__':
    SWIN.show()
