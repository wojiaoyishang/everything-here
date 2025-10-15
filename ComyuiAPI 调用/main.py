import os
import json
import time

import requests

from flask import Flask, send_file, request

if not os.path.exists('./save'):
    os.mkdir('./save')

queue = []

BASE_URL = "https://c-1978251476767354881.ksai.scnet.cn:58043"

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'no-cache',
    'Comfy-User': '',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://c-1978251476767354881.ksai.scnet.cn:58043',
    'Pragma': 'no-cache',
    'Referer': 'https://c-1978251476767354881.ksai.scnet.cn:58043/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0',
    'sec-ch-ua': '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2222054924066%22%2C%22first_id%22%3A%221971b6a2a08c87-063596827e477f4-4c657b58-1821369-1971b6a2a0926f5%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22zy%22%2C%22%24latest_utm_medium%22%3A%22zy%22%2C%22%24latest_utm_campaign%22%3A%222504act%22%2C%22%24latest_utm_content%22%3A%22landp%22%2C%22%24latest_utm_term%22%3A%22custservwind%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3MWI2YTJhMDhjODctMDYzNTk2ODI3ZTQ3N2Y0LTRjNjU3YjU4LTE4MjEzNjktMTk3MWI2YTJhMDkyNmY1IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjIwNTQ5MjQwNjYifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2222054924066%22%7D%2C%22%24device_id%22%3A%221971b6a2a08c87-063596827e477f4-4c657b58-1821369-1971b6a2a0926f5%22%7D; _ga=GA1.1.1340730244.1749287643; _ga_R1FN4KJKJH=GS2.1.s1749303307$o3$g1$t1749303308$j59$l0$h0; Hm_lvt_0fe323929429a55a4d13bccce9540f31=1760193424,1760230340,1760344444,1760435089',
}


def generate_workflow_api(prompt):

    if prompt.startswith("皮卡丘："):
        with open('./workflow.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        with open('./workflow2.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

    data['prompt']['2']['inputs']['prompt'] = prompt

    return data


def request_prompt(workflow_api):
    # 请求 prompt
    response = requests.post(f"{BASE_URL}/api/prompt", json=workflow_api, headers=headers)
    response.raise_for_status()

    prompt_id = response.json()['prompt_id']

    while True:
        time.sleep(1)
        response = requests.get(f"{BASE_URL}/api/history?max_items=64", headers=headers)
        response.raise_for_status()

        data = response.json()

        if prompt_id in data:
            break

    data = data[prompt_id]
    filename = data['outputs']['8']['images'][0]['filename']

    params = {
        'filename': filename,
        'subfolder': '',
        'type': 'output',
        'rand': '0.7626782563449418',
    }

    response = requests.get(
        'https://c-1978251476767354881.ksai.scnet.cn:58043/api/view',
        params=params,
        headers=headers,
    )

    with open(f'./save/{filename}', 'wb') as f:
        f.write(response.content)

    return filename


def get_image_filename(prompt):
    if not os.path.exists('./save.json'):
        with open('./save.json', 'w', encoding='utf-8') as f:
            f.write("{}")

    while prompt in queue:
        time.sleep(1)

    with open('./save.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if prompt not in data:
        queue.append(prompt)
        filename = request_prompt(generate_workflow_api(prompt))
        queue.remove(prompt)
    else:
        return data[prompt]

    data[prompt] = filename

    with open('./save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return filename


app = Flask(__name__)


@app.route('/image')
def image():
    t = time.time()
    prompt = request.args.get('prompt')
    if prompt is None:
        return ''

    filename = get_image_filename(prompt)
    print(time.time() - t)
    return send_file(f'./save/{filename}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7383)

# t = time.time()
# print(request_prompt(generate_workflow_api("这个角色在跳舞，保持画风不变")))
# print(time.time() - t)
