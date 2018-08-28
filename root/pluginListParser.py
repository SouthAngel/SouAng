#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-25 19:13 
import xml.sax
import sqlite3
from SouAng.smod import ssys


class PluginData(object):
    NAME_TABLE = 'PLUGINS_CACHE'
    FILE = ssys.StorePath.TEMP + '\\plugins.cache'
    STUCT_TABLE = '''
    ID  INTEGER  PRIMARY  KEY  AUTOINCREMENT
    NAME  TEXT  NOT NULL
    NAME_PATH  TEXT  NOT NULL
    COMMAND  TEXT  NOT NULL
    DESCRIPTION  TEXT
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

    def cacheLines(self):
        # [line_list, id_list, line_string, id_string]
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

    def checkUpdata(self):
        print('checkUpdata')

    def updata(self):
        print('updata')

    def find(self, found):
        script = 'SELECT * FROM %s WHERE column LIKE \'%%s%\''%(self.NAME_TABLE, found)
        print('find')

    def outputAll(self):
        for i in self.db.execute('SELECT * FROM %s'%self.NAME_TABLE):
            print(i)

    def append(self, tub):
        script = 'INSERT INTO %s (<keys>) VALUES (<values>)'%self.NAME_TABLE
        script = script.replace('<keys>', self.line_cache[3][4:])
        script = script.replace('<values>', ' ,'.join(['\'%s\''%x for x in tub]))
        self.db.execute(script)

    def update(self, content, fiter):
        script = 'UPDATE %s SET <content> WHERE <filter>'%self.NAME_TABLE


class ParseXml(xml.sax.ContentHandler):

    def __init__(self):
        self.xpath = []
        self.type = ''
        self.content = ''
        self.attribute = None

    def startDocument(self):
        print('startDocument')

    def startElement(self, name, attrs):
        self.type = name
        self.attribute = attrs
        self.xpath.append(attrs['name'])
        self.content = ''
        print('startElement')
        print(name, attrs.items())

    def characters(self, content):
        self.content += content

    def endElement(self, name):
        print('endElement')
        if name == 'plugin':
            print(self.attribute['name'])
            print(self.xpath)
            print(self.content)
        print(name+'/End')
        self.xpath.pop()

    def endDocument(self):
        print('endDocument')


def parseFile():
    file_config = ssys.StorePath.TOOL + '\\plugins.xml'
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    xml_handler = ParseXml()
    parser.setContentHandler(xml_handler)
    parser.parse(file_config)


if __name__ == '__main__':
    print('Run in main')
#     testObj = PluginData()
#     testObj.initTable()
#     print(testObj.append(['a', 'b', 'c', 'd']))
#     testObj.outputAll()
    parseFile()
    
