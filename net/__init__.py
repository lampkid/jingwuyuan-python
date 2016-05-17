# -*- encoding=utf-8 -*-

import urllib
import urllib2
import cookielib

class HttpClient(object):

    def __init__(self, url=None):

        urllib2.socket.setdefaulttimeout(10)

        self.url = url;

    def simpleRequest(self, url=None, data={}):

        if url:
            self.url = url

        request = urllib2.Request(self.url, urllib.urlencode(data))
        request.add_header('User-Agent', 'fake-client')
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            response = e
            raise e;
        except urllib2.URLError, e:
            response = e
            raise e;

        return response

    def request(self, url=None, data=None, cookie=None, headers=None, mobile=None):

        if url:
            self.url = url

        '''
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        debugOpener = urllib2.build_opener(httpHandler, httpsHandler)
        urllib2.install_opener(debugOpener)
        '''


        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]

        if mobile:
            mobileUserAgent = ('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')
            opener.addheaders = [mobileUserAgent,]

        if headers:
            opener.addheaders = headers

        urllib2.install_opener(opener)

        if data:
            request = urllib2.Request(self.url, urllib.urlencode(data))
        else:
            request = urllib2.Request(self.url)

        request.add_header('Refferer',self.url)

        if cookie:
            request.add_header('Cookie', cookie)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            response = e
        except urllib2.URLError, e:
            response = e
            raise e;
        return response

    def requestWithCookie(self, url=None, data={}):

        if url:
            self.url = url

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]

        try:
            response = opener.open(self.url, urllib.urlencode(data))
        except urllib2.HTTPError, e:
            response = e
        except urllib2.URLError, e:
            response = e
            raise e;
        return response


if __name__ == '__main__':

    hc = HttpClient()
    url = 'http://www.jingwuyuan.net'
    print hc.request(url).read()

    import sys
    sys.exit()



