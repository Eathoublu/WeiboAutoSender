# -*- coding:utf-8 -*-
import requests
import cookielib
import urllib2
import json
import re

def get_urls(data):
  print 'got it!', data
  # data = '{"retcode":20000000,"msg":"","data":{"crossdomainlist":{"weibo.com":"https:\/\/passport.weibo.com\/sso\/crossdomain?entry=mweibo&action=login&proj=1&ticket=ST-MjIxNTA3MzUwNA%3D%3D-1519401683-yf-8EF91A7772AA6846F24C46E8CB322121-1","sina.com.cn":"https:\/\/login.sina.com.cn\/sso\/crossdomain?entry=mweibo&action=login&proj=1&ticket=ST-MjIxNTA3MzUwNA%3D%3D-1519401683-yf-2B51E94CE82EC76B7334D75961304BBD-1","weibo.cn":"https:\/\/passport.sina.cn\/sso\/crossdomain?entry=mweibo&action=login&ticket=ST-MjIxNTA3MzUwNA%3D%3D-1519401683-yf-A74BF8EAB0A83C6C2FA971F3EADCFD68-1"},"loginresulturl":"","uid":"2215073504"}}'
  jsonInsetance = json.loads(data)
  url1 = re.findall(u"com': u'(.*?)', u'", str(jsonInsetance))
  url2 = re.findall(u"m.cn': u'(.*?)', u'", str(jsonInsetance))
  url3 = re.findall(u"bo.cn': u'(.*?)'}, u'", str(jsonInsetance))
  return url1[0], url2[0], url3[0]

cookie = cookielib.MozillaCookieJar() #创建一个cookie对象来保存cookie
handler = urllib2.HTTPCookieProcessor(cookie) #用urllib创建一个cookie处理对象
opener = urllib2.build_opener(handler) #构建一个handler对象，opener可以直接打开网站
#记得要绑定
data0 = {
'username':'{your username}',
'password':'{your password}',
'savestate':'1',
'r':'http://m.weibo.cn',
'ec':'0',
'pagerefer':'https://m.weibo.cn/p/102803_ctg1_8999_-_ctg1_8999_home',
'entry':'mweibo',
'wentry': '',
'loginfrom': '',
'client_id': '',
'code': '',
'qq': '',
'mainpageflag':'1',
'hff': '',
'hfp': ''
}   #data不应该是字典，否则unhashable

data = 'password={your password}&savestate=1&r=http://m.weibo.cn&ec=1&pagerefer=https://m.weibo.cn/p/102803_ctg1_8999_-_ctg1_8999_home&entry=mweibo&wentry=&loginfrom=&client_id=&code=&qq=&mainpageflag=1&hff=&hfp='
data2 = 'username={your id (url encoded)}&password={your password}&savestate=1&r=&ec=0&pagerefer=&entry=mweibo&wentry=&loginfrom=&client_id=&code=&qq=&mainpageflag=1&hff=&hfp='

headers = {

'Referer':'https://passport.weibo.cn/signin/login',
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Mobile Safari/537.36',
'Origin':'https://passport.weibo.cn'

}


headers2 = {

'Host':'m.weibo.cn',
'Origin':'https://m.weibo.cn',
'Referer':'https://m.weibo.cn/compose',
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Mobile Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'X-Requested-With':'XMLHttpRequest'
}

# req = urllib2.Request('https://passport.weibo.cn/signin/login',data=data , headers=headers)#通过该方法创建一个网页对象
req = urllib2.Request('https://passport.weibo.cn/sso/login', data=data2, headers=headers)
html = opener.open(req)

obj = html.read().decode('gb2312') #html.read().decode('gb2312')对象引用一次就被销毁了？

print obj

u1, u2, u3 = get_urls(obj)

#当变量名为str时，出现这个奇怪的报错：TypeError: 'unicode' object is not callable 查明原因：使用了关键字命名变量，修改掉即可

print u1, u2, u3

opener.open(u1)
opener.open(u2)
opener.open(u3)

req2 = urllib2.Request('https://m.weibo.cn', headers=headers)
opener.open(req2)

for item in cookie:
    print item.name, item.value

# x = raw_input('请输入手动获得的st值：')

#
# req2 = urllib2.Request('https://m.weibo.cn/compose', headers=headers2)
#
# check = opener.open(req2)
#
# print check.read().decode('utf-8')

html = requests.get('https://m.weibo.cn/compose', params=headers, cookies=cookie)
st = re.findall("st: '(.+?)',", html.text)[0]
print st

data3 = 'content=konnichiha minasan&visible=1&st=' + st
print data3


# print html.text #很奇怪，使用urllib抓下来就是乱码，使用requests抓下来就是正常的

# 'https://m.weibo.cn/api/users/show' #获取个人数据成功！

#
req4 = urllib2.Request('https://m.weibo.cn/api/statuses/update', data=data3, headers = headers)

html = opener.open(req4)
#
print html.read()


# data3 = 'content=%E5%86%8D%E6%B5%8B%E8%AF%95%E4%B8%80%E6%AC%A1%E3%80%82%E3%80%82%E3%80%82&visible=1&st=2b8d9b'
#
#
# html2 = opener.open(req2)
#
# print html2.read().decode('gb2312')
# html = requests.get('https://m.weibo.cn/api/statuses/update', params=headers2)
#
# print html.text


# req3 = urllib2.Request('https://m.weibo.cn/compose',headers=headers2)
#
# html2 = opener.open(req3)
#
# print html2
#
# html3 = requests.get('https://m.weibo.cn/api/statuses/update', params=headers2)
# print html3
