import json
import csv
import re

f = open("Aliya-FULL.txt", "w", encoding="utf-8")

# 使用 with 确保文件正确关闭
with open("aliya.bytes", "r", encoding="utf-8") as origin_csv:
    reader = csv.reader(origin_csv)

    # 跳过第一行（标题）
    next(reader)

    all_data = []

    for row in reader:
        if not row:  # 跳过空行
            continue

        key = row[0].split(".")[0] if "." in row[0] else row[0]
        standard = row[2] if len(row) > 2 else ""
        en = row[3] if len(row) > 3 else ""

        f.write(standard.replace("\\n", "\n") + "\n")
