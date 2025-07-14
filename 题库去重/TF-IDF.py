import jieba

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text):
    return " ".join(jieba.cut(text, cut_all=False))


def tfidf_similarity_matrix(sentences):
    # 预处理所有句子
    preprocessed = [preprocess_text(s) for s in sentences]

    # 统一向量化
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed)

    # 计算相似度矩阵
    return cosine_similarity(tfidf_matrix)


question_file = open("./测试的题目.md", "r", encoding="utf-8")
export_file = open("./题库去重.md", "w", encoding="utf-8")

all_question = []

line = question_file.readline()
while line:
    line = question_file.readline()

    if line and line[0] == "#":  # 题目字段
        all_question.append([line.strip()[2:], question_file.readline().strip()])

# 计算所有文本相似度
similarity_matrix = tfidf_similarity_matrix([_[0] for _ in all_question])

# 便利所有题目找出相似
for x in range(len(all_question)):
    re = False
    for y in range(x + 1, len(all_question)):
        s = similarity_matrix[x][y]
        if s > 0.8:
            re = True
            print(f"题目重复：{all_question[x][0]} {all_question[y][0]}")

    if not re:
        export_file.write("# " + all_question[x][0] + "\n" + all_question[x][1] + "\n\n")
