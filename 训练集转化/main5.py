import json

with open("recode.txt", "r", encoding="utf-8") as f:
    origin_dataset = f.read()

all_dataset = []

offset = 0
flag = True  # True 问题  False 答案
while offset != -1:
    offset1 = origin_dataset.find("**问：**", offset)
    offset2 = origin_dataset.find("**答：**", offset)

    offset1 = offset1 + len("**问：**")

    question = origin_dataset[offset1:offset2].strip()

    offset1 = offset2 + len("**答：**")
    offset2 = origin_dataset.find("**问：**", offset1)

    answer = origin_dataset[offset1:offset2].strip()

    offset = offset2

    all_dataset.append({
        "instruction": question,
        "input": "",
        "output": answer
    })

with open("Aliya-knowledge.json", "w", encoding="utf-8") as f:
    json.dump(all_dataset, f, ensure_ascii=False, indent=4)