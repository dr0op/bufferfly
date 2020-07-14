#!/usr/bin/evn python3
#_*_ coding:utf-8 _*-
#攻防演习信息搜集资产处理框架v1.2.1
#author Ra1ndr0op

import requests
import re
import sys
import threading
from queue import Queue
import argparse
from lxml import etree
import random
from collections import Counter
import socket
from urllib.parse import urlparse


active_url_list = []
threadList = []
CsubThreadList = []
urlQueue = Queue(1000*100)
port = list(range(80,90))+list(range(8080,8091))+list(range(8000,8010))+[7001,8032,8023,9200,2375,5904,6066,7077,8161]
URIList = []
IPCsubList = []
lineQueue = Queue(1000*100)


banner = '''
    __          ________          ______     
   / /_  __  __/ __/ __/__  _____/ __/ /_  __
  / __ \/ / / / /_/ /_/ _ \/ ___/ /_/ / / / /
 / /_/ / /_/ / __/ __/  __/ /  / __/ / /_/ / 
/_.___/\__,_/_/ /_/  \___/_/  /_/ /_/\__, /  
                                    /____/      v1.2.1 
1.高速资产存活检测，获取标题
2.常见Web端口访问测试/获取标题  lxml方式速度较快
3.资产去重
4.随机UA
5.C段探测
6.识别C段IP
7.shiro识别
8.简单中间件识别

适用用于外网资产梳理

TODO:
1.在不发送更多请求的情况下模糊识别weblogic/jboss/jenkins/zabbix/activeMQ/solr/gitlab/spring等
2.常见端口扫描(22/445/3389/3306/6379/1521等常见端口  与masscan、nmap结合)

'''


# 获取url请求title，返回title值   利用正则方式获取title信息
def getTitle(url):

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

    if "http://" or "https://" not in url:
        url = "http://"+url
    try:
        sys.stdout.write("\r Going to access {0} ...".format(url))
        res = requests.get(url,headers=headers,timeout=2)
    except:
        return

    split = "   ------  "
    code = res.status_code
    enc = res.encoding

    if code in [200,301,302,404,403,500]:
        try:
            text=res.text.encode(enc).decode('utf-8')
        except:
            try:
                text=res.text.encode(enc).decode('gbk')
            except:
                pass
        try:
            title =re.search(r'<title>(.*?)</title>',text,re.I).group(1)
        except:
            title="Null"
    
        print(url+split+str(code)+split+title)
        return str(url)+split+str(code)+split+title
    else:
        return


# 获取url请求title，返回title值   利用lxml方式获取title信息

def getTitle2(url):
    headers={'User-Agent':get_user_agent(),'Cookie':'rememberMe=b69375edcb2b3c5084c02bd9690b6625',}

    if "http://" not in url:
        url = "http://"+url
    try:
        sys.stdout.write("\r[*]Recording to access {0} ...".format(url))
        res = requests.get(url,headers=headers,timeout=2)
    except:
        return

    split = "   ------  "
    code = res.status_code
    enc = res.encoding
    server = get_url_servers(res)
    ctext = ''
    if code in [200,301,302,404,403,500]:
        try:
            text=res.text.encode(enc).decode('utf-8')
        except:
            try:
                text=res.text.encode(enc).decode('gbk')
            except:
                pass
        try:
            html = etree.HTML(text)
            Title = html.findtext('.//title')
            title = Title if Title !=None else 'Null'
            if None == server:
                server = 'Null'
            ctext = get_context(text)
            if None == ctext:
                ctext ='Null'
        except:
            title="Null"
        result = '{}[+]{}{}{}{}{}{}'.format(Color.OKGREEN,url.ljust(36),str(code).ljust(10),server.ljust(20),title[:20].ljust(30),''.join(ctext.split()).ljust(20),Color.ENDC)
        print('\r{0}'.format(result))
        #print(url+split+str(code)+split+server+split+title+split+ctext)
        #return str(url)+split+str(code)+split+server+split+title
        return result
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
# 随机UA
def get_user_agent():
  user_agents = [
      "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",]
  return random.choice(user_agents)

# 获取服务器容器
def get_url_server(resp):
    try:
        for k in resp.headers.keys():
          if k.upper() == 'SERVER':
            header_server = resp.headers[k].upper()
        return header_server
    except:
        return 'Unkonw'



# 获取服务器容器  格式化
def get_url_servers(resp):
    try:
        for k in resp.headers.keys():
            if k.upper() == 'SERVER':
                header_server = resp.headers[k].upper()
                if re.search('iis/6.0'.upper(), header_server):
                  short_server = 'IIS/6.0'
                elif re.search('iis/7.0'.upper(), header_server):
                  short_server = 'IIS/7.0'  
                elif re.search('iis/7.5'.upper(), header_server):
                  short_server = 'IIS/7.5'    
                elif re.search('iis/8.0'.upper(), header_server):
                  short_server = 'IIS/8.0'   
                elif re.search('iis/8.5'.upper(), header_server):
                  short_server = 'IIS/8.5'  
                elif re.search('iis'.upper(), header_server):
                  short_server = 'IIS'  
                elif re.search('apache'.upper(), header_server):
                  short_server = 'Apache' 
                elif re.search('nginx'.upper(), header_server):
                  short_server = 'Nginx' 
                elif re.search('vWebServer'.upper(), header_server):
                  short_server = 'vWebServer' 
                elif re.search('openresty'.upper(), header_server):
                  short_server = 'OpebResty' 
                elif re.search('tengine'.upper(), header_server):
                  short_server = 'Tengine'  
                elif re.search('apusic'.upper(), header_server):
                  short_server = 'APUSIC' 
                elif re.search('marco'.upper(), header_server):
                  short_server = 'Marco'  
                elif re.search('twebap'.upper(), header_server):
                  short_server = 'TWebAP'     
                elif re.search('360'.upper(), header_server):
                  short_server = '360wzws'  
                elif re.search('cdn'.upper(), header_server):
                  short_server = 'CDN'          
                else:
                    short_server = get_url_server(resp)
            if k.upper() == 'SET-COOKIE':
                header_cookie = resp.headers[k]
                if 'rememberMe=deleteMe' in header_cookie:
                    short_server= 'shiro'
        return short_server
    except:
        return "Unkonw"


