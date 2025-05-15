all_old_questions = []

old = open("旧判断题.txt", "r", encoding="utf-8").read()

total_question = 0

# 判断一下标号是否正确：
print("验证题目数据中......")

pos = 0

while pos != -1:
    total_question += 1
    _pos = pos

    # 所有可能的
    pos = old.find(f"{total_question}.", _pos)

    all_old_questions.append(old[pos:old.find("\n", pos)].strip())

new = open("新增判断题.txt", "r", encoding="utf-8").read()


export = open("导出新判断.md", "w", encoding="utf-8")

for new in new.split("\n"):
    new = new[new.find(".")+1:].strip()

    correct = None
    if '(正确)' in new:
        correct = True
        new = new.replace('(正确)', '')
    elif '(错误)' in new:
        correct = False
        new = new.replace('(错误)', '')
    elif '（正确）' in new:
        correct = True
        new = new.replace('（正确）', '')
    elif '（错误）' in new:
        correct = False
        new = new.replace('（错误）', '')

    if correct is None:
        continue

    r = False
    for o in all_old_questions:
        if o.find(new[:5]) != -1:
            r = True

    if r:
        continue

    export.write(f"# {new}\n")
    export.write(f"A、正确\n\nB、错误\n\n")
    export.write(f"**正确答案：** {'BA'[correct]}\n")

