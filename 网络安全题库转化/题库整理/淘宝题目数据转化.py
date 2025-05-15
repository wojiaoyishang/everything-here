import re

origin_question = open("淘宝1000题.txt", "r", encoding="utf-8").read()

single_file = open("单选题.md", "w", encoding="utf-8")
judge_file = open("判断题.md", "w", encoding="utf-8")

total_question = 0
question_pos = []

# 判断一下标号是否正确：
print("验证题目数据中......")

pos = 0

while pos != -1:
    total_question += 1
    _pos = pos

    # 所有可能的
    length = len(f"、")
    pos = origin_question.find(f"{total_question}、", _pos)
    if pos == -1:
        pos = origin_question.find(f"{total_question}.", _pos)
        length = len(f".")
    if pos == -1:
        pos = origin_question.find(f"{total_question}，", _pos)
        length = len(f"，")
    if pos == -1:
        pos = origin_question.find(f"{total_question}．", _pos)
        length = len(f"．")
    if pos == -1:
        pos = origin_question.find(f"{total_question}.、", _pos)
        length = len(f".、")

    question_pos.append(pos)


total_question -= 1
print(f"一共 {total_question} 题")

print("正在进行数据清洗......")

for i in range(0, total_question, 2):
    pos1, pos2 = question_pos[i], question_pos[i + 1]

    question = origin_question[pos1:pos2]
    _question = question
    if "！！！空！！！" in question:
        continue

    match = re.search(r"(（([ABCD]?)）)", question)
    if match is None:
        match = re.search(r"(\((.*?)\))", question)
        if match is None:
            print(f"ERROR：第 {i + 1} 题 {question} 没有答案。")
            continue

    answer = match.group(2).strip()

    if match.group(2).strip() == '':
        print(f"ERROR：第 {i + 1} 题 {question} 没有答案。")
        continue

    question = question.replace(match.group(1).strip(), "(     )")

    if question.find("、") > len(f"{i + 1}、"):
        # 过滤掉无用的序号
        continue

    question = question[question.find("、") + 1:].strip()

    # 寻找 A B C D
    if question.find("A") != -1 and question.find("B") != -1 and question.find("C") != -1 and question.find("D") != -1:
        # 单选或多选
        print("单选或多选题", question)
        match = re.search(r"([\s\S]*)A、([\s\S]*)B、([\s\S]*)C、([\s\S]*)D、([\s\S]*)", question)
        if match is None:
            continue

        question = match.group(1).strip()
        pretty_choice = f"A、{match.group(2).strip()}\n\n"
        pretty_choice += f"B、{match.group(3).strip()}\n\n"
        pretty_choice += f"C、{match.group(4).strip()}\n\n"
        pretty_choice += f"D、{match.group(5).strip()}\n\n"

        if len(answer) == 1:  # 单选
            single_file.write(f"## {question}\n")
            single_file.write(f"{pretty_choice}")
            single_file.write(f"**正确答案：** {answer}\n")
        else:
            pass  # 多选有问题直接 pass

    else:
        # 过滤掉三个的题，只考虑判断
        if question.find("A、正确") != -1 and question.find("B、错误") != -1:
            print("判断题", question)

            match = re.search(r"([\s\S]*)A、([\s\S]*)B、([\s\S]*)", question)
            if match is None:
                continue

            question = match.group(1).strip()
            pretty_choice = f"A、正确\n\nB、错误\n\n"
            judge_file.write(f"## {question}\n")
            judge_file.write(f"{pretty_choice}")
            judge_file.write(f"**正确答案：** {answer}\n")


