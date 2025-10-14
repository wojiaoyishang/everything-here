import time

import requests

cookies = {
    '5yh9l__v': '1',
    '5yh9l_t': '14',
    '5yh9l_cdn': 'https%3A%2F%2F23.224.199.26%3A63456%2Fxcdn3%2F',
    'pb8': 'szmzq0-34504b26',
    'c74': '4a32ba81',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.wuwusk.com',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.wuwusk.com/search/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    # 'cookie': '5yh9l__v=1; 5yh9l_t=14; 5yh9l_cdn=https%3A%2F%2F23.224.199.26%3A63456%2Fxcdn3%2F; pb8=szmzq0-34504b26; c74=4a32ba81',
}

data = {
    'keyword': '学姐',
}

response = requests.post('https://www.wuwusk.com/search/', cookies=cookies, headers=headers, data=data, allow_redirects=False)

print(response.headers.get('location'))
