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
__cpath__ = '\\'.join(__file__.split('\\')[:-1])

def intoMayaMain(win):
    win.setParent(WIN_MAYA_MAIN)

def setStyle(obj, f='main'):
    path_style_dir = __cpath__[:-4] + 'resource\\style'
    path_style_file = '%s\\%s.qss'%(path_style_dir, f)
    qfile = open(path_style_file, 'rb')
    obj.setStyleSheet(qfile.read())
    qfile.close()

def moveRelative(posMove, obj, relative=None):
    if not relative:
        relative = obj.parent()
    size_p = relative.size()
    obj.move(size_p.width()*posMove[0], size_p.height()*posMove[1])

def safeGet(val, defaultValue=0):
    if val:
        return val
    else:
        return defaultValue


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


class DragMove(object):

    def __init__(self):
        super(DragMove, self).__init__()
        self.isMousePressed = False
        self.posWhenPressed = QtCore.QPoint(0, 0)
        self.posDrviedWhenPressed = [QtCore.QPoint(0, 0)]
        self.drived = [self]

    def setDrived(self, drived):
        self.drived = drived

    def mousePressEvent(self, event):
        self.posWhenPressed = event.globalPos()
        self.posDrviedWhenPressed = map(lambda x: x.pos(), self.drived)
        self.isMousePressed = True

    def mouseReleaseEvent(self, event):
        self.isMousePressed = False

    def mouseMoveEvent(self, event):
        vector_moved = event.globalPos() - self.posWhenPressed
        for i, each in enumerate(self.drived):
            each.move(self.posDrviedWhenPressed[i]+vector_moved)


class ButtonArrayLayout(QtWidgets.QGridLayout):

    def __init__(self, info=None, lineCoun=3, dirction=0):
        super(ButtonArrayLayout, self).__init__()
        self.info = safeGet(info, 
                [
                    ('b1', self.printInfo), 
                    ('b2', self.printInfo), 
                    ('b3', self.printInfo)
                    ]
                )
        self.lineCount = 3
        # 1 vertical 0 horizontal
        self.dirction = 0
        self.build()

    def build(self):
        len_btns = len(self.info)
        list_divide = [x/self.lineCount for x in xrange(len_btns)]
        list_remainder = [x%self.lineCount for x in xrange(len_btns)]
        if self.dirction:
            col_list = list_divide
            row_list = list_remainder
        else:
            col_list = list_remainder
            row_list = list_divide
        for i in xrange(len_btns):
            btn = QtWidgets.QPushButton(self.info[i][0])
            btn.clicked.connect(self.info[i][1])
            self.addWidget(btn, row_list[i], col_list[i])

    def printInfo(self):
        print(self.sender(), self.count())


class ButtonTextLayout(QtWidgets.QHBoxLayout):
    clicked = QtCore.Signal(unicode)

    def __init__(self, button='button', slot=None, defaultText=''):
        super(ButtonTextLayout, self).__init__()
        self.button = QtWidgets.QPushButton(button)
        self.line = QtWidgets.QLineEdit(defaultText)
        self.button.clicked.connect(self.on_button_clicked)
        self.clicked.connect(safeGet(slot, self.printInfo))
        self.addWidget(self.button)
        self.addWidget(self.line)

    def on_button_clicked(self):
        self.clicked.emit(self.line.text())

    def printInfo(self, *args):
        print(self.sender(), args)
