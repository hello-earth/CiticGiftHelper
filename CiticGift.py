# -*- coding:utf-8 -*-


import urllib,urllib2,re,json
import SockCookie


###
#
#拉杆箱 49
#电饭锅 48
#牙刷 47
#
###
#http://zx.51cnb.xin/buy.php?pid=47&month=01
pids = ["49","48","47","44"]
month = "01"
retry = 10

mheader = {
    'Host': 'zx.51cnb.xin',
    "Connection": "keep-alive",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.27.400 QQBrowser/9.0.2524.400",
    "Cookie": "PHPSESSID=imb23ntoanl8nvm4crro13khh3"
}

def updateCookie():
    cookie = SockCookie.getCookie("zx.51cnb.xin")
    if(len(cookie)==26):
        global  mheader
        print "get cookie : "+cookie
        mheader['Cookie']="PHPSESSID="+cookie
        return True
    return False
		
def get(url):
    request = urllib2.Request(url, headers=mheader)
    content = urllib2.urlopen(request,timeout=10)
    return content.read()

def post(posturl, dictdata):
    json_obj = urllib.urlencode(dictdata)
    request = urllib2.Request(posturl, json_obj, headers=mheader)
    content = urllib2.urlopen(request, timeout=10)
    return content.read()

def getItem(mpid):
    global month
    data = get("http://zx.51cnb.xin/buy.php?pid=%s" % (mpid))
    token = re.compile("token : '(.*?)'".decode('u8')).findall(data)[0]
    if (token):
        post_data = {"pid": mpid, "month": month, "token": token}
        data = post("http://zx.51cnb.xin/exchange.php", post_data)
        data = json.loads(data)
        return data

def ExchangeGift():
    for pid in pids:
        if(pid=="49"):
            print u"正在抢拉杆箱"
        elif(pid=="48"):
            print u"正在抢电饭锅"
        elif(pid=="47"):
            print u"正在抢牙刷"
        elif (pid == "46"):
            print u"正在抢小米电源"
        elif (pid == "45"):
            print u"正在抢爱奇艺月卡"
        elif (pid == "44"):
            print u"正在抢500MB流量"
        elif (pid == "43"):
            print u"正在抢100/70MB流量"

        for i in xrange(retry):
            result = getItem(pid)
            if(result):
                print result['msg']
                if(result['code']==0):
                    break
        print "*******************"
if __name__ == '__main__':

    if(updateCookie()):
        ExchangeGift()
    print "finish"
