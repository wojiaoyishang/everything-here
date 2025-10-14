import time

import requests
import winsound
from bs4 import BeautifulSoup
import datetime


while True:
    response = requests.get("https://www.zjzs.net/col/col155/index.html")
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    soup = BeautifulSoup(response.content.decode(), 'lxml')

    xml = soup.find("script", type="text/xml").contents[0]
    soup = BeautifulSoup(str(xml), 'lxml')
    if soup.find("record").find('a').text != "浙江省2025年普通高校招生艺术类统考批第一段平行投档分数线":
        print(f"[{formatted_time}]已更新文章！", soup.find("record").find('a').text)
        winsound.Beep(1000, 1000)
    else:
        print(f"[{formatted_time}]暂未更新")
    time.sleep(5)

