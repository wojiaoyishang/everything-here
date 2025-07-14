import csv
import json

all_strings = {}

# 使用 with 确保文件正确关闭
with open("aliya.bytes", "r", encoding="utf-8") as origin_csv:
    reader = csv.reader(origin_csv)

    # 跳过第一行（标题）
    next(reader)

    all_data = []

    for row in reader:
        if not row:  # 跳过空行
            continue

        key = row[0]  # 第一个 key
        data = row[2]  # 回答内容

        data = data.replace("{$name}", "玩家").replace("\\n", "\n")

        all_strings[key] = data
        all_strings[key[:-1]] = data

all_strings["PlayerEmpty"] = "[登录系统]"
all_strings["AliyaEmpty"] = "[对方已下线]"


def get_string(d):
    if isinstance(d, str):
        if d not in all_strings:
            return d
        return all_strings[d]
    s = ""
    for i in d:
        s += all_strings[i] + "\n\n"
        s += "---\n\n"

    s = s.strip("-\n")
    return s


flows = [
    # 情节1：苏醒后的重逢（First Wake）
    [
        "PlayerEmpty",
        "AliyaMessage.First Wake.4.",
        "PlayerChoice.First Wake.6.",
        "AliyaMessage.First Wake.8.",
        "PlayerChoice.First Wake.9.",
        "AliyaMessage.First Wake.12.",
        "PlayerChoice.First Wake.14.",
        "AliyaEmpty"
    ],

    # 情节2：中秋节对话（Mid-Autumn Festival）
    [
        "PlayerEmpty",
        "AliyaMessage.Mid-Autumn_Festival.1.",
        "PlayerChoice.Mid-Autumn_Festival.3.",
        ("AliyaMessage.Mid-Autumn_Festival.10.", "AliyaMessage.Mid-Autumn_Festival.12."),
        "PlayerChoice.Mid-Autumn_Festival.14.",
        "AliyaMessage.Mid-Autumn_Festival.19.",
        "PlayerChoice.Mid-Autumn_Festival.20.",
        ("AliyaMessage.Mid-Autumn_Festival.22.", "AliyaMessage.Mid-Autumn_Festival.24."),
        "PlayerChoice.Mid-Autumn_Festival.26.",
        "AliyaEmpty"
    ],

    # 情节3：氧气危机与救援（O2RunOut2）
    [
        "PlayerEmpty",
        ("AliyaMessage.O2RunOut2.4.", "AliyaMessage.O2RunOut2.6.", "AliyaMessage.O2RunOut2.35."),
        "PlayerChoice.O2RunOut2.16.",
        "AliyaMessage.O2RunOut2.21.",
        "PlayerChoice.O2RunOut2.23.",
        ("AliyaMessage.O2RunOut2.27.", "AliyaMessage.O2RunOut2.28.", "AliyaMessage.O2RunOut2.30."),
        "[急救措施启动]",
        "AliyaEmpty"
    ]
]
for flow_keys in flows:

    with open("conversations.json", "r", encoding="utf-8") as conversations_json:
        pre_conversation = json.load(conversations_json)

    new_conversation = {
        "instruction": "",
        "input": "",
        "output": "",
        "history": []
    }

    new_conversation["output"] = get_string(flow_keys[-1])
    new_conversation["instruction"] = get_string(flow_keys[-2])

    for i in range(0, len(flow_keys) - 2, 2):
        new_conversation['history'].append(
            [
                get_string(flow_keys[i]),
                get_string(flow_keys[i + 1]),
            ]
        )

    pre_conversation.append(new_conversation)

    with open("conversations.json", "w", encoding="utf-8") as conversations_json:
        conversations_json.write(json.dumps(pre_conversation, ensure_ascii=False, indent=4))
