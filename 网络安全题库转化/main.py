import random
import time
import os

import win32com.client
from docx import Document

questions = {}

ppt_instance = win32com.client.Dispatch('PowerPoint.Application')

read_only = True
has_title = False
window = True

if os.path.exists('题目重复记录.txt'):
    recode_txt = open('题目重复记录.txt', 'r+', encoding='utf-8').read()
else:
    recode_txt = ""

recode_file = open('题目重复记录.txt', "w", encoding='utf-8')
recode_file.write(recode_txt)

question_recode_csv = open("问题记录.csv", "w", encoding='utf-8')


def getq(qtype):
    global recode_txt
    allq = questions[qtype]

    i = random.randint(0, len(allq) - 1)

    result = allq[i]
    while result is None or result['body'][:10] in recode_txt:
        result = allq[i]
        i = random.randint(0, len(allq) - 1)

    allq[i] = None

    recode_file.write(result['body'][:10] + "\n")
    recode_file.flush()
    recode_txt += result['body'][:10]

    return result


def summon(save_name, ptype, ppt_name, mounts_type, rand=False):
    nr_slide = 2  # 模板页
    insert_index = 3

    prs = ppt_instance.Presentations.open(r'E:\Programming\Python\everything-here\网络安全题库转化\题包模板.pptx',
                                          read_only, has_title, window)
    prs.Slides(nr_slide).Copy()

    # 设定第一页的文字
    for Shape in prs.Slides(1).Shapes.Range():
        if Shape.HasTextFrame:
            if Shape.TextFrame.TextRange.Text == "题目":
                Shape.TextFrame.TextRange.Text = ptype
            elif Shape.TextFrame.TextRange.Text == "题包编号":
                Shape.TextFrame.TextRange.Text = ppt_name

    def add_page(htype, question, key):
        nonlocal insert_index
        prs.Slides(insert_index).Select()

        for Shape in prs.Slides(insert_index).Shapes.Range():
            if Shape.Type == 6:

                con = False
                for Shape2 in Shape.GroupItems:
                    if Shape2.HasTextFrame:
                        if Shape2.TextFrame.TextRange.Text == "答案":
                            if key is None:
                                Shape.Delete()
                                con = True
                                break
                            Shape2.TextFrame.TextRange.Text = "答案：" + key
                        elif Shape2.TextFrame.TextRange.Text == "题目类型":
                            Shape.TextFrame.TextRange.Text = htype
                        # elif Shape2.TextFrame.TextRange.Text == "题目":
                        #     Shape.TextFrame.TextRange.Text = question

                if con:
                    continue

            if Shape.HasTextFrame:
                if Shape.TextFrame.TextRange.Text == "题目类型":
                    Shape.TextFrame.TextRange.Text = htype
                elif Shape.TextFrame.TextRange.Text == "题目":
                    Shape.TextFrame.TextRange.Text = question

        insert_index += 1

    mounts_map = []
    question_count = 1
    all_mount_count = 0

    # for qtype, mount in mounts.items():
    #     all_mount_count += mount
    #     for _ in range(mount):
    #         mounts_map.append(qtype)

    if mounts_type == 0:  # 判断5 单选5 多选5
        for qtype in ["判断", "单选", "多选"]:
            for __ in range(5):
                mounts_map.append(qtype)
                all_mount_count += 1
    elif mounts_type == 1:  # 判断3 单选3 多选2 填空1 重复一次
        for _ in range(2):
            for __ in range(3):
                mounts_map.append("判断")
                all_mount_count += 1
            for __ in range(3):
                mounts_map.append("单选")
                all_mount_count += 1
            for __ in range(2):
                mounts_map.append("多选")
                all_mount_count += 1
            mounts_map.append("填空")
            all_mount_count += 1
        mounts_map.append("简答")
        all_mount_count += 1

    elif mounts_type == 2:
        for _ in range(4):
            for __ in range(2):
                mounts_map.append("判断")
                all_mount_count += 1
            for __ in range(2):
                mounts_map.append("单选")
                all_mount_count += 1
            for __ in range(2):
                mounts_map.append("多选")
                all_mount_count += 1
            mounts_map.append("填空")
            all_mount_count += 1

    elif mounts_type == 3:
        for _ in range(4):
            mounts_map.append("判断")
            mounts_map.append("单选")
            mounts_map.append("多选")
            mounts_map.append("填空")
            all_mount_count += 4
        mounts_map.append("单选")
        mounts_map.append("多选")
        mounts_map.append("简答")
        mounts_map.append("简答")
        all_mount_count += 4

    for i in range(insert_index, insert_index + all_mount_count):
        prs.Slides.Paste(i)
        time.sleep(0.3)

    for qtype in mounts_map:
        # 随机抽题
        time.sleep(0.3)
        meta = getq(qtype)

        question_recode_csv.write(f"{save_name}\t{question_count}\t{qtype}\t{meta['index']}\t{meta['body'][:10]}...\n")
        question_recode_csv.flush()

        add_page(ptype, f"（{qtype}题）{question_count}、{meta['body']}", meta['key'])
        question_count += 1

    # 删掉模板页
    prs.Slides(nr_slide).Delete()
    prs.SaveAs(rf'E:\Programming\Python\everything-here\网络安全题库转化\{save_name}.pptx')
    prs.Close()


