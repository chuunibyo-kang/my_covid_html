import datetime
import hashlib
import pymysql
import time
import traceback
import requests
import json
from config import *
import re

from bs4 import *

def get_cdc_news_data():
    header = {'User-Agent':
                  r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}
    target_url = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_13141/'
    #发送网页请求
    response = requests.get(target_url, headers=header)
    #初始化BS4对象
    soup = BeautifulSoup(response.text, 'lxml')
    #获取昨日时间 
    yesterday_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).date().strftime('%Y-%m-%d')
    date_format = '[' + yesterday_date + ']'

    #获取最新一条消息的短链
    cdc_short_link = soup.find('div',"item-top-text")

    return response.text

get_cdc_news_data()
