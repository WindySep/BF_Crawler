'''
@Project ：BilibiliFans 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：H。R。Y
@Date    ：2023/10/8 17:04 
'''
from crawler import Crawler

# 输入目标的UID，作为一个字符串
uid = str(input("输入查询用户的UID："))
# uid = '2070667222'

Crawler.crawler(uid)