import re
import json

with open("./database.json", "r", encoding="utf-8") as f:
    datas = json.loads(f.read())

with open("./origin.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    i = 0
    add_more = False
    line = ""
    while i < len(lines):

        if add_more:
            line = line.strip() + lines[i + 1].strip()
        else:
            line = lines[i]

        add_more = False

        if line.strip() == "":
            continue

        match = re.search(r"\d.*(.*)（(.*)）.*A\.([\s\S]*)B\.([\s\S]*)C\.([\s\S]*)D\.([\s\S]*)", line)
        if match:
            datas.append({
                "instruction": "你是一位专业的出题专家，请根据用户提供的主题（如书名），以JSON格式设计高水平的选择题。",
                "input": "请围绕《平凡的世界》这本书，设计一组考察知识点的选择题。",
                "output": json.dumps({
                    "type": "选择题",
                    "question": match.group(1).strip(),
                    "options": [
                        match.group(3).strip(),
                        match.group(4).strip(),
                        match.group(5).strip(),
                        match.group(6).strip()
                    ],
                    "answer": match.group(3 + ord(match.group(2)) - ord("A")).strip(),
                }, ensure_ascii=False)
            })

            open("./database.json", "w", encoding="utf-8").write(json.dumps(datas, ensure_ascii=False, indent=4))
        else:
            if not add_more:
                add_more = True

        i += 1
        if not add_more:
            line = ""
