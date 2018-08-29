#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-08-29 14:10 
import os
from SouAng.smod import ssys

class Generator(object):
    TYPE_MODULE = "<type 'module'>"
    TYPE_CLASS = "<type 'module'>"

    def __init__(self):
        super(Generator, self).__init__()
        self.module = None
        self.path = None

    def generat(self, module, path):
        self.module = module
        self.path = path
        ssys.mtpath(self.path, 1)
        print('generat')

    @staticmethod
    def recursiveAll(input_):
        if str(type(input_)) == "<type 'module'>"


if __name__ == '__main__':
    print('Run in main')