# 获取中间部分内容信息
# TODO: jenkins/weblogic/zabbix/shiro/elasticsearch/gitlab/shiro
def get_context(html):
    context = etree.HTML(html)
    for bad in context.xpath(".//script"):
        bad.getparent().remove(bad)
    for bad in context.xpath(".//style"):
        bad.getparent().remove(bad)
    content = context.xpath('string(.)').replace(" ","").replace("\n","")
    n = int(len(content)/2)
    ct =  content[n-20:n+20]
    return ct.strip()[:25]

# 提取url中的域名或IP
def url2Domain(line):
    if ("http://" in line) or ("https://" in line):
        return urlparse(line)[1]
    else:
        return line


# 域名转为ip
def Domain2Ip(host):
    try:
        ip=socket.getaddrinfo(host, None)[0][4][0]
        return ip
    except Exception as e:
        pass

# # C段识别
# def FindCsub(urls):
#     ipc = []
#     for url in urls:
#         ip=Domain2Ip(url2Domain(url))
#         if None != ip:
#             x =ip.rfind('.')
#             ip=ip[:x+1]+"0/24"
#             ipc.append(ip)
#     for value,count in Counter(ipc).most_common():
#         print(value, "-----------------",count)
#     return Counter(ipc).most_common()


# 将url转为C段ip地址表示
def Domain2Csub2(url):
    sys.stdout.write("\r[*]Recording to desolve {0} ...".format(url))
    ip=Domain2Ip(url2Domain(url))
    if '' != ip and None !=ip:
        x =ip.rfind('.')
        ip=ip[:x+1]+"0/24"
        return ip



class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[90m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\33[93m'
    WARNING = '\033[91m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


#多线程
class MyThread(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q

    def run(self):
        while not self.q.empty():
            getTitle2(self.q.get())

class FindCsubThread(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q
    def run(self):
        while not self.q.empty():
            IPCsubList.append(Domain2Csub2(self.q.get()))


def main():
    print(Color.OKYELLOW+banner+Color.ENDC)
    parser = argparse.ArgumentParser(description='攻防资产处理工具，用于简单处理筛选攻防前的有价值资产')
    parser.add_argument('-t','--thread',metavar='',type=int,default='10',help='线程参数')
    parser.add_argument('-f','--file',metavar='',default='',help='从文件读取')
    parser.add_argument('--mvdups',metavar='',default='',help='文本去重')
#    parser.add_argument('--mvdups2',metavar='',default='',help='去除file1中含有file2内容的部分，然后将两个文件合并')
    parser.add_argument('-c','--c',metavar='',default='',help='C段探测')
    args = parser.parse_args()

    target = args.file
    thread_nums = args.thread
    movdup = args.mvdups
    mvdups2 = args.mvdups2
    ip = args.ip
    print(target)

    if '' != target:
        with open(target,'r') as f:
            for line in f.readlines():
                lineQueue.put(line.strip())
                for p in port:
                    #print(line.strip()+":"+str(p))

                    urlQueue.put(line.strip()+":"+str(p))
        print("Queue OK! !")
        print("thread nums:",thread_nums,"!")
        print("识别C段IP中...")

        for j in range(thread_nums):
            CsubThreadList.append(FindCsubThread(lineQueue))
        for k in CsubThreadList:
            k.start()
        for m in CsubThreadList:
            m.join()
        if lineQueue.empty():
            for value,count in Counter(IPCsubList).most_common():
                if count >= 5 and None != value:
                    result = '{}[+]{}{}'.format(Color.OKYELLOW,value.ljust(50),count,Color.ENDC)
                    print('\r{0}'.format(result))
                    #print(value,"                                               ",count)


        for i in range(thread_nums):
            threadList.append(MyThread(urlQueue))
        for t in threadList:
            t.start()
        for l in threadList:
            l.join()

    if '' != movdup:
        MovDups(movdup)
    if '' !=ip:
        #ipl = ip.split('.')
        for i in range(1,254):
            x =ip.rfind('.')
            ip=ip[:x+1]+str(i)
            for p in port:
                urlQueue.put(ip.strip()+":"+str(p))
        print("Queue OK! !")
        print("thread nums:",thread_nums,"!")
        for i in range(thread_nums):
            threadList.append(MyThread(urlQueue))
        for t in threadList:
            t.start()
        for l in threadList:
            l.join()
if __name__ == '__main__':
    main()
    
















