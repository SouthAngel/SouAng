#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-25 19:13 
import xml.etree.cElementTree as ET
import sqlite3
from SouAng.smod import ssys


class PluginData(object):
    NAME_TABLE = 'PLUGINS_CACHE'
    FILE = ssys.StorePath.TEMP + '\\plugins.cache'

    def __init__(self):
        super(PluginData, self).__init__()
        ssys.mtpath(self.FILE)
        self.db = sqlite3.connect(self.FILE)

    def __del__(self):
        self.db.close()

    def checkUpdata(self):
        print('checkUpdata')

    def updata(self):
        print('updata')

    def find(self):
        script = 'SELECT column_list FROM table_name WHERE column LIKE \'XXXX%\''
        print('find')

    def append(self, tub):
        script = 'INSERT INTO %s (PID, COMMAND, NAME, DESCRIPION) VALUES (<values>)'%self.NAME_TABLE

    def update(self, content, fiter):
        script = 'UPDATE %s SET <content> WHERE <filter>'%self.NAME_TABLE


if __name__ == '__main__':
    print('Run in main')
    tree = ET.parse(r"D:\001forM\project\code_dev\SouAng\plugins.xml")
    root = tree.getroot()
    for each in tree.iter():
        print(each, each.tag, each.attrib, each.text)
