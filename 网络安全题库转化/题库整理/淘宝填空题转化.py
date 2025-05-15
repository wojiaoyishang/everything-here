import re

origin_question = open("填空题库.txt", "r", encoding="utf-8").read()
blank_file = open("填空题.md", "w", encoding="utf-8")


for question in origin_question.split("\n"):
    if question.strip() == "":
        continue

    all_match = re.findall(r"(（(.*?)）)", question)
    if len(all_match) == 0:
        all_match = re.findall(r"(\((.*?)\))", question)
        if len(all_match) == 0:
            raise ValueError(f"出现问题 {question}")


    for match in all_match:
        question = question.replace(match[0], f"（ **{match[1].strip()}** ）")


    blank_file.write("# " + question + "\n")