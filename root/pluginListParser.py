#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: 1932554894@qq.com 
# Time: 2018-08-25 19:13 
import xml.etree.cElementTree as ET


if __name__ == '__main__':
    print('Run in main')
    tree = ET.parse(r"D:\001forM\project\code_dev\SouAng\plugins.xml")
    root = tree.getroot()
    for each in tree.iter():
        print(each, each.tag, each.attrib, each.text)
