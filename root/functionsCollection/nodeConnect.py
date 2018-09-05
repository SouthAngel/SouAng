#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-05 11:08 
from maya import cmds
from SouAng.smod import ssys


class GenratorCodeC(object):

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
        for i in xrange(0, len(up_stream_all), 2):
            node_f, attr_f = self.splitAttrName(up_stream_all[i])
            node_s, attr_s = self.splitAttrName(up_stream_all[i+1])
            if node_f in set_sel and node_s in set_sel:
                str_f = '\'%s.{}\'%{}_node'.format(attr_f, node_f)
                str_s = '\'%s.{}\'%{}_node'.format(attr_s, node_s)
                self.script_gen += 'cmds.connectAttr(%s, %s, f=1)\n'%(str_s, str_f)
        self.outWrite()

    def outWrite(self, output_print=1, output_file=None):
        if output_print:
            print('*'*99 + '\n' + self.script_gen + '\n' + '*'*99 + '\n')
        if output_file:
            ssys.mtpath(output_file)
            with open(output_file, 'rb') as opf:
                opf.write(self.script_gen)

    @staticmethod
    def splitAttrName(name_attr):
        pos_dot = name_attr.find('.')
        return name_attr[:pos_dot], name_attr[pos_dot+1:]
