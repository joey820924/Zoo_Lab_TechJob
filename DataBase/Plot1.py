# -*- coding: utf-8 -*-
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import OrderedDict
import sys
from datetime import datetime
reload(sys)
exec("sys.setdefaultencoding('utf-8')")  
assert sys.getdefaultencoding().lower() == "utf-8" 
sns.set(style='whitegrid')
path = '/Users/joey/Desktop/SJT.json'

TimeScore = defaultdict(int)
with open(path) as f:
    data = json.load(f)
    for i in data:
        Time = i['DateTime']
        #Score = i['TotalScore']
        TimeScore[Time] +=1 
TimeScore =  sorted(TimeScore.iteritems(),key = lambda x :x[0])  #將時間進行排序
ordered_dict = OrderedDict(TimeScore) #能排序的字典



    
    

def ShowTimeScore(TimeScore):
    Sorted_Time = []
    #Sorted_Score = []
    TimeCount = []
    for i in ordered_dict.items():
        TransTime = datetime.strptime(i[0], '%H:%M:%S')
        Sorted_Time.append(TransTime.time())
        TimeCount.append(i[1])
        #Sorted_Score.append(i[1])
    x = Sorted_Time
    y = TimeCount
    #y = Sorted_Score
    
    f,ax = plt.subplots(figsize=(10,6))
    sns.set_color_codes('pastel')
    sns.plt.plot(x,y ,label='Post_Time', color='blue')
    ax.legend(ncol=1, loc='upper right', frameon=True)
    ax.set(ylabel='Count',xlabel='Time',title='Post Time analyze')
    sns.despine(left=True, bottom=True)
    plt.show(f)
ShowTimeScore(TimeScore)