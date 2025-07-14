# 注意：需要 transformers>=4.51.0

import os
import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel


def last_token_pool(last_hidden_states: Tensor,
                    attention_mask: Tensor) -> Tensor:
    """
    从模型输出中提取最后一个有效 token 的隐藏状态作为句子表示。

    参数:
        last_hidden_states (Tensor): 模型最后一层的隐藏状态。
        attention_mask (Tensor): 注意力掩码，用于判断哪些 token 是实际内容。

    返回:
        Tensor: 提取后的句子嵌入向量。
    """
    # 判断是否是左填充（即 padding_side='left'）
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]  # 取最后一个 token 的向量
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1  # 计算每个序列的有效长度
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]


def get_detailed_instruct(task_description: str, query: str) -> str:
    """
    构造带任务描述的查询输入格式。

    参数:
        task_description (str): 当前任务的描述。
        query (str): 用户的真实查询内容。

    返回:
        str: 带任务描述的完整输入文本。
    """
    return f"指令: {task_description}\n情感:{query}"


# 定义当前任务：根据搜索查询检索相关段落
task = "判断句子情感"

# 构建两个查询（Queries）
queries = [
    get_detailed_instruct(task, "积极"),
    get_detailed_instruct(task, "消极"),
    get_detailed_instruct(task, "中性")
]

# 构建两个文档（Documents）
documents = [
    "皮卡丘真可爱。",
    "真实太差劲了。"
]

# 将查询和文档合并为输入列表
input_texts = queries + documents

# 加载本地 Qwen3-Embedding 模型的 tokenizer
tokenizer = AutoTokenizer.from_pretrained(r"D:\Ollama-models\models\Qwen3-Embedding-0.6B", padding_side="left")

# 加载模型并指定使用 float16 精度，同时移动到 GPU 上
model = AutoModel.from_pretrained("D:\Ollama-models\models\Qwen3-Embedding-0.6B", torch_dtype=torch.float16).cuda()

# 设置最大输入长度（支持长文本）
max_length = 8192

# 对输入文本进行分词处理
batch_dict = tokenizer(
    input_texts,
    padding=True,  # 自动填充
    truncation=True,  # 自动截断
    max_length=max_length,  # 最大长度限制
    return_tensors="pt",  # 返回 PyTorch 张量
)

# 将数据移动到与模型相同的设备上（如 GPU）
batch_dict.to(model.device)

# 使用模型推理得到输出
outputs = model(**batch_dict)

# 提取每个句子的句向量（使用最后一个有效 token 的向量）
embeddings = last_token_pool(outputs.last_hidden_state, batch_dict["attention_mask"])

# 对所有嵌入向量做 L2 归一化（方便计算余弦相似度）
embeddings = F.normalize(embeddings, p=2, dim=1)

# 计算查询与文档之间的相似度分数（点积 ≈ 余弦相似度）
scores = (embeddings[:2] @ embeddings[2:].T)

# 输出结果
print(scores.tolist())
# 示例输出：
# [[0.7645568251609802, 0.14142508804798126],
#  [0.13549736142158508, 0.5999549627304077]]