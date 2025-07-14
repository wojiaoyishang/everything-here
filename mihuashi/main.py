import requests
#
# cookies = {
#     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22197e7f83e061b82-06f2cbd1158fc48-4c657b58-1821369-197e7f83e072ac6%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3ZTdmODNlMDYxYjgyLTA2ZjJjYmQxMTU4ZmM0OC00YzY1N2I1OC0xODIxMzY5LTE5N2U3ZjgzZTA3MmFjNiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
#     'aliyungf_tc': '4329044d007aaccc3d39ad29461c6c1739e3820da1dd11a852e18b3aa4d4c5e8',
# }

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'authorization': 'Bearer null',
    'cache-control': 'no-cache',
    'm-s': 'fnfruRIiSYGk_42RF1iUmV0btJVVthTQv1mfMdTLjh2a0IDM2IDNxcDM30mba9WR4gDZ+VUb9ADO5UWcHZlVSdGRNRXTnZjUExDP',
    'm-t': '1752327415',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    'web-version': 'frontend',
    # 'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22197e7f83e061b82-06f2cbd1158fc48-4c657b58-1821369-197e7f83e072ac6%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3ZTdmODNlMDYxYjgyLTA2ZjJjYmQxMTU4ZmM0OC00YzY1N2I1OC0xODIxMzY5LTE5N2U3ZjgzZTA3MmFjNiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; aliyungf_tc=4329044d007aaccc3d39ad29461c6c1739e3820da1dd11a852e18b3aa4d4c5e8',
}

params = {
    'page': '1',
    'type': 'recent',
}

response = requests.get('/api/v1/artworks/search', params=params,  headers=headers)

print(response.json())