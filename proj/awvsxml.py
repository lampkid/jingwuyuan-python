# -*- encoding=utf-8 -*-

from pprint import pprint

from jingwuyuan.xml import parseXML2JSON
from jingwuyuan.os import listFiles

def parseAwvsXML(dir):
    files = listFiles(dir)
    for file in files:
        print file
        pprint(parseXML2JSON(file))

if __name__ == '__main__':
    dir = 'XML/'
    dir = '/Users/chunmansun/code/webscan/XML/'
    parseAwvsXML(dir)
