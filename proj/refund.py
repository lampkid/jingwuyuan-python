# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from BeautifulSoup import BeautifulSoup

from jingwuyuan.net import HttpClient
from jingwuyuan.cron import TaskManager
from jingwuyuan.mail import Mail


def getRefundURL(refundCode):
    refundApi = 'http://q.m.hexun.com/ajax/ajax_fund_detail_iopv.php?code=%s' % refundCode
    return refundApi


def getRefundInfo(refundCode):

    refundApi = getRefundURL(refundCode)
    hc = HttpClient()
    return hc.request(refundApi, mobile='iPhone').read()

def buildRefundInfo(refundCode, html):
    soup = BeautifulSoup(html)
    realtimeValues = []
    nodeList = soup.findAll('mindata')
    for node in nodeList:
        try:
            nodeValue = float(node.text)
        except:
            continue

            import traceback
            traceback.print_exc()

        realtimeValues.append(nodeValue)

    latestValue = '--'
    print len(realtimeValues)
    if len(realtimeValues) > 0:
        latestValue = realtimeValues[-1]

    confirmedDate = soup.releasedate.text
    confirmedValue = soup.unitnetvalue.text

    refundName = refundCode
    if refundCode == '001158':
        refundCode = '工银新材料新能源股票'

    return {
        'name': refundCode,
        'code': refundName,
        'realtimeValues': realtimeValues,
        'confirmedDate': confirmedDate,
        'confirmedValue': confirmedValue,
        'updateTime': soup.updatetime,
        'latestValue': latestValue
    }


def buildMailContent(refundData):
    content = "<table width='100%' align='center' cellpadding='0' cellspacing='0' style='border-collapse:collapse'><tr><td style='background-color:#f7f9fa;' >"
    content = "<h2 style='text-align:center; padding: 20px;background-color:#eb414b;color:#ffffff;'>基金收益提醒<br></h2> "

    content += "<table align='center' cellpadding='0' width='80%' cellspacing='0' style='border-collapse:collapse;margin-bottom:30px;'>"
    content += "<tr><td>基金：</td><td>%s</td> </tr>" % refundData.get('name', '--')
    content += '<tr><td>基金代码：</td><td>%s</td></tr>' % refundData.get('code', '--')

    confirmed = (refundData.get('confirmedValue', '--'),refundData.get('confirmedDate', '--'))
    content += '<tr><td>已确认净值：</td><td><b>%s</b> [%s] </td></tr>' % confirmed

    latest = (refundData.get('latestValue', '--'),refundData.get('updateTime', '--'))
    content += '<tr><td>最新净值：</td><td><b>%s</b> [%s] </td></tr>' % latest

    content += "</table><br />"

    content += "</td></tr></table>"

    return content

def sendMail(content):
    server = 'smtp.qq.com'
    user = 'lampkid@qq.com'
    password = 'ayxceudeurhubffc'
    displayName = '静悟猿基金'
    postfix = 'qq.com'


    mail = Mail(server, user, password, displayName, postfix)

    receivers = ['lampkid@qq.com', '497462302@qq.com', 'hh211@qq.com', '934277507@qq.com']
    subject =  '基金净值自动提醒'
    mail.send(receivers, subject, content)

def refundTask():
    refundList = []
    refundCode = '001158'
    html = getRefundInfo(refundCode)
    data = buildRefundInfo(refundCode, html)
    content = buildMailContent(data)

    sendMail(content)



def monitorRefund():
    tm = TaskManager()

    tm.addTask(refundTask)

    tm.startCron(hour=14)

