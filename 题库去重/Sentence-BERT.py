from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def bert_similarity_matrix(sentences):
    embeddings = model.encode(sentences)
    return cosine_similarity(embeddings)


question_file = open("./测试的题目.md", "r", encoding="utf-8")
all_question = []

line = question_file.readline()
while line:
    line = question_file.readline()

    if line and line[0] == "#":  # 题目字段
        all_question.append([line.strip()[2:], question_file.readline().strip()])

similarity_matrix = bert_similarity_matrix([_[0] for _ in all_question])

for x in range(len(all_question)):
    for y in range(x + 1, len(all_question)):
        s = similarity_matrix[x][y]
        if s > 0.8:
            print(f"题目重复：{all_question[x][0]} {all_question[y][0]}")
