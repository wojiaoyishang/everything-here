import requests
import json


def query_ollama_qwen_stream(user_input, model="qwen3-1.7b", api_url="http://localhost:11434/api/chat"):
    """
    向Ollama API发送流式请求，动态打印Qwen模型的响应

    参数:
        user_input (str): 用户输入的文本
        model (str): 要使用的模型，默认为"qwen:1.7b"
        api_url (str): Ollama API的URL，默认为本地地址

    返回:
        str: 模型生成的完整响应文本
    """
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你的回答不能超过1000字"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    full_response = ""

    while True:

        try:
            # 发送POST请求（流式）
            response = requests.post(
                api_url,
                data=json.dumps(payload),
                headers=headers,
                stream=True  # 启用流式接收
            )
            response.raise_for_status()

            # 逐块读取流式响应
            for line in response.iter_lines():
                if line:
                    # 解析JSON数据块
                    chunk = json.loads(line.decode('utf-8'))
                    response_text = chunk.get("message", "").get("content", "")

                    if len(response_text)  >= 1024:
                        raise RuntimeError("超字数，重新生成。")

                    # 动态打印（不换行）
                    print(response_text, end="", flush=True)
                    full_response += response_text

            print()  # 换行
            return full_response

        except requests.exceptions.RequestException as e:
            print(f"\n请求Ollama API时出错: {e}")
            continue


origin_data = json.load(open("common-v2-qwen3.json", "r", encoding="utf-8"))


new_data = []
"""
{
    "instruction": "人类指令（必填）",
    "input": "人类输入（选填）",
    "chosen": "优质回答（必填）",
    "rejected": "劣质回答（必填）"
}
"""
total = len(origin_data)
for i, data in enumerate(origin_data):
    print(f"=====> 生成{i + 1}/{total}任务")
    instruction = data["instruction"]
    output = data["output"]

    bad_output = query_ollama_qwen_stream(instruction)
    new_data.append(
        {
            "instruction": instruction,
            "input": "",
            "chosen": output,
            "rejected": bad_output
        }
    )
    summon_data = open("prefer-common-v2-qwen3.json", "w", encoding="utf-8")
    summon_data.write(json.dumps(new_data, ensure_ascii=False, indent=4))
    summon_data.close()


