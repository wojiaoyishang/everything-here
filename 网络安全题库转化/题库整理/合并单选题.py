import re

all_old_questions = []

origin_question = open("要合并的单选题.txt", "r", encoding="utf-8").read()
single_file = open("多的单选.md", "w", encoding="utf-8")

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

# 读一下原来的题库
old = open("原来的单选.txt", "r", encoding="utf-8").read()

print("开始整理......")
for i in range(0, total_question, 1):
    pos1, pos2 = question_pos[i], question_pos[i + 1]
    all_text = origin_question[pos1:pos2]

    question = all_text[:all_text.find("\n")]
    question = question[question.find("、") + 1:]

    body = all_text[all_text.find("\n") + 1:]

    match = re.search(r"(（([ABCDE ]*)）)", question)
    if match is None:
        match = re.search(r"(\(([ABCDE ]*)\))", question)
        if match is None:
            match = re.search(r"(\(([ABCDE ]*)）)", question)
            if match is None:
                match = re.search(r"(（([ABCDE ]*)\))", question)
                if match is None:
                    raise ValueError(f"第 {i + 1} 题 没有答案。 {question}")

    question = question.replace(match.group(1), "（      ）").strip()
    answer = match.group(2).strip()

    if question[7:10] in old:
        # 过滤重复
        print("题目重复：", question)
        continue

    match = re.search(r"([\s\S]*)A[.．、]([\s\S]*)B[.．、]([\s\S]*)C[.．、]([\s\S]*)D[.．、]([\s\S]*)", body)
    if match is None:
        continue
    pretty_choice = f"A、{match.group(2).strip()}\n\n"
    pretty_choice += f"B、{match.group(3).strip()}\n\n"
    pretty_choice += f"C、{match.group(4).strip()}\n\n"
    pretty_choice += f"D、{match.group(5).strip()}\n\n"

    single_file.write(f"# {question}\n")
    single_file.write(match.group(1).strip() + "\n\n")
    single_file.write(pretty_choice)
    single_file.write(f"**正确答案：** {answer}\n")
    single_file.flush()
    print(question, "\n", match.group(1).strip(), "\n", pretty_choice)