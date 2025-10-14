# 爬取 https://tzuqiu.cc/stats.do 中的球队排名数据， 存在 User-Agent 校验
import bs4
import requests
from bs4 import BeautifulSoup

response = requests.get("https://tzuqiu.cc/stats.do", headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'})
content = response.content.decode('utf-8')

soup = BeautifulSoup(content, 'lxml')

table = soup.find('table', id="teamStatSummary")  # type: bs4.element.Tag
tbody = table.find('tbody')  # type: bs4.element.Tag
for i, tr in enumerate(tbody.find_all('tr')):  # type: bs4.element.Tag
    td = tr.find('td').findNext()
    print(i + 1, td.text.strip())
