#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-05 11:08 
from maya import cmds
from SouAng.smod import ssys, smaya


class GenratorCodeC(object):
    ALLOW_ATTR_TYPE = set(('bool', 'enum', 'renderType', 'float', 'double', 'long', 'typed'))
    EXCEPT_CHAR = set('.[]')

    def __init__(self):
        super(GenratorCodeC, self).__init__()
        self.script_gen = ''

    def generate(self, output_print=1, output_file=None):
        self.script_gen = ''
        sel = cmds.ls(sl=1)
        set_sel = set(sel)
        up_stream_all = cmds.listConnections(sel, s=1, d=0, p=1, c=1)
        for each in iter(sel):
            self.script_gen += '{n}_node = cmds.createNode(\'{t}\', n=\'{n}\')\n'.format(n=each, t=cmds.nodeType(each))
        self.script_gen += self.findUserDefinedAttribute(sel)
        for i in xrange(0, len(up_stream_all), 2):
            node_f, attr_f = self.splitAttrName(up_stream_all[i])
            node_s, attr_s = self.splitAttrName(up_stream_all[i+1])
            if node_f in set_sel and node_s in set_sel:
                str_f = '\'%s.{}\'%{}_node'.format(attr_f, node_f)
                str_s = '\'%s.{}\'%{}_node'.format(attr_s, node_s)
                self.script_gen += 'cmds.connectAttr(%s, %s, f=1)\n'%(str_s, str_f)
        self.script_gen += self.findNotDefaultAttribute(sel)
        self.outWrite()

    def outWrite(self, output_print=1, output_file=None):
        if output_print:
            print('*'*99 + '\n' + self.script_gen + '\n' + '*'*99 + '\n')
        if output_file:
            ssys.mtpath(output_file)
            with open(output_file, 'rb') as opf:
                opf.write(self.script_gen)

    @staticmethod
    def findNotDefaultAttribute(nodes):
        res_str = ''
        for node in iter(nodes):
            for attr in cmds.listAttr(node, m=1):
                if len(set(attr) & GenratorCodeC.EXCEPT_CHAR):
                    continue
                if cmds.listConnections('%s.%s'%(node, attr)):
                    continue
                attr_type = cmds.attributeQuery(attr, n=node, at=1)
                if attr_type in  GenratorCodeC.ALLOW_ATTR_TYPE:
                    attr_n = cmds.getAttr('%s.%s'%(node, attr))
                    attr_d = cmds.attributeQuery(attr, n=node, ld=1)
                    if attr_type == 'typed':
                        if attr_n:
                            attr_data_type = cmds.addAttr('%s.%s'%(node, attr), q=1, dt=1)
                            if attr_data_type!=None and attr_data_type[0] == 'string':
                                res_str += 'cmds.setAttr(\'%s.{}\'%{}_node, \'{}\', type=\'string\')\n'.format(attr, node, attr_n)
                    elif attr_n != attr_d[0]:
                        res_str += 'cmds.setAttr(\'%s.{}\'%{}_node, {})\n'.format(attr, node, attr_n)
        return res_str

    @staticmethod
    def findUserDefinedAttribute(nodes):
        res_str = ''
        for node in iter(nodes):
            attr_ud = cmds.listAttr(node, ud=1)
            if not attr_ud:
                continue
            for attr in attr_ud:
                attr_type = cmds.attributeQuery(attr, n=node, at=1)
                attr_n = cmds.getAttr('%s.%s'%(node, attr))
                attr_d = cmds.attributeQuery(attr, n=node, ld=1)
                name_nn = cmds.attributeQuery(attr, n=node, nn=1)
                if attr_type == 'duble3':
                    if name_nn:
                        res_str += 'cmds.addAttr({}_node, ln=\'{}\', nn=\'{}\', at=\'double3\')\n'.format(node, attr, name_nn)
                elif attr_type == 'typed':
                        res_str += 'cmds.addAttr({}_node, ln=\'{}\', nn=\'{}\', dt=\'string\')\n'.format(node, attr, name_nn)
                elif attr_type == 'enum':
                        res_str += 'cmds.addAttr({}_node, ln=\'{}\', nn=\'{}\', en=\'{}\')\n'.format(node, attr, name_nn,
                                cmds.attributeQuery(attr, n=node, le=1)[0])
                else:
                    attr_p = cmds.attributeQuery(attr, n=node, lp=1)
                    if attr_p:
                        res_str += 'cmds.addAttr({}_node, ln=\'{}\', nn=\'{}\', at=\'{}\', p=\'{}\')\n'.format(node, attr,
                                name_nn, attr_type, attr_p[0])
                    else:
                        res_str += 'cmds.addAttr({}_node, ln=\'{}\', nn=\'{}\', at=\'{}\')\n'.format(node, attr, name_nn,
                                attr_type)
                res_str += 'cmds.setAttr(\'%s.{}\'%{}_node, e=1, keyable=1)\n'.format(attr, node)
        return res_str

    @staticmethod
    def splitAttrName(name_attr):
        pos_dot = name_attr.find('.')
        return name_attr[:pos_dot], name_attr[pos_dot+1:]


if __name__ == '__main__':
    print('Run in main')
    GenratorCodeC().generate()
