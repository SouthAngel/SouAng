#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-20 15:41 
from maya import cmds
import pymel.core as pm


class JointSetIkFk(object):
    IKFKATTR = 'IKFK'

    def __init__(self):
        super(JointSetIkFk, self).__init__()
        self.ikfk_c = None
        self.ikfkAttr = self.IKFKATTR
        self.origin_j = [None for i in xrange(3)]
        self.ik_j = [None for i in xrange(3)]
        self.fk_j = [None for i in xrange(3)]

    @staticmethod
    def getFromParent(obj, valueArray):
        if not obj:
            return 0
        valueArray[0] = obj
        sec_j = cmds.listRelatives(obj, c=1, f=1)
        if not obj:
            return 0
        valueArray[1] = sec_j[0]
        thi_j = cmds.listRelatives(sec_j[0], c=1, f=1)
        if not obj:
            return 0
        valueArray[2] = thi_j[0]
        return 1

    def jjjIkFkSet(self, text):
        sel = cmds.ls(sl=1)
        if not sel:
            return 0
        if len(sel) < 4:
            return 0
        self.ikfk_c = sel[0]
        self.ikfkAttr = text
        if not self.getFromParent(sel[1], self.origin_j):
            return 0
        if not self.getFromParent(sel[2], self.ik_j):
            return 0
        if not self.getFromParent(sel[3], self.fk_j):
            return 0
        fkwn = cmds.createNode('multiplyDivide')
        ikwn = cmds.createNode('plusMinusAverage')
        cmds.connectAttr('%s.%s'%(self.ikfk_c, self.ikfkAttr), '%s.input1X'%fkwn)
        cmds.setAttr('%s.input2X'%fkwn, 0.1)
        cmds.setAttr('%s.input1D[0]'%ikwn, 1)
        cmds.setAttr('%s.operation'%ikwn, 2)
        cmds.connectAttr('%s.outputX'%fkwn, '%s.input1D[1]'%ikwn, f=1)
        for i in xrange(3):
            self.shareWeight(self.origin_j[i], self.ik_j[i], self.fk_j[i], 
                    '%s.output1D'%ikwn, '%s.outputX'%fkwn, 'translate')
            self.shareWeight(self.origin_j[i], self.ik_j[i], self.fk_j[i], 
                    '%s.output1D'%ikwn, '%s.outputX'%fkwn, 'rotate')

    @staticmethod
    def shareWeight(oj, ikj, fkj, ikwa, fkwa, shareAttr='translate'):
        mult_ik = cmds.createNode('multiplyDivide')
        cmds.connectAttr('%s.%s'%(ikj, shareAttr), '%s.input1'%mult_ik, f=1)
        cmds.connectAttr(ikwa, '%s.input2X'%mult_ik, f=1)
        cmds.connectAttr(ikwa, '%s.input2Y'%mult_ik, f=1)
        cmds.connectAttr(ikwa, '%s.input2Z'%mult_ik, f=1)
        mult_fk = cmds.createNode('multiplyDivide')
        cmds.connectAttr('%s.%s'%(fkj, shareAttr), '%s.input1'%mult_fk, f=1)
        cmds.connectAttr(fkwa, '%s.input2X'%mult_fk, f=1)
        cmds.connectAttr(fkwa, '%s.input2Y'%mult_fk, f=1)
        cmds.connectAttr(fkwa, '%s.input2Z'%mult_fk, f=1)
        plus_node = cmds.createNode('plusMinusAverage')
        cmds.connectAttr('%s.output'%mult_ik, '%s.input3D[0]'%plus_node, f=1)
        cmds.connectAttr('%s.output'%mult_fk, '%s.input3D[1]'%plus_node, f=1)
        cmds.connectAttr('%s.output3D'%plus_node, '%s.%s'%(oj, shareAttr), f=1)
        

if __name__ == '__main__':
    print('Run in main')
    JointSetIkFk().jjjIkFkSet('IKFK')
