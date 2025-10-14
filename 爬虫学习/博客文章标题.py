import bs4
from bs4 import BeautifulSoup
import requests

response = requests.get("https://lovepikachu.top/")
content = response.content.decode()

soup = BeautifulSoup(content, "lxml")

main = soup.find('main', id='main')
for div in main.find_all('div', recursive=False):  # type: bs4.element.Tag
    print(div.find('a', class_='shuoshuo-title').text.strip())

for article in main.find_all('article', recursive=False):
    print(article.find('span', class_='post-title').text.strip())
