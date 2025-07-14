import copy
import json

from bs4 import BeautifulSoup
from readmdict import MDX

filename = "现汉7.mdx"
all_data = []
all_data_map = {}  # 拿来做规划，不然不好定位 LINK

wait_for_link = {}  # 有一部分生僻字通假，元数据中直接使用 @@@LINK 作为标记，这里备用

for head, item in MDX(filename).items():
    # 解码两者
    head = head.decode("utf-8").strip()
    item = item.decode("utf-8").strip()

    if item[:8] == "@@@LINK=":
        wait_for_link[head] = item[8:]
        continue

    html = BeautifulSoup(item, "lxml")

    tidy_data = {
        "head": head
    }

    # entry = html.find("entry")
    # if entry is None:
    #     continue
    #
    # for tag in entry.find_all():
    #     if tag.name != "hwg":
    #         tidy_data[tag.name] = tag.text.strip()

    # 对每个进行整理划分

    # 找所有图片
    # tidy_data['images'] = []
    # for img_html in html.find_all("img"):
    #     tidy_data['images'].append(img_html.attrs["src"])

    # 汉文
    if html.find('hw'):
        tidy_data['hw'] = html.find("hw").text.strip()
    else:
        # tidy_data['hw'] = ""
        continue

    # 拼音
    if html.find('pinyin'):
        tidy_data['pinyin'] = html.find("pinyin").text.strip()
    else:
        tidy_data['pinyin'] = ""

    # 定义
    tidy_data['def'] = []
    tidy_data['note'] = []
    for def_ in html.find_all('def'):
        ps_tag = def_.find("ps")
        if ps_tag:
            ps_content = ps_tag.get_text(strip=True)
            remaining_text = ""
            for sibling in ps_tag.next_siblings:
                remaining_text += sibling.text.strip()

            if def_.find("num"):
                tidy_data['def'].append(def_.find("num").get_text(strip=True) + f" [{ps_content}] " + remaining_text)
            else:
                tidy_data['def'].append(f"[{ps_content}] " + remaining_text)

        else:
            tidy_data['def'].append(def_.text.strip())

        # 检查一下下一个元素是不是 column ，如果是就加到 note 中
        if def_.next_sibling and def_.next_sibling.name == "column":
            remaining_text = ""
            note = def_.next_sibling.find('note')
            for sibling in note.next_siblings:
                remaining_text += sibling.text.strip()
            tidy_data['note'].append(remaining_text)
        else:
            tidy_data['note'].append("")


    # 注意
    # tidy_data['note'] = []
    # for note in html.find_all('note'):
    #     remaining_text = ""
    #     for sibling in note.next_siblings:
    #         remaining_text += sibling.text.strip()
    #     tidy_data['note'].append(remaining_text)

    # 关联词语
    tidy_data['relative'] = []
    if html.find('ci'):
        for a in html.find_all('a'):
            tidy_data['relative'].append(a.text.strip())

    all_data_map[head] = len(all_data)
    all_data.append(tidy_data)

# 在所有基本数据处理完成之后，将 LINK 写回
for head, target in wait_for_link.items():
    data = copy.deepcopy(all_data[all_data_map[target]])
    data['head'] = head
    data['hw'] = f"{head}（{target}）"
    all_data.append(data)

with open("现汉7.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)
