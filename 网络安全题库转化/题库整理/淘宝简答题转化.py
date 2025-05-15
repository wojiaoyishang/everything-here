import re
from ollama import chat

system_prompt = """
# 说明
请帮用户整理输入，要求将用户的输入以标准的markdown形式返回


# 示例
用户输入：
1 计算机病毒入侵检测技术 2 智能引擎技术.智能引擎技术发展了特征代码扫描法的优点 3 嵌入式杀毒技术.嵌入式杀毒技术是对病毒经常攻击的应用程序或者对象提供重点保护的技术， 4 未知病毒查杀技术.

你输出：
1. 计算机病毒入侵检测技术
2. 智能引擎技术.智能引擎技术发展了特征代码扫描法的优点
3. 嵌入式杀毒技术.嵌入式杀毒技术是对病毒经常攻击的应用程序或者对象提供重点保护的技术，
4. 未知病毒查杀技术.

用户输入：
初始级，可管理级，可定义级，可预知级，优化级。

你输出：
初始级，可管理级，可定义级，可预知级，优化级。

用户输入：
病毒对于网络的威胁：病毒的主要传播途径已经变成了网络。
黑客对于网络的破坏和入侵：主要目的在于窃取数据和非法修改系统。

你输出：
**病毒对于网络的威胁：** 病毒的主要传播途径已经变成了网络。
**黑客对于网络的破坏和入侵：** 主要目的在于窃取数据和非法修改系统。

# 要求
1. 无论用户输入的内容是否正确都仅整理不要多余更改，
2. 不能输出多余内容，不需要解释
3. 如果最终整理的内容已经有序标号，内容不需要加粗
4. 如果最终整理的内容是某个方面的展开，这个方面的总称需要加粗
"""


def qwen_request(system, user):
    """
    简单的通义千问请求接口。

    :param system: 系统内容
    :param user: 用户内容
    :return: 通义千问内容
    """

    stream = chat(model="qwen3:4b", messages=[
        {
            "role": "system",
            "content": system
        },
        {
            "role": "user",
            "content": user
        }
    ], stream=True, options={'temperature': 0.1})

    content = ""
    for chunk in stream:
        content += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)

    return content[content.find("</think>") + len("</think>"):].strip()


origin_question = open("简答题库.txt", "r", encoding="utf-8").read()
free_file = open("free.txt", "a", encoding="utf-8")

total_question = 0
question_pos = []

# 判断一下标号是否正确：
print("验证题目数据中......")

pos = 0

while pos != -1:
    total_question += 1
    _pos = pos

    # 所有可能的
    pos = origin_question.find(f"{total_question}\t", _pos)

    print(origin_question[pos:origin_question.find("\n", pos)])

    question_pos.append(pos)

total_question -= 1
print(f"一共 {total_question} 题")

print("开始整理......")
for i in range(0, total_question, 1):

    if i < 139:
        continue

    pos1, pos2 = question_pos[i], question_pos[i + 1]

    all_text = origin_question[pos1:pos2]

    question = all_text[all_text.find("\t"):all_text.find("\n")]
    question = question[question.find("、") + 1:]  # 去掉题号

    body = all_text[all_text.find("\n") + 1:].strip()

    body = qwen_request(system_prompt, body)

    free_file.write("# " + question + "\n")
    free_file.write(body + "\n\n")

    print("\n================整理结果================")
    print(f"{i + 1} 题目：", question)
    print(body)

    free_file.flush()
