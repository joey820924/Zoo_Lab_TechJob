# -*- coding: utf-8 -*-
import scrapy
from ipproxy.items import IpproxyItem

class IpsSpider(scrapy.Spider):
    name = "IPS"
    allowed_domains = ["xicidaili.com"]
    start_urls = ['http://www.xicidaili.com']

    def start_requests(self):
        reqs = []

        for i in range(1,3):
            req = scrapy.Request("http://www.xicidaili.com/nn/%s"%i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        ip_list = response.xpath('//table[@id="ip_list"]/tbody')
        trs = ip_list.xpath('//tr')[2:]
        items = []
        for ip in trs:
            pre_item = IpproxyItem()
            pre_item['IP'] = ip.xpath('td[2]/text()').extract()
            pre_item['PORT'] = ip.xpath('td[3]/text()').extract()
            pre_item['POSITION'] = ip.xpath('string(td[4])').extract()[0].strip()
            pre_item['TYPE'] = ip.xpath('td[6]/text()').extract()[0]
            pre_item['SPEED'] = ip.xpath('td[7]/div/@title').re('\d+\.d*')[0]
            pre_item['LAST_CHECK_TIME'] = ip.xpath('td[10]/text()').extract()[0]
            items.append(pre_item)
        return items

