#-*-coding:utf-8-*-
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from pylab import mpl
import matplotlib

reload(sys)
exec("sys.setdefaultencoding('utf-8')")
token = u''' : ! ) , . : ; ? ] } ¢ ' " 、 。 〉 》 」 』 】 〕 〗 〞 ︰ ︱ ︳ ﹐ ､ ﹒ ﹔ ﹕ ﹖ ﹗ ﹚ ﹜ ﹞ ！ ） ， ． ： ； ？ ｜ ｝ ︴ ︶ ︸ ︺ ︼ ︾ ﹀ ﹂ ﹄ ﹏ ､ ～ ￠ 々 ‖ • · ˇ ˉ ―-- ′ ’ ” ( [ { £ ¥ ' " ‵ 〈 《 「 『 【 〔 〖 （ ［ ｛ ￡ ￥ 〝 ︵ ︷ ︹ ︻ 
︽ ︿ ﹁ ﹃ ﹙ ﹛ ﹝ （ ｛ “ ‘ -— _ … / - ~ < > = + @ * ／ → 1 2 3 / '''
Token = []
for i in token.split(' '):
    i = i.decode('utf-8')
    Token.append(i)
assert sys.getdefaultencoding().lower() == "utf-8"
with open('SJC.json') as f:
    datasSJC = json.load(f)
with open('SJT.json') as f:
    datas = json.load(f)
C_Words = []
C_Scores = []
for dataSJC in datasSJC:
    comment = dataSJC['Comment']
    if comment and dataSJC['Score'] !=0:
        CommentScore = defaultdict(int)
        comment = comment.replace(' ','')
        for wc in jieba.cut(comment):
            if wc not in Token:
                CommentScore[wc] +=1
        if len(CommentScore) > 0:
            C_Words.append(CommentScore)
            C_Scores.append(1 if int(dataSJC['Score']) else 0)

Words = []
Scores = []
for data in datas:
    WordScore = defaultdict(int)
    Content = data['Content']
    if data['TotalScore'] != 0:
        for setence in Content.split('\n'):
            setence = setence.replace(' ','')
            if setence:
                for word in jieba.cut(setence):
                    if word not in Token :
                        WordScore[word] += 1

        if len(WordScore) > 0:
            Words.append(WordScore)
            Scores.append(1 if int(data['TotalScore']) >0 else -1)
            
devc = DictVectorizer()
tfidf = TfidfTransformer()
x = tfidf.fit_transform(devc.fit_transform(Words))
c_devc = DictVectorizer()
c_tfidf = TfidfTransformer()
c_x = c_tfidf.fit_transform(c_devc.fit_transform(C_Words))
svc = LinearSVC()
svc.fit(x,Scores)
svcc = LinearSVC()
xc = svcc.fit(c_x,C_Scores)


c_svc = LinearSVC()
c_svc.fit(c_x, C_Scores)
def showContent(weights,names,top_n):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
    matplotlib.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
    Top_Features = sorted(zip(weights,names), key = lambda x: x[0],reverse=True)[:top_n]
    Top_Weights = [x[0] for x in Top_Features]
    Top_Names = [x[1] for x in Top_Features]
    fig, ax =plt.subplots(figsize = (10,8))
    count = np.arange(top_n)
    bars = ax.bar(count,Top_Weights,color='blue',edgecolor='black')
    for bar,w in zip(bars,Top_Weights):
        if w<0:
            bar.set_facecolor('red')
    width = 0.5
    ax.set_xticks(count+width)
    ax.set_xticklabels(Top_Names , rotation = 45, fontsize = 8 )
    #plt.show()
def showComment(weights,names,top_n):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
    matplotlib.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
    Top_Features = sorted(zip(weights,names), key = lambda x:x[0],reverse = True)[:top_n]
    Top_Weights = [x[0] for x in Top_Features]
    Top_Names = [x[1] for x in Top_Features]
    fig , ax = plt.subplots(figsize = (10,8))
    count = np.arange(top_n)
    bars = ax.bar(count,Top_Weights,color = 'blue',edgecolor='black')
    for bar,w in zip(bars,Top_Weights):
        if w<0:
            bar.set_facecolor('red')
    width = 0.5
    ax.set_xticks(count)
    ax.set_xticklabels(Top_Names,rotation = 45 ,fontsize = 8)
    plt.show()
#showContent(svc.coef_[0],devc.get_feature_names(),30)
showComment(svcc.coef_[0],c_devc.get_feature_names(),30)