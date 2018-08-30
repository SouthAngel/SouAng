#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-08-29 14:10 
import os
from SouAng.smod import ssys

class Generator(object):
    TYPE_MODULE = 'module'

    def __init__(self):
        super(Generator, self).__init__()
        self.module = None
        self.path = None
        self.list_rec = {}
        self.safeSet = set()
        self.m_under = ''

    def generat(self, module, path):
        self.module = module
        self.path = path
        self.m_under = module.__name__
        self.recursiveAllFolder(module)
        self.buildFolderStuct(path)
        self.writeToFile()
        print('generat')

    def buildFolderStuct(self,  path_):
        for k, v in self.list_rec.iteritems():
            path = path_ + '\\' + '\\'.join(k.split('.'))
            if v[1] == 'folder':
                path_folder = path + '\\__init__.py'
                ssys.mtpath(path_folder)
                v[4] = path_folder
            else:
                path_file = path + '.py'
                ssys.mtpath(path_file)
                v[4] = path_file

    def writeToFile(self):
        for km, vm in self.list_rec.iteritems():
            file_content = ''
            for kc, vc in vm[0].__dict__.iteritems():
                if not kc.startswith('__'):
                    file_content += 'class %s(object):\n\n    def __init__(self):\n        super(%s, self).__init__()\n\n'%(kc, kc)
                    for m in dir(vc):
                        if not m.startswith('__'):
                            file_content += '    def %s(self, *args, **kwargs):\n        return 1\n\n'%m
                    file_content += '\n\n'
            with open(vm[4], 'wb') as opf:
                opf.write(file_content)
            print('Write to %s'%vm[4])

    def recursiveAllFolder(self, input_, parent=None):
        ctype = type(input_).__name__
        name = input_.__name__
        ftype = self.determineFtype(input_)
        self.list_rec[name] = [input_, ftype, ctype, parent, '']
        if type(input_).__name__ == self.TYPE_MODULE:
            for m in input_.__dict__.itervalues():
                if ('__file__' in dir(m)) and (m not in self.safeSet) and (m.__name__.startswith(self.m_under)):
                    print(m.__name__)
                    self.safeSet.add(m)
                    self.recursiveAllFolder(m, name)
        else:
            print('%s is a class'%name)
        return self.list_rec
            
    
    @staticmethod
    def determineFtype(input_):
        if os.path.basename(input_.__file__) == '__init__.py':
            return 'folder'
        else:
            return 'file'


if __name__ == '__main__':
    print('Run in main')
    import PySide2
    generator = Generator()
    generator.generat(PySide2, r'E:\work\current\cache\compCode')
