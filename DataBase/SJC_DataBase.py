# -*- coding: utf-8 -*-
import MySQLdb
import json
import sys
import os
reload(sys)
exec("sys.setdefaultencoding('utf-8')")  
assert sys.getdefaultencoding().lower() == "utf-8" 
def GetTableName():
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='joey820924',db='Soft_Job_Comment',charset='utf8')
    cursor = conn.cursor()
    sql = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = "Soft_Job_Comment"'  #取得相對應的ID以取得Soft_Job_Comment內的資料
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    with open('TABLE_NAME.json','w+') as f: #w+是打開後清空裡面資料，可讀可寫，若檔案不存在則建立
        for row in data:
            result = {}
            result['TABLE_NAME'] = str(row[0])
            jsondata = json.dumps(result,ensure_ascii=False)
            f.write(jsondata+'\n')
    f.close()
    
    
    
def createJson():
    conn = MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = 'joey820924', db='Soft_Job_Comment',charset='utf8' )
    cursor = conn.cursor()
    path = '/Users/joey/Desktop/TABLE_NAME.json'
    if os.path.exists('SJC.json'):
        os.remove('SJC.json')
    file = open(path,'r')
    for line in file.readlines():  #因json讀取一次只能讀取一組，所以當有很多時就必須要分行讀取，不然就是要在最開始建立json檔時就要把它包成一個list
        dic = json.loads(line)
        TableName = str(dic['TABLE_NAME'])
        sql = 'SELECT * FROM '+TableName
        cursor.execute(sql)
        data = cursor.fetchall()
        fields = cursor.description
        column_list = [] 
        for i in fields:
            column_list.append(i[0])
        
        a = []
        with open('SJC.json','w+') as f:  #a 是 append的意思
            for row in data:
                result = {}
                result['User'] = str(row[0])
                result['Comment'] = str(row[1])
                result['Score'] = str(row[2])
                a.append(result)
            jsondata = json.dumps(a,ensure_ascii=False,sort_keys=True)
            f.write(jsondata+'\n')
    #A = SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'Soft_Job_Comment'

if __name__ == '__main__':
    GetTable = GetTableName()
    JsonData = createJson()
    
    