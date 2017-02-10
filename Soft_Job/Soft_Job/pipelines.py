# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb
from scrapy.crawler import Settings as settings

class SoftJobPipeline(object):
    def __init__(self):
        DBargs = dict(host = '127.0.0.1',db = 'Soft_Job',user = 'root',passwd = 'joey820924',charset = "utf8",cursorclass = MySQLdb.cursors.DictCursor,use_unicode=True)
        self.dbpool = adbapi.ConnectionPool('MySQLdb',**DBargs)

    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        return item
    def insert_into_table(self,conn,item):
        conn.execute('insert into Soft_Job_Table (ID,Title,Author,DateTime,IP,Content,TotalScore,Url) values(%s,%s,%s,%s,%s,%s,%s,%s)', (item['ID'],item['Title'],item['Author'],item['DateTime'],item['IP'],item['Content'],item['TotalScore'],item['Url']))
        conn.execute('insert into Soft_Job_Content (Content) values(%s)',(item['Content'],)) #測試用，將Content進行單一建表處理
