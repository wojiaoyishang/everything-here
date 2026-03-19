import os
import shutil
import logging
import sys


def normal_file(path):
    """
    将通信达导出的基金净值文件转化
    """
    content = ""

    try:
        with open(path, "r", encoding="gb2312") as f:

            for i, line in enumerate(f):
                line = line.strip()

                if line == "" or line[0] == '#':
                    continue

                if i == 0 or i == 1:  # 去掉第一行第二行
                    continue

                line = line.replace("	", ",")
                line = line.replace("         ", "")
                line = line.replace("      ", "")
                line = line.replace("     ", "")
                line = line.replace("  ", "")
                line = line.replace(" ", "")
                content += line + '\n'

        with open(path, "w", encoding='utf-8') as f:
            f.write(content)
    except:
        pass


def copy_value(config_string):
    BASE_PATH = './values'

    for line in config_string.split("\n"):
        name, code = line.split(" ")
        logging.info(f"Normalized file: {BASE_PATH + '/' + code + '.xls'}")
        normal_file(BASE_PATH + '/' + code + '.xls')

        # 拷到目标文件夹
        for filename in os.listdir('.'):
            if filename.startswith(name) and os.path.isdir(filename):
                shutil.copy(BASE_PATH + '/' + code + '.xls', './' + filename + '/基金净值.csv')
                logging.info(f"Copy {BASE_PATH + '/' + code + '.xls'} => {'./' + filename + '/基金净值.csv'}")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        stream=sys.stdout  # 明确输出到 stdout
    )
    config_string = """长盛城镇化主题混合A 000354
富国中小盘精选混合A 000940
华宝核心优势混合C 016461
工银新兴制造混合A 009707
浦银安盛高端装备混合A 019864
长信电子信息量化灵活配置混合A 519929
博时创新精选混合C 011487
宏利复兴混合A 001170
前海开源嘉鑫混合A 001765
瑞达先进制造混合型发起式C 018227
财通多策略升级混合(LOF)A 501015
格林高股息优选混合A 015289
中加新兴成长混合C 009856
格林高股息优选混合C 015290
大摩数字经济混合C 017103
财通匠心优选一年持有混合C 014916
前海开源沪港深乐享生活 004320
前海开源沪港深核心资源混合A 003304
万家全球成长一年持有期混合(QDII)C 012536
中加转型动力混合C 005776
财通资管先进制造混合发起式A 021985
建信电子行业股票A 017746
融通价值趋势混合C 010647
南方半导体产业股票发起A 020553
海富通中小盘混合 519026
博时厚泽匠选一年持有期混合A 018217
中欧半导体产业股票发起C 019764"""
    copy_value(config_string)