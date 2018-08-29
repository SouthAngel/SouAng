#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-26 19:13 
from maya import cmds
from SouAng.smod import ssys


# Menu command
def refresh():
    ssys.SuperReload().removeAll()
    import SouAng
    SouAng.run()

def listAllShow():
    import SouAng.root.listAll as listA
    listA.SWIN.show()

class InitUi(object):
    NAME_LABEL = 'SouAng'
    NAME_MENU = 'SouAngMenu'
    NAME_SHELF = 'SouAngShelf'
    LIST_MENUS = (
            ('listAllShow', 'Tools List'),
            ('', 'Tools Find'),
            ('', 'Collection'),
            ('refresh', 'Refresh'),
            )
    LIST_SHELF = (
            ('', 'List'),
            ('', 'Find'),
            ('', 'Collection'),
            ('refresh', 'Refresh'),
            )

    def __init__(self):
        super(InitUi, self).__init__()

    @staticmethod
    def wrapIm(scrpit):
        return 'import SouAng.root.smenuSet as SouAngm\nSouAngm.%s()'%scrpit

    def buildMenu(self):
        mMenuLayout = 'MayaWindow'
        cmds.setParent(mMenuLayout)
        if cmds.menu(self.NAME_MENU, q=1, ex=1):
            cmds.deleteUI(self.NAME_MENU)
        cmds.menu(self.NAME_MENU, to=1, l=self.NAME_LABEL)
        for menu in self.LIST_MENUS:
            cmds.menuItem(c=self.wrapIm(menu[0]), l=menu[1])
        print('buildMenu')

    def buildShelf(self):
        if not cmds.shelfLayout(self.NAME_LABEL, ex=1):
            shelfTab = 'ShelfLayout'
            cmds.setParent(shelfTab)
            cmds.shelfLayout(self.NAME_LABEL)
            for menu in self.LIST_SHELF:
                cmds.shelfButton(c=self.wrapIm(menu[0]), l=menu[1], iol=menu[1], i='123d.png')
        print('buildShelf')
