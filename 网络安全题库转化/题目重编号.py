from docx import Document

document = Document(f"（改）决赛-单选题.docx")

count = 0
for paragraph in document.paragraphs:
    if paragraph.style.name == 'Heading 1':  # 遇到问题了
        count += 1

        p = str(count) + paragraph.text[paragraph.text.find('.'):]

        if paragraph.text[:paragraph.text.find('.')] != str(count):
            print('修正编号', paragraph.text, '=>', p)

        paragraph.text = p

document.save('已修改.doc')