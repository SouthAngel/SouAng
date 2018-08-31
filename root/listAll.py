#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-08-30 23:29 
from PySide2 import QtWidgets, QtGui, QtCore
from SouAng.smod import sgui, smaya
from SouAng.root import pluginListParser


class ListMainWin(QtWidgets.QDialog):

    def __init__(self):
        super(ListMainWin, self).__init__(sgui.WIN_MAYA_MAIN)
        self.layout_m = QtWidgets.QHBoxLayout()
        self.area_display = PorpertyDisplay()
        self.view_tree = ListTreeView(self.area_display)
        self.setInit()

    def setInit(self):
        self.layout_m.addWidget(self.view_tree)
        self.layout_m.addWidget(self.area_display)
        self.setLayout(self.layout_m)
        self.setWindowTitle(u'Tools')


class ListTreeView(QtWidgets.QTreeView, sgui.VeiwPlus):

    def __init__(self, area_display):
        super(ListTreeView, self).__init__()
        self.area_display = area_display
        self.setModel(ListMod())
#         self.setItemDelegate(ListDelegate())
        self.buildAll()
        self.setSelectionMode(self.SingleSelection)
        self.setSelectionBehavior(self.SelectRows)
        self.setAnimated(1)
        self.setIndentation(6)
        self.header().hide()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.clicked.connect(self.on_clicked)
        self.customContextMenuRequested.connect(self.on_right_clicked)
        self.doubleClicked.connect(self.on_double_clicked)

    def buildAll(self, *args):
        self.model().update()
        # Hide ID
        self.hideColumns((1, 2, 3, 4, 5))
        self.expandAll()

    def hideColumns(self, list_col):
        for i in iter(list_col):
            self.hideColumn(i)
    
    # Slot method
    def on_clicked(self):
        if self.area_display.isHidden():
            self.area_display.show()
        print('Click')

    def on_double_clicked(self):
        item_first = self.model().itemFromIndex(self.selectedIndexes()[0])
        print(self.size())
        if not item_first.hasChildren():
            print(self.selectedContent(1))
            print('Item')

    def on_right_clicked(self, cursorPos):
        list_content = (
                ('Open', self.on_open_pop),
                ('Add favorite', self.tpr),
                ('To shelf', self.tpr),
                )
        menu = QtWidgets.QMenu(self)
        for each in list_content:
            action = QtWidgets.QAction(each[0], self)
            action.triggered.connect(each[1])
            menu.addAction(action)
        menu.exec_(self.mapToGlobal(cursorPos))

    def on_open_pop(self):
        smaya.gEvalPy(self.selectedContent(4))

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
            for each in line:
                item_col = initItem()
                if not isinstance(each, unicode):
                    each = unicode(each)
                item_col.setText(each)
                line_plugin.append(item_col)
            line_plugin[0].setText('%s  %s'%(line[1], line[2]))
            line_plugin[2].setText(unicode(line[0]))
            line_plugin.append(QtGui.QStandardItem('item'))
            # line (NAME  NAME_CN, NAME, ID, NAME_PATH, COMMAND, DESCRIPTION, ICON_PATH, item or grp)
            #      (0            , 1   , 2 , 3        , 4      , 5          , 6        ,  7)
            stuct_grp[list_grps[-1]].appendRow(line_plugin)
        print('update')


class ListDelegate(QtWidgets.QItemDelegate):

    def __init__(self):
        super(ListDelegate, self).__init__()

    @staticmethod
    def splitRect(rect, splitPos=[]):
        if not splitPos:
            return rect
        rect_l = rect.getRect()
        splitPos.insert(0, 0)
        splitPos.append(rect_l[2])
        list_res = []
        for i in xrange(1, len(splitPos)):
            list_res.append(QtCore.QRect(rect_l[0]+splitPos[i]-splitPos[i-1], rect_l[1], splitPos[i], rect_l[3]))
        print(list_res)
        return list_res

    def paint(self, painter, option, index):
        if index.column() == 0 and sgui.VeiwPlus.findIndexSibling(index, 7).data() == 'item':
            painter.setBrush(QtGui.QBrush(QtGui.QColor(99, 0, 0)))
            rect_l = option.rect.getRect()
#             painter.fillRect(option.rect, QtGui.QColor(0, 0, 26))
#             painter.drawText(option.rect, index.data())
            data_name = sgui.VeiwPlus.findIndexSibling(index, 1).data()
            data_name_cn = sgui.VeiwPlus.findIndexSibling(index, 2).data()
            if data_name_cn:
                text_draw = '%s  %s'%(data_name, data_name_cn)
            else:
                text_draw = data_name
            option.rect.moveLeft(option.rect.left()+option.rect.height())
            painter.drawText(option.rect, text_draw)
            return 1
        super(ListDelegate, self).paint(painter, option, index)

    def sizeHint(self, option, index):
        initSize = super(ListDelegate, self).sizeHint(option, index)
        initSize.setHeight(24)
        return initSize


class PorpertyDisplay(QtWidgets.QWidget):

    def __init__(self):
        super(PorpertyDisplay, self).__init__()
        self.setFixedSize(155, 251)

    def update(self):
        print('update')

    def setIcon(self):
        print('setIcon')

    def setName(self):
        print('setName')

    def setNameCn(self):
        print('setNameCn')

    def setGroup(self):
        print('setGroup')

    def setCommand(self):
        print('setCommand')

    def paintEvent(self, event):
        print('OoOo')


SWIN = ListMainWin()


if __name__ == '__main__':
    SWIN.show()
