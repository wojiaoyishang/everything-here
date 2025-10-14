import os
import math
import shutil
from struct import unpack


def lc1_to_csv(source_dir, file_name, target_dir):
    source_file = open(os.path.join(source_dir, file_name), 'rb')
    buf = source_file.read()
    source_file.close()

    target_file = open(os.path.join(target_dir, file_name.replace('.lc1', '.csv').replace('31#', '').replace('sh', '').replace('sz', '')), 'w', encoding='utf-8')
    header = "日期,分钟,开盘,最高,最低,收盘,成交额,成交量\n"
    target_file.write(header)

    buf_size = len(buf)
    rec_count = buf_size // 32
    for i in range(rec_count):
        record = unpack('<HH5fI4x', buf[i * 32:(i + 1) * 32])
        year = math.floor(record[0] / 2048) + 2004
        month = math.floor(record[0] % 2048 / 100)
        day = record[0] % 2048 % 100
        date = f"{year}-{month}-{day}"
        minutes = f"{record[1] // 60:02d}:{record[1] % 60:02d}"
        line = f"{date},{minutes},{record[2]:.3f},{record[3]:.3f},{record[4]:.3f},{record[5]:.3f},{record[6]},{record[7]}\n"
        target_file.write(line)
    target_file.close()


def day_to_csv(source_dir, file_name, target_dir):
    source_file = open(os.path.join(source_dir, file_name), 'rb')
    buf = source_file.read()
    source_file.close()

    target_file = open(os.path.join(target_dir, file_name.replace('.day', '.csv').replace('31#', '').replace('sh', '').replace('sz', '')), 'w', encoding='utf-8')
    header = "日期,开盘,最高,最低,收盘,成交额,成交量\n"
    target_file.write(header)

    buf_size = len(buf)
    rec_count = buf_size // 32
    for i in range(rec_count):
        record = unpack('IfffffII', buf[i * 32:(i + 1) * 32])
        date = f"{record[0] // 10000}-{(record[0] % 10000) // 100:02d}-{record[0] % 100:02d}"
        line = f"{date},{record[1]:.3f},{record[2]:.3f},{record[3]:.3f},{record[4]:.3f},{record[5]:.3f},{record[6]}\n"
        target_file.write(line)

    target_file.close()


source_path = r"./lc1"
target_path = "./parsed_data"
os.makedirs(target_path, exist_ok=True)

for file in os.listdir(source_path):
    if file.endswith(".lc1"):
        print("转化：", source_path + file)
        lc1_to_csv(source_path, file, target_path)
    if file.endswith(".day"):
        print("转化：", source_path + file)
        day_to_csv(source_path, file, target_path)


# 自动整理
stock_data = [
    ('09992', '泡泡玛特', 6.62),
    ('002594', '比亚迪', 4.81),
    ('301061', '匠心家居', 4.18),
    ('689009', '九号公司', 3.94),
    ('09926', '康方生物', 3.83),
    ('301004', '嘉益股份', 3.49),
    ('688235', '百济神州', 3.42),
    ('300752', '隆利科技', 3.40),
    ('600595', '中孚实业', 3.40),
    ('603530', '神马电力', 3.39)
]

save_path = './永赢睿信混合 2025-03-31 至 2025-06-30'
if not os.path.exists(save_path):
    os.mkdir(save_path)


for data in stock_data:
    i, n, p = data

    path = os.path.join(target_path, i + '.csv')
    shutil.copy(path, save_path + "/" + n + ' ' + str(p) + '.csv')


