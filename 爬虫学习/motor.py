import os
import httpx
import pandas as pd
import asyncio
import pickle

import logging

from rich.logging import RichHandler

from rich.progress import Progress
from rich.progress import track

from bs4 import BeautifulSoup

logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

client = httpx.AsyncClient(headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.mlp-motor.com/list/?9_1.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Microsoft Edge";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': 'ASPSESSIONIDSEQBTBCT=DCPBMDFDNPJJEHICGJNHGIJI',
}, proxies={
    "http://": "http://localhost:7890",
    "https://": "http://localhost:7890"
}, timeout=30)

os.makedirs("./result", exist_ok=True)
os.makedirs("./result/网页缓存", exist_ok=True)


async def get_list(product_type: str, page: int) -> dict:
    """
    获取产品列表，并返回该页面所有产品
    """
    full_url = f'https://www.mlp-motor.com/list/?{product_type}_{page}.html'

    response = await client.get(full_url)

    response.raise_for_status()

    soup = BeautifulSoup(response.content.decode(), 'lxml')

    result = []
    product_ul = soup.find('ul', id='Pro_ul_list')
    for index, li in enumerate(product_ul.find_all('li')):  # type: BeautifulSoup
        product_url = 'https://www.mlp-motor.com' + li.find('a').attrs.get('href')
        product_name = li.find('a').attrs.get('title')
        product_image = li.find('img').attrs.get('src')

        if product_name is None:
            logging.warning(f"页面 {full_url} 第 {index + 1} 个产品没有找到产品名称，跳过该产品获取。")
            continue

        if product_url is None:
            logging.warning(f"页面 {full_url} {product_name} 产品没有找到产品链接，跳过该产品获取。")
            continue

        if product_image.strip() == "/Images/nopic.gif":
            product_image = None

        result.append({
            'product_url': product_url,
            'product_name': product_name,
            'product_image': product_image
        })

    return result


async def build_index():
    """
    构建需要爬取的所有产品索引
    """
    if os.path.exists("./result/所有产品索引.xlsx"):
        index_df = pd.read_excel("./result/所有产品索引.xlsx")
    else:
        index_df = pd.DataFrame(columns=["产品链接", "产品名称", "产品头图"])

    if os.path.exists("./result/index_status.pickle"):
        with open('./result/index_status.pickle', 'rb') as f:
            status_recoder = pickle.load(f)
    else:
        status_recoder = set()

    # 批量 GET 产品
    async def get_batch(product_type: str, page_range: tuple):
        logging.info(f"构建产品获取索引已开始，目标产品类型 {product_type} ......")

        for page in range(page_range[0], page_range[1] + 1):
            logging.info(
                f"构建 {product_type} 类型第 {page} 页 ({page}/{page_range[1]} {page / page_range[1] * 100:.2f}%)"
            )

            await asyncio.sleep(0.1)

            retry_times = 0

            while retry_times < 5:

                try:

                    if (product_type, page) in status_recoder:
                        logger.info("此项已完成，跳过。")
                        continue

                    for data in await get_list(product_type, page):
                        index_df.loc[len(index_df)] = {
                            "产品链接": data['product_url'],
                            "产品名称": data['product_name'],
                            "产品头图": data['product_image'] if data['product_image'] else ""
                        }

                    # 记录已完成状态
                    status_recoder.add((product_type, page))
                    with open("./result/index_status.pickle", "wb") as file:
                        pickle.dump(status_recoder, file)
                    index_df.to_excel("./result/所有产品索引.xlsx", index=False)

                    break
                except Exception as e:
                    retry_times += 1
                    logger.error(f"获取 {product_type} 类型第 {page} 页出现错误，将在 3 秒之后重试。" + str(e))
                    await asyncio.sleep(3)

    await asyncio.gather(
        get_batch("6", (1, 96)),
        get_batch("9", (1, 7)),
        get_batch("7", (1, 5))
    )

    index_df.to_excel("./result/所有产品索引.xlsx", index=False)


async def build_cache():
    """
    从索引里获取到所有产品页面的原 HTML 数据，便于之后二次处理和筛查
    """
    index_df = pd.read_excel("./result/所有产品索引.xlsx")

    logging.info(f"一共 {len(index_df)} 条产品记录。")

    with Progress() as progress:
        task = progress.add_task(f"[cyan]构建页面缓存...(0/{len(index_df)})", total=len(index_df))

        sem = asyncio.Semaphore(5)  # 同时进行五个异步任务

        async def get_page(url: str, name: str):

            try_times = 0

            while try_times < 5:

                try:

                    logging.info(f"正在缓存页面 ({name}){url} ......")

                    if os.path.exists(f"./result/网页缓存/{url[url.rfind('?') + 1:]}"):
                        logging.info(f"页面 ({name}){url} 已经被缓存，跳过。")
                        progress.update(task, advance=1)
                        return

                    response = await client.get(url)
                    response.raise_for_status()

                    with open(f"./result/网页缓存/{url[url.rfind('?') + 1:]}", "wb") as f:
                        f.write(response.content)

                    break

                except BaseException as e:
                    logging.info(f"页面 ({name}) {url} 缓存失败，将在 3 秒之后重试。" + str(e))
                    try_times += 1

                    await asyncio.sleep(3)

            progress.update(task, advance=1,
                            description=f"[cyan]构建页面缓存...({progress.tasks[task].completed}/{progress.tasks[task].total})")

        async def limit_get(url: str, name: str):
            async with sem:
                await get_page(url, name)

        tasks = []

        for index, row in index_df.iterrows():
            url = row['产品链接']
            name = row['产品名称']

            tasks.append(asyncio.create_task(limit_get(url, name)))

        await asyncio.gather(*tasks)


