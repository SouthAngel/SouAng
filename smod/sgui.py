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

def setStyle(obj, f='main'):
    path_style_dir = __file__[:-12] + 'resource\\style'
    path_style_file = '%s\\%s.qss'%(path_style_dir, f)
    qfile = open(path_style_file, 'rb')
    obj.setStyleSheet(qfile.read())
    qfile.close()

def moveRelative(posMove, obj, relative=None):
    if not relative:
        relative = obj.parent()
    size_p = relative.size()
    obj.move(size_p.width()*posMove[0], size_p.height()*posMove[1])


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
