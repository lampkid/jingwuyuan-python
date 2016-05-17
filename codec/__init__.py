# -*- coding=utf-8 -*-

import traceback


def setDefaultEncodingUTF8():
    import sys
    reload(sys)

    sys.setdefaultencoding('utf-8')


def codecText(text, coding='utf-8'):
    textType = type(text)
    if textType is int:
        text = str(text)

    if textType is not unicode:
        try:
            text = text.decode('utf-8')
        except:
            #traceback.print_exc()
            text = text.decode('gbk').encode('utf-8')


    if coding != 'utf-8':
        text = text.encode(coding)
    return text


setDefaultEncodingUTF8()
