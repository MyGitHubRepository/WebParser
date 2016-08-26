import urllib
from bs4 import BeautifulSoup

proxies = {'http': 'http://10.3.1.155:8080'}
page = urllib.urlopen('http://nightbot/buildslaves', proxies=proxies)

print 'RESPONSE:', page
print 'URL     :', page.geturl()

headers = page.info()
print 'DATE    :', headers['date']
print 'HEADERS :'
print '---------'
print headers

html = page.read()
print 'LENGTH  :', len(html)
print 'DATA    :'
print '---------'
print html

soup = BeautifulSoup(html, "html.parser")
#div = soup.find_all('table')
#div = soup.find_all(tbl_thmn="tbl_thmn")
#print(div)

html1 = soup.prettify("utf-8")
target = open("nightbot.txt", 'w')
target.truncate()
target.write(html1)
target.close()