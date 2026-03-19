import logging
import os
import math
import shutil
from struct import unpack


def lc5_to_csv(source_dir, file_name, target_dir):
    source_file = open(os.path.join(source_dir, file_name), 'rb')
    buf = source_file.read()
    source_file.close()

    target_file = open(os.path.join(target_dir,
                                    file_name.replace('.lc5', '.csv').replace('31#', '').replace('sh', '').replace('sz',
                                                                                                                   '')),
                       'w', encoding='utf-8')
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


def batch_convert_lc5(source_path=r'./lc5', target_path=r'./parsed_data'):
    os.makedirs(target_path, exist_ok=True)

    for file in os.listdir(source_path):
        if file.endswith(".lc5"):
            logging.info("转化：" + source_path + '/' + file)
            lc5_to_csv(source_path, file, target_path)


def tidy_lc5_result(target_path, stock_data, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    for data in stock_data:
        i, n, p = data

        path = os.path.join(target_path, i + '.csv')
        shutil.copy(path, save_path + "/" + n + ' ' + str(p) + '.csv')

        logging.info(f"Copy {path} => {save_path + '/' + n + ' ' + str(p) + '.csv'}")
