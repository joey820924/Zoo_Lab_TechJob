# -*- coding: utf-8 -*-

import sys
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb
from scrapy.crawler import Settings as settings


class SoftJobPipeline(object):
    def __init__(self):
        DBargs = dict(host = '127.0.0.1',db = 'soft_job',user = 'soft_job',passwd = 'joey820924',charset = "utf8",cursorclass = MySQLdb.cursors.DictCursor,use_unicode=True)
        self.dbpool = adbapi.ConnectionPool('MySQLdb',**DBargs)
    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        return item
    def insert_into_table(self,conn,item):
            conn.execute('insert into soft_job_table (ID,Title,Author,DateTime,Content,TotalScore,Url) values(%s,%s,%s,%s,%s,%s,%s)', (item['ID'],item['Title'],item['Author'],item['DateTime'],item['Content'],item['TotalScore'],item['Url']))
            #conn.execute('insert into soft_job_content (Content) values(%s)',(item['Content'],)) #測試用，將Content進行單一建表處理
   