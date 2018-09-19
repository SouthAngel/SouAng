#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-19 15:03 
from PySide2 import QtWidgets, QtGui, QtCore
from SouAng.smod import sgui

class RigUi(QtWidgets.QDialog):

    def __init__(self):
        super(RigUi, self).__init__(sgui.WIN_MAYA_MAIN)
        self.initSet()

    def initSet(self):
        lo = QtWidgets.QVBoxLayout()
        lo.addLayout(self.addButtons)
        lo.addLayout(sgui.ButtonTextLayout())
        self.setLayout(lo)

    def addButtons(self):
        return sgui.ButtonArrayLayout()

