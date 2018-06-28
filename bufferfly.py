#!/usr/bin/evn python3
#_*_ coding:utf-8 _*-
#信息搜集资产处理框架v1
#author dr0op

import requests
import re
import getopt,sys
import threading
from queue import Queue

active_url_list = []
threadList = []
urlQueue = Queue(1000)

usage ='''

    __          ________          ______     
   / /_  __  __/ __/ __/__  _____/ __/ /_  __
  / __ \/ / / / /_/ /_/ _ \/ ___/ /_/ / / / /
 / /_/ / /_/ / __/ __/  __/ /  / __/ / /_/ / 
/_.___/\__,_/_/ /_/  \___/_/  /_/ /_/\__, /  
                                    /____/   

渗透测试资产处理框架，对渗透测试前的信息搜集到的大批量资产进行处理的框架，可插件扩展 
python3 bufferfly.py -t 20 -g urls.txt 

1.高速资产存活检测，获取标题
2.资产去重：单文件去重，双文件去重
3.导出为excel，导入excel
4.多线程支持
5.功能插件化支持，可扩展

-t   --thread   设置线程数，若要设置，在第一个参数设置
-g   --gettitle 存活检测-获取url的title
-m   --mvdups   单文件去重
     --mvdup2  双文件去重，去除文件1和文件2中共同的部分
'''




# 获取url请求title，返回title值
def getTitle(url):

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

    if "http://" or "https://" not in url:
        url = "http://"+url
    try:
        res = requests.get(url,headers=headers,timeout=2)
    except:
        return

    split = "   ------  "
    code = res.status_code
    enc = res.encoding
    if code in [200,301,302]:
        try:
            text=res.text.encode(enc).decode('utf-8')
        except:
            text=res.text.encode(enc).decode('gbk')

        try:
            title =re.search(r'<title>(.*?)</title>',text,re.I).group(1)
        except:
            title="Null"
    
        print(str(url)+split+str(code)+split+title)
        return str(url)+split+str(code)+split+title
    else:
        return



#文本去重,
def MovDups(file):
# 大文件，使用上下文管理,利用set的键值去重
    with open(file,'r') as f:
        with open(file.split(".")[0]+'-rmdups.txt','w') as ff:
            while True:
                ulist = f.readlines(1024*10)
                if not ulist:
                    break
                rustr = "".join(list(set(ulist)))
                ff.write(rustr)

#双文本去重
def MovDups2(file1,file2):
    #去除file1中含有file2内容的部分，然后将两个文件合并
    cache = []
    with open(file1,'r') as f:
        for ln in f.readlines():
            cache.append(ln)
            print(ln)
    
    with open(file2,'r') as ff:
        for ln in ff.readlines():
            if ln in cache:
                cache.remove(ln)
                continue
            cache.append(ln)
            
    with open("mv2dups.txt",'w') as fff:
        for ln in cache:
            print(ln)
            fff.write(ln)


#多线程
class MyThread(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q
    def run(self):
        while not self.q.empty():
            getTitle(self.q.get())
        


def main():
    thread_nums = 10
    helplist = ['help','thread=','infile=','outfile=','mvdups=',"gettitle=","mvdup2=",]
    try:
        opts,args = getopt.getopt(sys.argv[1:],"ht:i:o:m:g:",helplist)
    except getopt.GetoptError:
        print(usage)
    for opt,arg in opts:
        if opt in ('-m','--mvdups'):
            MovDups(arg)
        elif opt in ('-h','--help'):
            print(usage)
        elif opt in ('-t','--thread'):
            thread_nums = int(arg)
        elif opt in ('--mvdup2'):
            MovDups2(sys.argv[-1],sys.argv[-2])
        elif opt in ('-g','--gettile'):
            with open(arg,'r') as f:
                for line in f.readlines():
                    urlQueue.put(line.strip())
            print("Queue ok !")
            print("thread nums:",thread_nums,"!")
            for i in range(thread_nums):
                threadList.append(MyThread(urlQueue))
            for t in threadList:
                t.start()
            for l in threadList:
                l.join()


if __name__ == '__main__':
    main()
    