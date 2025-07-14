import os
import json
import traceback
import base64
from openai import OpenAI
from response_format import parse_content_to_json

prompt = """
你需要从图片中提取出题目，并以标准的JSON格式返回数据，不需要多余解释，输出格式参考：
{"question": "获取到问题", "choices": ["A选项", "B选项", "C选项", "D选项"]}

要求：
1.你只需要提取题目与选项，不需要解题，也不允许将答案直接嵌入到题目中
2.忽略掉“考试中选项顺序会自动打乱。您现在查看的是试题原选项顺序。”的提示，不要摘录这句话
3.题目中的空使用“__________”代替，不准多不准少。

参考输出:
{"question": "The _________ of the silicon chip was a landmark in the history of the computer.", "choices": ["invention", "information", "interaction", "infection"]}
"""


#  base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def vlm_get_response(image_path):
    base64_image = encode_image(image_path)

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url="https://api.siliconflow.cn/",
    )

    response = client.chat.completions.create(
        model="Pro/Qwen/Qwen2.5-VL-7B-Instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}", 'detail': 'high'},
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        temperature=0.1,
        stream=True,
    )

    content = ""
    for chunk in response:
        chunk_message = chunk.choices[0].delta.content
        print(f"{chunk_message}", end="")
        content += chunk_message

    return parse_content_to_json(content)


f = open("./导出的题目2.md", "w", encoding="utf-8")

for filename in os.listdir("./不同题目3"):
    path = f"./不同题目3/{filename}"
    while True:
        print("获取", filename)
        try:
            meta = vlm_get_response(path)[1]
            if 'question' not in meta or 'choices' not in meta:
                raise RuntimeError("错误")
            f.write(f"# {meta['question']}\n")
            f.write(f"A. {meta['choices'][0]}\tB. {meta['choices'][1]}\tC. {meta['choices'][2]}\tD. {meta['choices'][3]}\n\n")
            break
        except BaseException as e:
            traceback.print_exc()
            print("出错重试。")

    f.flush()