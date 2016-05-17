# -*- coding: utf-8 -*-

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Mail(object):
    def __init__(self, server, user, password, displayName=None, postfix=''):
        self.sendServer = server
        self.sendUser = user
        self.sendPassword = password

        self.postfix = postfix

        if displayName:
            self.sendDisplayName = displayName
        else:
            self.sendDisplayName = '自动邮件系统'

    def setSendServer(self):
        pass
        
    def openDebugMode(self):
        pass

    def addPicToContent(self):
        #在正文显示图片,这个还是在发送的content里构造吧
        pass

    def send(self, receiverList, subject, content, attachFileList=[]):

        """
        receiverList：收件人；subject：主题；content：邮件内容
        """

        sender = self.sendDisplayName + "<" + self.sendUser + "@" + self.postfix + ">"

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ";".join(receiverList)

        txt = MIMEText(content,_subtype='html',_charset='utf-8')

        msg.attach(txt)


        #构造附件

        for attachFile in attachFileList:

            attachFilename = os.path.basename(attachFile)
            att = MIMEText(open(attachFile, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % attachFilename
            msg.attach(att)


        """
        # 将图片在正文中直接展示,上面那几行也可以哦
        file = "test.png"
        image = MIMEImage(open(file,'rb').read())
        image.add_header('Content-ID','<image1>')
        msg.attach(image)
        """


        isSuccess = False
        try:
            s = smtplib.SMTP()
            s.connect(self.sendServer)

            s.ehlo()
            s.starttls()
            s.ehlo

            s.login(self.sendUser, self.sendPassword)
            s.sendmail(sender, receiverList, msg.as_string())
            s.close()

            isSuccess = True

        except Exception, e:
            print str(e)

        return isSuccess