def main():
    for qtype in ['填空', '单选', '判断', '多选', '简答']:
        questions[qtype] = []

        document = Document(f"决赛题库/决赛-{qtype}题.docx")

        # 遍历文档中的所有段落并打印其内容
        question_meta = {
            'body': None,
            'key': None,
            'index': None
        }
        for paragraph in document.paragraphs:
            if paragraph.style.name == 'Heading 1' or paragraph.style.name == 'Normal' and qtype == "填空":  # 遇到问题了
                if question_meta['body']:
                    questions[qtype].append(question_meta)
                question_meta = question_meta.copy()
                question_meta['body'] = None
                question_meta['key'] = None
                if qtype == "填空":
                    keys = ""
                    body = ""
                    for run in paragraph.runs:
                        for t in run.text:
                            if t.strip() == "）":
                                body += "）"
                                keys = keys + "、"
                            elif run.bold:
                                keys = keys + t
                            else:
                                body += t
                        question_meta['body'] = body
                        question_meta['key'] = keys.strip("、")
                else:
                    question_meta['body'] = paragraph.text + "\n"

                if question_meta['body'] is None:
                    continue

                question_meta['index'] = question_meta['body'][:question_meta['body'].find(".")]

                if question_meta['body'].find(".") != -1 and question_meta['body'].find(".") < 5:
                    question_meta['body'] = question_meta['body'][question_meta['body'].find(".") + 1:]

                continue

            if "正确答案：" in paragraph.text:
                question_meta['key'] = paragraph.text.replace("正确答案：", "")
                continue

            if question_meta['body']:
                question_meta['body'] += paragraph.text + "\n"

            if qtype == "简答":
                question_meta['body'] = question_meta['body'][:question_meta['body'].find("\n")]

        # 去掉. 、
        if question_meta['body']:
            questions[qtype].append(question_meta)

    for name in ["题包一", "题包二", "题包三", "题包四"]:
        print("生成", name)
        summon("决赛ppt\\环节一\\" + name, "有问必答", name, 0,
               False)

    for name in ["题包一", "题包二"]:
        print("生成", name)
        summon("决赛ppt\\环节二\\" + name, "两两PK", name, 1,
               True)

    for name in ["题包一", "题包二", "题包三", "题包四"]:
        print("生成", name)
        summon("决赛ppt\\环节三\\" + name, "争分夺秒", name, 2, True)

    for name in ["题包一", "额外题包1", "额外题包2"]:
        print("生成", name)
        summon("决赛ppt\\环节四\\" + name, "风险抢答", name, 3, True)


if __name__ == '__main__':
    main()
    ppt_instance.Quit()
