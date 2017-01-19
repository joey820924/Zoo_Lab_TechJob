# -*- coding: utf-8 -*-
import scrapy
from Soft_Job.items import SoftJobItem
from datetime import datetime
import logging

class PsjSpider(scrapy.Spider):
    name = "PSJ"
    allowed_domains = ["ptt.cc"]
    start_urls = ['https://www.ptt.cc/bbs/Soft_Job/index.html',]
    _Page = 0
    Max_Page = 3

    def parse(self, response):
        self._Page += 1
        for href in response.xpath('//div[@class="r-ent"]/div[@class="title"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url,callback = self.parse_detail)
        if self._Page < PsjSpider.Max_Page:
            Next_Page = response.xpath(u'//div[@class="action-bar"]//a[contains(text(),"上頁")]/@href')
            if Next_Page:
                url = response.urljoin(Next_Page[0].extract())
                yield scrapy.Request(url,callback = self.parse)
            else:
                logging.warning('No more page')
        else:
            logging.warning('Max_Page reached')

    def parse_detail(self,response):
        Item = SoftJobItem()
        Item['Title'] = response.xpath('//meta[@property="og:title"]/@content')[0].extract()
        Item['Author'] = response.xpath('//div[@class="article-metaline"]/span[2]/text()')[0].extract().split(' ')[0]
        datetime_str = response.xpath(u'//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[0].extract()
        Item['DateTime'] = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')
        Item['IP'] = response.xpath(u'//div[@id="main-content"]/span[contains(text(),"發信站")]/text()').re('\d+\.\d+\.\d+\.\d+')
        Item['Content'] = response.xpath('//div[@id="main-content"]/text()')[0].extract()
        Item['Url'] = response.url

        Total_Score = 0
        Comments = []
        for comment in response.xpath('//div[@class="push"]'):
            Push_Comment = comment.xpath('span[3]/text()')[0].extract()
            Push_User = comment.xpath('span[2]/text()')[0].extract()
            Push_Tag = comment.xpath('span[1]/text()')[0].extract()
            if u'推' in Push_Tag:
                score = 1
            elif u'噓' in Push_Tag:
                score = -1
            else:
                score = 0
            Total_Score += score
            Comments.append({'User':Push_User,'Comment':Push_Comment,'Score':score})

        Item['Comment'] = Comments
        Item['Score'] = Total_Score
        yield Item
        
        

