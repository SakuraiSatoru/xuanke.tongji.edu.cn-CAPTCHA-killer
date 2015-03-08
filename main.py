# -*- coding: utf-8 -*-
import urllib  
import urllib2
import cookielib
import cv2
import time
from numpy import *

def init(num):
    arr = zeros((12,8),dtype=int8)
    txt = open(str(num)+".txt",'r').read()
    row = txt.split('\n')
    a = 0
    for x in row:
        b = 0
        for y in x:
            arr[a,b] = int(y)          
            b = b + 1
        a = a + 1
    return arr
std = [n for n in range(10)]


def match(td):
    n = 0
    for num in std:
        flag = 1
        a = 0
        for x in num:
            if flag == 0:
                break
            b = 0
            for y in x:
                time.sleep(0)
                if y == 1:
                    if td[a,b][0] > 20:
                        flag = 0
                        break
                b = b + 1
            a = a + 1
        if flag == 1:
            return n
        n = n + 1

def main():
    img = cv2.imread("test.jpg")
    ret,threshold = cv2.threshold(img,150,255,cv2.THRESH_BINARY) #binary
    td1 = threshold[3:15,2:10]
    td1r = str(match(td1))
    td2 = threshold[3:15,11:19]
    td2r = str(match(td2))
    td3 = threshold[3:15,20:28]
    td3r = str(match(td3))
    td4 = threshold[3:15,29:37]
    td4r = str(match(td4))
    return td1r+td2r+td3r+td4r


for n in range(10):
    std[int(n)] = init(int(n))


cookie = cookielib.CookieJar()  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


for step in range(100):
    print 'start downloading CAPTCHA'
    result = opener.open('http://xuanke.tongji.edu.cn/CheckImage')
    rere = result.read()
    local = open ('test.jpg','wb')
    local.write(rere)
    local.close()
    print 'start analyzing CAPTCHA'
    yzm = main()
    print 'analyze complete',yzm




    postdata = urllib.urlencode({  
            'goto':'http://xuanke.tongji.edu.cn/pass.jsp?checkCode='+yzm,
            'gotoOnFail':'http://xuanke.tongji.edu.cn/deny.jsp?checkCode='+yzm+'&account=1350320&password=7D28A0516BCF63A800BDA4F18F5AD2E6',
            'Login.Token1':'1350320',
            'Login.Token2':'1073741824',
    })
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6' }
    headers = {'User-Agent' : user_agent} 
    req = urllib2.Request( 
        url = 'http://tjis2.tongji.edu.cn:58080/amserver/UI/Login',  
        data = postdata,
        headers = headers
    )
    result = opener.open(req)
    #print result.read().decode('GB2312')
    if 'var HELP_URL' in result.read():
        print 'success,count:',step
    else:
        print 'fail!'


