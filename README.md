# bufferfly
渗透测试资产处理框架，对渗透测试前的信息搜集到的大批量资产进行处理的框架
![bufferfly](https://github.com/dropwiki/bufferfly/blob/master/bufferfly.png)
# 使用
渗透测试资产处理框架，对渗透测试前的信息搜集到的大批量资产进行处理的框架，可插件扩展 
python3 bufferfly.py -t 20 -g urls.txt 

1.高速资产存活检测，获取标题

2.资产去重：单文件去重，双文件去重

3.多线程支持

-t   --thread   设置线程数，若要设置，在第一个参数设置

-g   --gettitle 存活检测-获取url的title

-m   --mvdups   单文件去重

--mvdup2        双文件去重，去除文件1和文件2中共同的部分
  
# TODO
1. EXCEL支持，EXCEL处理导入导出

2. 插件化支持，使其可扩展

3. 在线化支持，提供网页可在线处理