async def parse_page(soup: BeautifulSoup):
    """
    解析网页提取信息
    """
    result = {}

    show_title = soup.find("div", class_="show_title")

    if show_title is None:
        raise RuntimeError("该页面的产品名称为空。")

    result['Product Name'] = show_title.text.strip()

    # 获取各个参数
    for li in soup.find('ul', class_='parameter').find_all('li'):
        # 标签对应内容
        tage = li.find('span').text.strip(":")
        meta = li.find('span').nextSibling.text.strip()
        result[tage] = meta

    # 获取下方产品详情
    tabs_name = []
    for li in soup.find('ul', class_='ParameterNav').find_all('li'):
        tabs_name.append(li.find('a').text.strip())

    tabs_info = []
    for div in soup.find('div', class_='ParameterNavTab').find_all('div', class_='arameterNav_nr'):
        text = ""
        for p in div.find_all(recursive=False):  # 获取所有子元素
            text += p.text.strip() + '\n'
        tabs_info.append(text.strip())

    result.update(dict(zip(tabs_name, tabs_info)))

    result['Images URL'] = []

    # 获取图片列表
    for li in soup.find('div', id="preview").find('ul', class_="list-h").find_all('li'):
        img_ele = li.find('img')  # type: BeautifulSoup

        if img_ele is None:
            continue

        result['Images URL'].append(img_ele.attrs.get('src'))

    return result


async def build_product_index():
    """
    构造完整产品的表格，同时构造图片的下载地址和下载目标文件夹，由于图片下载是大流量的，所以需要分开。
    """
    index_df = pd.DataFrame(columns=[
        'Product ID',
        'Product Name',
        'Product URL',
        'Loading Poit',
        'Supply Ability',
        'Guarantee',
        'Payment Terms',
        'Min.Order Quantity',
        'Product Details',
        'Technical Parameters',
        'Use in vehicles',
        'Technical drawings',
        'OEM & Application',
        'R&D Center',
        'Quality control',
        'Video Introduction',
        'honor certificate',
        'Images URL'
    ])

    image_map_file = open("./result/图片下载索引文件.txt", "w", encoding="utf-8")

    for filename in track(os.listdir("./result/网页缓存"), description="构建产品数据中......"):
        if filename.endswith(".html"):
            filepath = f"./result/网页缓存/{filename}"
            product_id = filename[:filename.index(".")]
            product_url = f"https://www.mlp-motor.com/?{filename}"

            logging.info(f"处理产品数据 {product_id} ...")

            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "lxml")
                result = await parse_page(soup)

                result['Product ID'] = product_id
                result['Product URL'] = product_url

                # 建立图片下载索引
                for image_url in result['Images URL']:
                    image_filename = image_url[image_url.rfind('/') + 1:]
                    image_map_file.write(f"{image_url} ./result/产品图片/{product_id}/{image_filename}\n")

                result['Images URL'] = "\n".join(["https://www.mlp-motor.com" + url for url in result['Images URL']])

                index_df.loc[len(index_df)] = result

    index_df.to_excel("./result/所有产品详细信息.xlsx", index=False)
    image_map_file.close()

    logging.info("成功构建所有产品详细信息索引数据。")


async def download_images():
    """
    根据图片索引下载所有图片
    """
    images_map = {}

    client.headers.pop("Cookie")  # 去掉 Cookie

    with open("./result/图片下载索引文件.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.split(" ")
            images_map["https://www.mlp-motor.com" + line[0]] = line[1].strip()  # 下载 url + 保存位置

    logging.info("图片索引读取完毕，准备下载图片...")

    with Progress() as progress:

        task = progress.add_task(f"[cyan]下载产品图片...(0/{len(images_map)})", total=len(images_map))

        async def download_image(key, value):

            if os.path.exists(value):
                logging.info(f"图片 {key} -> {value} 已经下载，跳过。")
                progress.update(task,
                                advance=1,
                                description=f"[cyan]下载产品图片...({progress.tasks[task].completed}/{len(images_map)})")
                return

            logging.info(f"下载图片 {key} -> {value}。")

            try_times = 0
            while try_times < 5:
                try:

                    response = await client.get(key)

                    if response.status_code == 404:
                        with open(value, "wb") as f:
                            logging.warning(f"产品图片 {key} 失效，跳过。")
                            f.write(b"404 Not Found")
                        break

                    response.raise_for_status()

                    # 创建目录
                    os.makedirs(os.path.dirname(value), exist_ok=True)

                    with open(value, "wb") as f:
                        f.write(response.content)

                    break

                except BaseException as e:
                    logging.error(f"下载产品图片 {key} 失败，将在 3 秒之后重试。" + str(e))
                    try_times += 1

                    await asyncio.sleep(3)

            progress.update(task,
                            advance=1,
                            description=f"[cyan]下载产品图片...({progress.tasks[task].completed}/{len(images_map)})")

        sem = asyncio.Semaphore(5)  # 五个并发

        async def limit_get(key, value):
            async with sem:
                await download_image(key, value)
                await asyncio.sleep(0.1)

        tasks = [limit_get(key, value) for key, value in images_map.items()]

        await asyncio.gather(*tasks)


async def main():
    # await build_index()  # 建立产品索引
    # await build_cache()
    # await build_product_index()
    await download_images()

    pass


if __name__ == '__main__':
    asyncio.run(main())
