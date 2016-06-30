import requests
from bs4 import BeautifulSoup
import lxml
import collections

base_url = "http://wiscom.chd.edu.cn:8080/opac/item.php"
#s = requests.Session(base_url)
payload = {'marc_no':'0000198282'}
r = requests.get(base_url, params=payload)
base_soup = r.content.decode('utf-8')
soup = BeautifulSoup(base_soup, 'lxml')
test  = soup.find('dd')
title = test.a.string
test.a.decompose()
name  = test.string
filename = title + name
douban_url = soup.find_all('a',attrs={'target':'_blank'})
for url in douban_url:
    d_u = url.get('href')
    if not d_u.endswith('/'):
        continue
    douban = d_u

d = requests.get(douban)
d_soup = d.content.decode('utf-8')
douban_soup = BeautifulSoup(d_soup, 'lxml')
pic_url = douban_soup.find('a', attrs={'class':'nbg'})['href']
print(pic_url)

pic = requests.get(pic_url)
content = pic.content
print(type(content))
#print(content)
print(type(filename))
filename ="F:\myGit\Chd_Lib\\book" + filename +".jpg"
print(filename)
print(type(filename))
print(type('test.jpg'))
fh = open(filename, 'wb')
fh.write(content)
