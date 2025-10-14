import json
import requests
from bs4 import BeautifulSoup

try:
    response = requests.get("https://spa4.scrape.center/api/news/?limit=10&offset=0")
    response.raise_for_status()

    data = response.json()

    for item in data['results']:
        print(f"\n{item['title']}\n新闻URL: {item['url']}")

        new_response = requests.get(item['url'])

        new_response.raise_for_status()

        soup = BeautifulSoup(new_response.content, 'lxml')

        content = soup.find_all('p', {'cms-style': 'font-L'})

        print("提取新闻正文内容:" if content else "404")
        for p in content:
            print(p.get_text().strip())

        print("-" * 50)

except BaseException as e:
    print("HTTP请求出错：", str(e))
    exit()





