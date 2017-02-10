# -*- coding: utf-8 -*-
import MySQLdb
import json
import sys
reload(sys)
exec("sys.setdefaultencoding('utf-8')")  
assert sys.getdefaultencoding().lower() == "utf-8" 
def createJson():
    conn = MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = 'joey820924', db='Soft_Job',charset='utf8' )
    cursor = conn.cursor()
    sql = 'SELECT * FROM Soft_Job_Table'
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    
    column_list = [] 
    for i in fields:
        column_list.append(i[0])
    a = []
    with open('SJT.json','w+') as f:
        for row in data:
            result = {}
            result['ID'] = row[0]
            result['Title'] = str(row[1])
            result['Author'] = str(row[2])
            result['DateTime'] = str(row[3]).split(' ')[1] #因只想取時間而不要日期，所以用split分隔
            result['IP'] = str(row[4])
            result['Content'] = str(row[5])
            result['TotalScore'] = str(row[6])
            result['Url'] = str(row[7])
            a.append(result)  #將其包成list，讓json讀取時能一次讀
        jsondata = json.dumps(a,ensure_ascii=False,sort_keys=True)
        f.write(jsondata+'\n')
    f.close()
    #A = SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'Soft_Job_Comment'

if __name__ == '__main__':
    JsonData = createJson()
    
    