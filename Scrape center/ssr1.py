import re
import requests

response = requests.get('https://ssr1.scrape.center/')

text = response.content.decode('utf-8')

for match in re.findall(r'class="m-b-sm">(.*)</h2>', text):
    print(match)