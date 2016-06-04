# -*- coding=utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os

def listFiles(dir):

    files = []
    itemsIndir = os.listdir(dir)
    for filename in itemsIndir:
        dir = os.path.abspath(dir)
        filepath = os.path.join(dir, filename)
        if os.path.isfile(filepath):
            files.append(filepath)

    return files


if __name__ == '__main__':
    dirpath = '.'
    print listFiles(dirpath)


