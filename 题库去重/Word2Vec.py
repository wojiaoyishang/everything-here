import jieba
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# pip install jieba gensim scikit-learn numpy
# 加载预训练的 Word2Vec 中文模型（请先下载）
# 推荐模型：哈工大 Tencent_AILab_Chinese_w2v (+- 144MB)
# 下载地址：https://github.com/Embedding/Chinese-Word-Vectors
model_path = r"D:\Ollama-models\light_Tencent_AILab_ChineseEmbedding.bin"  # 替换为你自己的路径
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)


# 对句子进行分词并生成句向量（词向量平均）
def sentence_vector(sentence):
    words = jieba.lcut(sentence)
    vectors = [w2v_model[word] for word in words if word in w2v_model]
    if not vectors:
        return np.zeros(w2v_model.vector_size)
    return np.mean(vectors, axis=0)


# 计算所有句子的句向量
def get_sentence_vectors(sentences):
    return np.array([sentence_vector(sent) for sent in sentences])


# 构建相似度矩阵
def word2vec_similarity_matrix(sentences):
    vectors = get_sentence_vectors(sentences)
    return cosine_similarity(vectors)


# 读取题目文件
question_file = open("./测试的题目.md", "r", encoding="utf-8")
all_question = []

line = question_file.readline()
while line:
    line = question_file.readline()
    if line and line[0] == "#":  # 题目字段
        all_question.append([line.strip()[2:], question_file.readline().strip()])

# 获取题目标题列表
sentences = [_[0] for _ in all_question]

# 计算相似度矩阵
similarity_matrix = word2vec_similarity_matrix(sentences)

# 打印相似度大于 0.8 的重复题目对
for x in range(len(all_question)):
    for y in range(x + 1, len(all_question)):
        s = similarity_matrix[x][y]
        if s > 0.95:
            print(f"题目重复：{all_question[x][0]} | {all_question[y][0]} | 相似度: {s:.4f}")
