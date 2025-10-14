# 爬取主页所有图片名字
from bs4.element import Tag
from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.umtuku.com/")
content = response.content.decode()

soup = BeautifulSoup(content, 'lxml')

for div in soup.find_all('div', attrs={'class': 'meta-title'}):  # type: Tag
    a: Tag = div.find('a')
    print(a.text)
