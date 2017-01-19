import requests
re=requests.get('https://www.ptt.cc/bbs/Tech_Job/index.html')
f = open('news.txt','a')
f.write(re.text.encode('utf-8')) 
print re.text.encode('utf-8')