# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import thread
import time,string
import sys
import  socket
import os

import traceback


import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)


#----------- 加载处理糗事百科 -----------
class Spider_Model:

    def __init__(self):
        self.count= 0
        self.page = 1 #the searching page are visiting
        self.contents = []#the contents in the page
        self.search=False#  get title
        self.enable = False# all
        self.downloadnum=0


    def GetPage(self,page):
        myUrl = "http://www.uniqlox.com/page/"+str(page)
        print myUrl+" count="+str(self.count)
        req = urllib2.Request(myUrl)
        flag=False
        count=0
        while(flag==False):
         try:
          myResponse = urllib2.urlopen(req)
         #print myResponse.getcode()+'\n'
          myPage = myResponse.read()#encode的作用是将unicode编码转换成其他编码的字符串，decode的作用是将其他编码的字符串转换成unicode编码
          #print myPage
          unicodePage = myPage.decode("utf-8")
          myItems = re.findall('<iframe src=\'(.*?)\'',unicodePage,re.S)
          print myItems
          if len(myItems) < 10 and count< 3:
            print "len="+str(len(myItems))+'\n'
           # print myPage
            count+=1
          else:
             flag=True
             self.count+=len(myItems)
             return myItems
         except Exception,ex:
           time.sleep(2)
           print "Error:page2:"
       # print myItems
       # print 'ok'



    def Gotosearch(self):
        # 如果用户未输入quit则一直运行
        while self.search:
            myPage = self.GetPage(self.page)
            self.page += 1
            self.contents.append(myPage)
            f=open('f3.txt','a')
            for item in myPage:
                f.write(item+'\n')
            #time.sleep(5)
            if len(myPage) == 0:
               self.search=False




    def getdownload(self,list):
        myUrl = str(list)
        #print "url="+myUrl
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(myUrl, headers = headers)
        f=open('f1.txt','a')
        flag=False
        while flag==False:
            try:
                myResponse = urllib2.urlopen(req)
                myPage = myResponse.read()
                unicodePage = myPage.decode("utf-8")
                myItems = re.findall('(https://www.tumblr.com/video_file/.*?)\"',unicodePage,re.S)
                if myItems:
                   flag=True
                   for i in myItems:
                       self.downloadnum+=1
                       print 'downloadnum='+str(self.downloadnum)
                       f.write(i+'\n')
                   return
            except Exception as e:
               print "download"
               print e




    def down(self):
         while self.enable:
            if self.contents:
                nowPage = self.contents[0]
                del self.contents[0]
                for item in nowPage:
                   self.getdownload(item)

            else:
                if self.search==False:
                 self.enable=False
                 return
                else:
                    time.sleep(2)

    def start(self):
        self.search = True
        self.enable = True
        print u'正在加载中请稍候......'
        thread.start_new_thread(self.Gotosearch,())

        thread.start_new_thread(self.down,())
        thread.start_new_thread(self.down,())
        thread.start_new_thread(self.down,())
        thread.start_new_thread(self.down,())
        self.down()
        return
def delete(path):
     files = os.listdir(path)
     for f in files:
      myItems = re.findall('(\(\d\))',f,re.S)
      if myItems:
         print myItems
         os.remove(path+f)

def add(path):
   files = os.listdir(path)
   for f in files:
    f1=open(path+f,'a')
    print 'done'
    f1.write("\0")

print 'press enter to start：'
raw_input(' ')
'''
myUrl='http://www.uniqlox.com/page/300'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
req = urllib2.Request(myUrl, headers = headers)
myResponse = urllib2.urlopen(req)
myPage = myResponse.read()
print myPage
'''
'''
myModel = Spider_Model()
myModel.start()
'''
add("E://video//AV//AV//")


