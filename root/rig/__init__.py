
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-19 15:03 
from PySide2 import QtWidgets, QtGui, QtCore
from SouAng.smod import sgui
from . import scmds, component

class RigUi(QtWidgets.QDialog):

    def __init__(self):
        super(RigUi, self).__init__(sgui.WIN_MAYA_MAIN)
        self.initSet()

    def initSet(self):
        lo = QtWidgets.QVBoxLayout()
        lo.addLayout(self.addButtons())
        lo.addLayout(self.addButtonLines())
        lo.addLayout(component.AttrConnect())
        self.setLayout(lo)
        self.setWindowTitle('SouAng Rigging Tool')

    def addButtons(self):
        return sgui.ButtonArrayLayout(scmds.BUTTON_LIST)

    def addButtonLines(self):
        lo = QtWidgets.QGridLayout()
        parallel_num = 2
        for n, each in enumerate(scmds.BUTTONLINE_LIST):
            bl = sgui.ButtonTextLayout(each[0], each[1], each[2])
            lo.addLayout(bl, n/parallel_num, n%parallel_num)
        return lo


SAWIN = None

def show():
    global SAWIN
    if not SAWIN:
        SAWIN = RigUi()
    SAWIN.show()
