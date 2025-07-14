import jieba


# 安装 jieba：pip install jieba

def tokenize_chinese(sentence):
    """使用 jieba 分词"""
    return set(jieba.lcut(sentence))


def jaccard_similarity(set1, set2):
    """计算 Jaccard 相似度"""
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0.0

question_file = open("./测试的题目.md", "r", encoding="utf-8")
all_question = []

line = question_file.readline()
while line:
    line = question_file.readline()

    if line and line[0] == "#":  # 题目字段
        all_question.append([line.strip()[2:], question_file.readline().strip()])

for x in range(len(all_question)):
    for y in range(x + 1, len(all_question)):
        s = jaccard_similarity(tokenize_chinese(all_question[x][0]), tokenize_chinese(all_question[y][0]))
        if s > 0.8:
            print(f"题目重复：{all_question[x][0]} {all_question[y][0]}")
