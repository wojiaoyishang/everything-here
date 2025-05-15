import re

origin_question = open("多选题库.txt", "r", encoding="utf-8").read()
multi_file = open("多选题.md", "w", encoding="utf-8")

total_question = 105
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

print("开始整理多选......")
for i in range(0, total_question, 1):
    pos1, pos2 = question_pos[i], question_pos[i + 1]

    all_text = origin_question[pos1:pos2]

    question = all_text[:all_text.find("\n")]
    question = question[question.find("、") + 1:]  # 去掉题号

    body = all_text[all_text.find("\n") + 1:]

    match = re.search(r"(（([ABCDE]*)）)", question)
    if match is None:
        match = re.search(r"(\(([ABCDE]*)\))", question)
        if match is None:
            raise ValueError(f"第 {i + 1} 题 没有答案。 {question}")

    question = question.replace(match.group(1), "（      ）")
    answer = match.group(2).strip()

    if len(answer) == 1:
        continue

    if 'E' in body:
        match = re.search(r"([\s\S]*)A[.．、]([\s\S]*)B[.．、]([\s\S]*)C[.．、]([\s\S]*)D[.．、]([\s\S]*)E[.．、]([\s\S]*)", body)
        if match is None:
            continue
        pretty_choice = f"A、{match.group(2).strip()}\n\n"
        pretty_choice += f"B、{match.group(3).strip()}\n\n"
        pretty_choice += f"C、{match.group(4).strip()}\n\n"
        pretty_choice += f"D、{match.group(5).strip()}\n\n"
        pretty_choice += f"E、{match.group(6).strip()}\n\n"
    else:
        match = re.search(r"([\s\S]*)A[.．、]([\s\S]*)B[.．、]([\s\S]*)C[.．、]([\s\S]*)D[.．、]([\s\S]*)", body)
        if match is None:
            continue
        pretty_choice = f"A、{match.group(2).strip()}\n\n"
        pretty_choice += f"B、{match.group(3).strip()}\n\n"
        pretty_choice += f"C、{match.group(4).strip()}\n\n"
        pretty_choice += f"D、{match.group(5).strip()}\n\n"

    multi_file.write(f"# {question}\n")
    multi_file.write(match.group(1).strip() + "\n\n")
    multi_file.write(pretty_choice)
    multi_file.write(f"**正确答案：** {answer}\n")
    multi_file.flush()
    print(question, "\n", match.group(1).strip(), "\n", pretty_choice)