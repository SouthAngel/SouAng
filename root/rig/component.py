#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-20 08:35 
from PySide2 import QtWidgets, QtGui, QtCore
from maya import cmds


class LineWhenIn(QtWidgets.QLineEdit):
    focusIn = QtCore.Signal()

    def __init__(self):
        super(LineWhenIn, self).__init__()

    def focusInEvent(self, event):
        super(LineWhenIn, self).focusInEvent(event)
        self.focusIn.emit()


class AttrConnect(QtWidgets.QHBoxLayout):

    def __init__(self):
        super(AttrConnect, self).__init__()
        self.button = QtWidgets.QPushButton('C')
        self.button.setFixedSize(28, 28)
        self.button.clicked.connect(self.on_button_clicked)
        self.attrF = LineWhenIn()
        self.attrL = LineWhenIn()
        self.attrF.focusIn.connect(self.on_L_focusIn)
        self.attrL.focusIn.connect(self.on_R_focusIn)
        self.addWidget(self.attrF)
        self.addWidget(self.button)
        self.addWidget(self.attrL)
        self.setSpacing(1)

    def on_button_clicked(self):
        sel = cmds.ls(sl=1)
        if len(sel) > 1:
            cmds.connectAttr('%s.%s'%(sel[0], self.attrF.text()), '%s.%s'%(sel[1], self.attrL.text()), f=1)

    def on_L_focusIn(self):
        self.attrF.setCompleter(self.getCompleter(0))

    def on_R_focusIn(self):
        self.attrL.setCompleter(self.getCompleter(1))

    @staticmethod
    def getCompleter(fOrl=0):
        sel = cmds.ls(sl=1)
        if len(sel) < fOrl+1:
            completer_list = []
        else:
            completer_list = cmds.listAttr(sel[fOrl], m=1)
        completer = QtWidgets.QCompleter(completer_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        return completer

if __name__ == '__main__':
    print('Run in main')
    TESTWIN = QtWidgets.QDialog()
    TESTWIN.setLayout(AttrConnect())
    TESTWIN.show()
