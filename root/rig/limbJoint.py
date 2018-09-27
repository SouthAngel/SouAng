#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-20 15:41 
from maya import cmds
import pymel.core as pm
from SouAng.smod import smaya
from . import nodeOperate


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
        
    @staticmethod
    def ikStretch():
        sel = cmds.ls(sl=1)
        if len(sel) < 2:
            return 0
        ik_con = sel[0]
        getJoints = [None for i in xrange(3)]
        if not JointSetIkFk.getFromParent(sel[1], getJoints):
            return 0
        baseAttr = ('baseDistanceUp', 'baseDistanceDown', 'baseDistanceLine')
        joints = (getJoints[0], getJoints[2], getJoints[1])
        distance_node = nodeOperate.distanceObjs(joints[0], joints[2])
        if not cmds.objExists('%s.%s'%(ik_con, baseAttr[0])):
            cmds.addAttr(ik_con, ln=baseAttr[0], at='double', dv=cmds.getAttr('%s.tx'%joints[1]))
            cmds.setAttr('%s.%s'%(ik_con, baseAttr[0]) , l=1)
        if not cmds.objExists('%s.%s'%(ik_con, baseAttr[1])):
            cmds.addAttr(ik_con, ln=baseAttr[1], at='double', dv=cmds.getAttr('%s.tx'%joints[2]))
            cmds.setAttr('%s.%s'%(ik_con, baseAttr[1]) , l=1)
        if not cmds.objExists('%s.%s'%(ik_con, baseAttr[2])):
            cmds.addAttr(ik_con, ln=baseAttr[2], at='double', dv=cmds.getAttr('%s.distance'%distance_node[0]))
            cmds.setAttr('%s.%s'%(ik_con, baseAttr[2]) , l=1)
        cmds.delete(distance_node)
        # ###
        multiplyDivide3_node = cmds.createNode('multiplyDivide')
        plusMinusAverage3_node = cmds.createNode('plusMinusAverage')
        multiplyDivide4_node = cmds.createNode('multiplyDivide')
        plusMinusAverage2_node = cmds.createNode('plusMinusAverage')
        joint1_node = joints[0]
        joint3_node = joints[2]
        multiplyDivide2_node = cmds.createNode('multiplyDivide')
        locator1_pointConstraint1_node = cmds.createNode('pointConstraint')
        condition1_node = cmds.createNode('condition')
        joint2_node = joints[1]
        multiplyDivide1_node = cmds.createNode('multiplyDivide')
        nurbsCircle1_node = ik_con
        distanceBetween2_node = cmds.createNode('distanceBetween')
        plusMinusAverage6_node = cmds.createNode('plusMinusAverage')
        locator2_pointConstraint1_node = cmds.createNode('pointConstraint')
        if not cmds.objExists('%s.strechValues'%nurbsCircle1_node):
            cmds.addAttr(nurbsCircle1_node, ln='strechValues', nn='Strech Values', at='double', dv=1)
            cmds.setAttr('%s.strechValues'%nurbsCircle1_node, e=1, keyable=1)
        if not cmds.objExists('%s.strechHandle'%nurbsCircle1_node):
            cmds.addAttr(nurbsCircle1_node, ln='strechHandle', nn='Strech Handle', at='double', max=1, min=0)
            cmds.setAttr('%s.strechHandle'%nurbsCircle1_node, e=1, keyable=1)
        cmds.connectAttr('%s.baseDistanceUp'%nurbsCircle1_node, '%s.input1X'%multiplyDivide3_node, f=1)
        cmds.connectAttr('%s.baseDistanceDown'%nurbsCircle1_node, '%s.input1Y'%multiplyDivide3_node, f=1)
        cmds.connectAttr('%s.strechValues'%nurbsCircle1_node, '%s.input2X'%multiplyDivide3_node, f=1)
        cmds.connectAttr('%s.strechValues'%nurbsCircle1_node, '%s.input2Y'%multiplyDivide3_node, f=1)
        cmds.connectAttr('%s.baseDistanceUp'%nurbsCircle1_node, '%s.input3D[0].input3Dx'%plusMinusAverage3_node, f=1)
        cmds.connectAttr('%s.baseDistanceDown'%nurbsCircle1_node, '%s.input3D[1].input3Dx'%plusMinusAverage3_node, f=1)
        cmds.connectAttr('%s.baseDistanceUp'%nurbsCircle1_node, '%s.input1X'%multiplyDivide4_node, f=1)
        cmds.connectAttr('%s.baseDistanceDown'%nurbsCircle1_node, '%s.input1Y'%multiplyDivide4_node, f=1)
        cmds.connectAttr('%s.output3Dx'%plusMinusAverage3_node, '%s.input2X'%multiplyDivide4_node, f=1)
        cmds.connectAttr('%s.output3Dx'%plusMinusAverage3_node, '%s.input2Y'%multiplyDivide4_node, f=1)
        cmds.connectAttr('%s.outputX'%multiplyDivide3_node, '%s.input3D[0].input3Dx'%plusMinusAverage2_node, f=1)
        cmds.connectAttr('%s.outputY'%multiplyDivide3_node, '%s.input3D[0].input3Dy'%plusMinusAverage2_node, f=1)
        cmds.connectAttr('%s.outputX'%multiplyDivide1_node, '%s.input3D[1].input3Dx'%plusMinusAverage2_node, f=1)
        cmds.connectAttr('%s.outputY'%multiplyDivide1_node, '%s.input3D[1].input3Dy'%plusMinusAverage2_node, f=1)
        cmds.connectAttr('%s.output3Dy'%plusMinusAverage2_node, '%s.translateX'%joint3_node, f=1)
        cmds.connectAttr('%s.outColorR'%condition1_node, '%s.input1X'%multiplyDivide2_node, f=1)
        cmds.connectAttr('%s.outColorR'%condition1_node, '%s.input1Y'%multiplyDivide2_node, f=1)
        cmds.connectAttr('%s.outputX'%multiplyDivide4_node, '%s.input2X'%multiplyDivide2_node, f=1)
        cmds.connectAttr('%s.outputY'%multiplyDivide4_node, '%s.input2Y'%multiplyDivide2_node, f=1)
        cmds.connectAttr('%s.translate'%nurbsCircle1_node, '%s.target[0].targetTranslate'%locator1_pointConstraint1_node, f=1)
        cmds.connectAttr('%s.rotatePivot'%nurbsCircle1_node, '%s.target[0].targetRotatePivot'%locator1_pointConstraint1_node, f=1)
        cmds.connectAttr('%s.rotatePivotTranslate'%nurbsCircle1_node, '%s.target[0].targetRotateTranslate'%locator1_pointConstraint1_node, f=1)
        cmds.connectAttr('%s.parentMatrix'%nurbsCircle1_node, '%s.target[0].targetParentMatrix'%locator1_pointConstraint1_node, f=1)
        cmds.connectAttr('%s.output3Dx'%plusMinusAverage3_node, '%s.firstTerm'%condition1_node, f=1)
        cmds.connectAttr('%s.distance'%distanceBetween2_node, '%s.secondTerm'%condition1_node, f=1)
        cmds.connectAttr('%s.output3Dx'%plusMinusAverage6_node, '%s.colorIfFalseR'%condition1_node, f=1)
        cmds.connectAttr('%s.output3Dx'%plusMinusAverage2_node, '%s.translateX'%joint2_node, f=1)
        cmds.connectAttr('%s.outputX'%multiplyDivide2_node, '%s.input1X'%multiplyDivide1_node, f=1)
        cmds.connectAttr('%s.outputY'%multiplyDivide2_node, '%s.input1Y'%multiplyDivide1_node, f=1)
        cmds.connectAttr('%s.strechHandle'%nurbsCircle1_node, '%s.input2X'%multiplyDivide1_node, f=1)
        cmds.connectAttr('%s.strechHandle'%nurbsCircle1_node, '%s.input2Y'%multiplyDivide1_node, f=1)
        cmds.connectAttr('%s.constraintTranslate'%locator2_pointConstraint1_node, '%s.point1'%distanceBetween2_node, f=1)
        cmds.connectAttr('%s.constraintTranslate'%locator1_pointConstraint1_node, '%s.point2'%distanceBetween2_node, f=1)
        cmds.connectAttr('%s.distance'%distanceBetween2_node, '%s.input3D[0].input3Dx'%plusMinusAverage6_node, f=1)
        cmds.connectAttr('%s.output3Dx'%plusMinusAverage3_node, '%s.input3D[1].input3Dx'%plusMinusAverage6_node, f=1)
        cmds.connectAttr('%s.translate'%joint1_node, '%s.target[0].targetTranslate'%locator2_pointConstraint1_node, f=1)
        cmds.connectAttr('%s.rotatePivot'%joint1_node, '%s.target[0].targetRotatePivot'%locator2_pointConstraint1_node, f=1)
        cmds.connectAttr('%s.rotatePivotTranslate'%joint1_node, '%s.target[0].targetRotateTranslate'%locator2_pointConstraint1_node, f=1)
        cmds.connectAttr('%s.parentMatrix'%joint1_node, '%s.target[0].targetParentMatrix'%locator2_pointConstraint1_node, f=1)
        cmds.setAttr('%s.operation'%multiplyDivide4_node, 2)
        cmds.setAttr('%s.enableRestPosition'%locator1_pointConstraint1_node, True)
        cmds.setAttr('%s.operation'%condition1_node, 3)
        cmds.setAttr('%s.operation'%plusMinusAverage6_node, 2)
        cmds.setAttr('%s.enableRestPosition'%locator2_pointConstraint1_node, True)
        # ### 
    

if __name__ == '__main__':
    print('Run in main')
    JointSetIkFk().jjjIkFkSet('IKFK')
