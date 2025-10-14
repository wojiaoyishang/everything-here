import bs4
from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.juzikong.com/works/15d86c22-8e3d-42c2-b9f2-133facb5b85c", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'})

content = response.content.decode()

soup = BeautifulSoup(content, 'lxml')
