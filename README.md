# bufferfly
攻防资产处理小工具，对攻防前的信息搜集到的大批量资产/域名进行存活检测、获取标题头、语料提取、常见web端口检测、简单中间识别，去重等，便于筛选有价值资产。

```python
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
5.C段web端口探测/获取标题
6.C段识别
7.shiro识别
8.简单中间件识别

适用用于外网资产梳理

TODO:
1.在不发送更多请求的情况下模糊识别weblogic/jboss/jenkins/zabbix/activeMQ/solr/gitlab/spring等
2.常见端口扫描(22/445/3389/3306/6379/1521等常见端口  与masscan、nmap结合)


```

![bufferfly](bufferflic.png)

# 使用
```
usage: bufferflic.py [-h] [-t] [-f] [--mvdups] [-c]

攻防资产处理工具，用于简单处理筛选攻防前的有价值资产

optional arguments:
  -h, --help      show this help message and exit
  -t , --thread   线程参数
  -f , --file     从文件读取
  --mvdups        文本去重
  -c , --c        C段探测

```

# DEFF

1. 添加C段探测
2. 添加C段识别
3. 添加shiro中间件检测
4. 修复一些显示BUG

# requirements

1. requests
2. lxml
3. argparse

```shell
pip3 install -r requirements.txt
```

# TODO

	1. 在不发送更多请求的情况下模糊识别weblogic/jboss/jenkins/zabbix/activeMQ/solr/gitlab/spring等
 	2. 常见端口扫描(22/445/3389/3306/6379/1521等常见端口  与masscan、nmap结合)

# help

主要是方便前期收集到的大量资产梳理的小工具，代码比较简陋，但还算实用。不要太相信Fofa。