from paddlenlp import Taskflow

similarity = Taskflow("text_similarity")

question_file = open("./题库.md", "r", encoding="utf-8")
all_question = []

line = question_file.readline()
while line:
    line = question_file.readline()

    if line and line[0] == "#":  # 题目字段
        all_question.append([line.strip()[2:], question_file.readline().strip()])

for x in range(len(all_question)):
    for y in range(x + 1, len(all_question)):
        s = similarity([[all_question[x][0], all_question[y][0]]])[0]['similarity']
        if s > 0.8:
            print(f"题目重复：{all_question[x][0]}")
