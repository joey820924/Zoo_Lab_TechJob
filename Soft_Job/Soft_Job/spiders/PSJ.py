# -*- coding: utf-8 -*-
import scrapy
from Soft_Job.items import SoftJobItem
from datetime import datetime
import logging
import sys
import MySQLdb
import random

class PsjSpider(scrapy.Spider):
    name = "PSJ"  #爬蟲識別名
    allowed_domains = ["ptt.cc"]  
    start_urls = ['https://www.ptt.cc/bbs/Soft_Job/index1.html',]  #起始鏈結
    _Page = 0
    Max_Page = 1  #最多爬幾頁
    reload(sys)
    exec("sys.setdefaultencoding('utf-8')")  
    assert sys.getdefaultencoding().lower() == "utf-8" #設定編碼

    def parse(self, response):
        self._Page += 1
        for href in response.xpath('//div[@class="r-ent"]/div[@class="title"]/a/@href'):  #爬每頁的內文鏈結，並丟入parse_detail載入
            url = response.urljoin(href.extract())
            yield scrapy.Request(url,callback = self.parse_detail)

        if self._Page < PsjSpider.Max_Page:
            Next_Page = response.xpath(u'//div[@class="action-bar"]//a[contains(text(),"下頁")]/@href') #若小於最多爬取頁數，就爬取下個index網頁的鏈結
            if Next_Page:
                url = response.urljoin(Next_Page[0].extract()) 
                yield scrapy.Request(url,callback = self.parse)  #獲取下個index鏈結後，回傳給parse函數進行處理
            else:
                logging.warning('No more page')
        else:
            logging.warning('Max_Page reached')

    def parse_detail(self,response):
        Item = SoftJobItem()  #從items.py載入設定好的抓取目標item[]，把抓取的資料丟進指定的目標item[]
        Item['Title'] = response.xpath('//meta[@property="og:title"]/@content')[0].extract().encode('utf-8')
        Item['Author'] = response.xpath('//div[@class="article-metaline"]/span[2]/text()')[0].extract().split(' ')[0]
        datetime_str = response.xpath(u'//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[0].extract()
        Item['DateTime'] = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y') #轉換成指定的日期格式
        #Item['IP'] = response.xpath(u'//div[@id="main-content"]/span[contains(text(),"發信站")]/text()').re('\d+\.\d+\.\d+\.\d+')
        content = ''
        for i in response.xpath('//div[@id="main-content"]/text()').extract():  #因原始碼問題，因此要進行字串連接的處理
            content+=i
        content = content.replace(' ',"")
        Item['Content'] = str(content)
        Item['Url'] = response.url
        ran = random.randint(0,99)
        a = response.url.split('.')[-4]  #獲取index值，並作為資料表名稱
        a = 'Soft_Job_'+a #Mysql的資料表命名必須要以英文開頭，不能以數字開頭
        conn = MySQLdb.connect(host = '140.118.110.90',port = 12345,user = 'soft_job',passwd = 'joey820924',db = 'soft_job_comment',charset = 'utf8')  #資料庫連接
        cursor = conn.cursor() #獲得資料庫指標
        Item['ID'] = a
        

        
        
        Total_Score = 0
        
        for comment in response.xpath('//div[@class="push"]'):
            if comment.xpath('span[3]/a/text()'):  #因原始碼問題，因此要對comment進行以下處理
                Push_Comment = comment.xpath('span[3]/a/text()')[0].extract()
            else:
                Push_Comment = comment.xpath('span[3]/text()')[0].extract()
             
            Push_User = comment.xpath('span[2]/text()')[0].extract()
            Push_Tag = comment.xpath('span[1]/text()')[0].extract()
            if u'推' in Push_Tag:
                score = 1

            elif u'噓' in Push_Tag:
                score = -1

            else:
                score = 0
            
            Total_Score += score #此篇文章的總分數
            Item['User'] = Push_User
            Item['Comment'] = Push_Comment
            Item['Score'] = score #單一用戶的推文分數
            sql = 'CREATE TABLE IF NOT EXISTS '+a+'(User varchar(255),Comment varchar(255),Score varchar(255))'  #創建comment資料表
            cursor.execute(sql) #執行sql語法
            sql1 = 'insert into '+a+' (User,Comment,Score) values(%s,%s,%s)'
            cursor.execute(sql1,(Push_User,Push_Comment,score))
            #Comments.append({'User':Push_User,'Comment':Push_Comment,'Score':score})
        Item['TotalScore'] = Total_Score
        yield Item
        
        

