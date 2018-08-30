#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-08-30 23:46 
import os
import xml.sax
import sqlite3
from SouAng.smod import ssys


FILE_CONFIG = ssys.StorePath.TOOL + '\\plugins.xml'


class PluginData(object):
    NAME_TABLE = 'PLUGINS_CACHE'
    FILE = ssys.StorePath.TEMP + '\\plugins.cache'
    KEY_TIME_MODIFY = 'timeModifyPluginCache'
    STUCT_TABLE = '''
    ID  INTEGER  PRIMARY  KEY  AUTOINCREMENT
    NAME  TEXT  NOT NULL
    NAME_CN  TEXT
    NAME_PATH  TEXT  NOT NULL
    COMMAND  TEXT  NOT NULL
    DESCRIPTION  TEXT
    ICON_PATH  TEXT
    '''

    def __init__(self):
        super(PluginData, self).__init__()
        self.line_cache = self.cacheLines()
        ssys.mtpath(self.FILE)
        self.db = sqlite3.connect(self.FILE)

    def __del__(self):
        self.db.close()

    def initTable(self):
        self.db.execute("DROP TABLE IF EXISTS  %s"%self.NAME_TABLE)
        script = 'CREATE TABLE IF NOT EXISTS %s (%s);'%(self.NAME_TABLE, self.line_cache[2])
        self.db.execute(script)
        self.db.commit()
        gData = ssys.GData()
        gData[self.KEY_TIME_MODIFY] = fileModfiyTime()

    def cacheLines(self):
        # [line_list, head_list, line_string, head_string]
        res = [self.parseStuctLines()]
        res.append([x.split(' ')[0] for x in res[0]])
        res.append(', '.join(res[0]))
        res.append(', '.join(res[1]))
        return res

    def parseStuctLines(self):
        lines = self.STUCT_TABLE.splitlines()
        res = []
        for line in lines:
            line_strip = line.strip()
            if line_strip:
                res.append(line_strip)
        return res


    def updata(self):
        print('updata')

    def find(self, found):
        script = 'SELECT * FROM {} WHERE {} LIKE \'%{}%\''.format(self.NAME_TABLE, self.line_cache[1][3], found)
        return self.db.execute(script)

    def outputAll(self):
        return self.db.execute('SELECT * FROM %s'%self.NAME_TABLE)

    def append(self, tub):
        script = 'INSERT INTO %s (<keys>) VALUES (<values>)'%self.NAME_TABLE
        script = script.replace('<keys>', self.line_cache[3][4:])
        script = script.replace('<values>', ' ,'.join(['\'%s\''%x.replace('\'', '\'\'') for x in tub]))
        self.db.execute(script)

    def update(self, content, fiter):
        script = 'UPDATE %s SET <content> WHERE <filter>'%self.NAME_TABLE


class ParseXml(xml.sax.ContentHandler):
    MARK_SPLIT_XPATH = '-:'

    def __init__(self):
        self.xpath = []
        self.indentPos = -1
        self.type = ''
        self.content = ''
        self.attribute = None
        self.db_write = PluginData()
        self.db_write.initTable()

    def safeGetAttr(self, key):
        if key in self.attribute:
            return self.attribute[key]
        else:
            return ''

    def startDocument(self):
        print('startDocument')

    def formatItemData(self):
        # item_data [name, name_cn, xpath, content, description, icon_path]
        # item_data [0   , 1      , 2    , 3      , 4          , 5        ]
        item_data = ['', '', '', '', '', '']
        item_data[0] = self.safeGetAttr('name')
        item_data[1] = self.safeGetAttr('name_cn')
        item_data[2] = self.MARK_SPLIT_XPATH.join(self.xpath)
        item_data[3] = self.content
        item_data[4] = self.safeGetAttr('description')
        item_data[5] = self.safeGetAttr('icon_path')
        return item_data

    def startElement(self, name, attrs):
        self.type = name
        self.indentPos = -1
        self.attribute = attrs
        self.xpath.append(self.safeGetAttr('name'))
        self.content = ''

    def characters(self, content):
        if self.indentPos == -1:
            if content.strip():
                indentLine = content.lstrip()
                self.indentPos = len(content) - len(indentLine)
                self.content += indentLine
        else:
            self.content += content[self.indentPos:]
            if content == '\n':
                self.content += content

    def endElement(self, name):
        if name == 'plugin':
            self.db_write.append(self.formatItemData())
            print('>>Cache item --%s--'%self.safeGetAttr('name'))
        self.xpath.pop()

    def endDocument(self):
        self.db_write.db.commit()


def parseFile():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    xml_handler = ParseXml()
    parser.setContentHandler(xml_handler)
    parser.parse(FILE_CONFIG)


def fileModfiyTime():
    return os.stat(FILE_CONFIG).st_mtime


def checkUpdata():
    if ssys.GData().get(PluginData.KEY_TIME_MODIFY) != fileModfiyTime():
        print('Update plugin list cache')
        parseFile()


if __name__ == '__main__':
    print('Run in main')
#     testObj = PluginData()
#     testObj.initTable()
#     print(testObj.append(['a', 'b', 'c', 'd']))
#     testObj.outputAll()
    checkUpdata()
#     parseFile()
    pTest = PluginData()
    for i in pTest.find(''):
        print(i)
    del pTest
    
