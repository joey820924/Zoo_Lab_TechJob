''''
import requests
re=requests.get('https://www.ptt.cc/bbs/Tech_Job/index.html')
f = open('news.txt','a')
f.write(re.text.encode('utf-8')) 
print re.text.encode('utf-8')
'''

import requests
from bs4 import BeautifulSoup
re=requests.get('https://www.ptt.cc/bbs/Tech_Job/index.html')
#  print re.text.encode('utf-8')
soup=BeautifulSoup(re.text.encode('utf-8'), "html.parser")
for line in soup.select('.r-ent'):
    print line.select('.title')[0].text.encode('utf-8')
    print line.select('.date')[0].text.encode('utf-8'),line.select('.author')[0].text.encode('utf-8')
