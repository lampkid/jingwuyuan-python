# -*- encoding=utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString

def parseXML2JSON(file):
    fp = open(file, 'r')
    content = fp.read()
    fp.close()

    soup = BeautifulSoup(content)
    jsonObj = {}
    parseNode(soup, jsonObj)

    return jsonObj

def parseNode(node, jsonObj):
    nodeName = node.name
    if nodeName == '[document]':
        nodeName = 'document'

    nodeObj= jsonObj.get(nodeName, None)

    if nodeObj is None:
        jsonObj[nodeName] = {}
        if type(node.contents) is list  and  len(node.contents) > 0 and isinstance(node.contents[0], NavigableString):
            print node.contents,'------------'
            text = node.contents[0].strip()
        else:
            text = ''

        jsonObj[nodeName]['text'] = text
        jsonObj[nodeName]['attrs'] = {}
        attrs = node.attrs
        for k, v in attrs:
            jsonObj[nodeName]['attrs'][k] = v


        jsonObj[nodeName]['children'] = {}
        childJsonObj = jsonObj[nodeName]['children']

    elif type(nodeObj) is dict and len(nodeObj) != 0:
        jsonObj[nodeName] =[nodeObj, {}]
        childJsonObj = jsonObj[nodeName][-1]

    elif type(nodeObj) is list:
        jsonObj[nodeName].append({})
        childJsonObj = jsonObj[nodeName][-1]





    children = node.findAll(recursive=False)
    if len(children) !=0:
        for child in children:

            parseNode(child, childJsonObj)


if __name__ == '__main__':
    file = 'XML/Trojan.xml'
    parseAwvsXML(file)
