import os
import json
import time

from weibo import Weibo

wb = Weibo()


def login_to_weibo():
    # 验证登录是否有效
    if os.path.exists('login.json'):
        with open('login.json', 'r') as f:
            wb.update_cookies(json.loads(f.read()))

    if wb.get_user_id() == -1:  # 是否登录
        print("登录无效，请使用手机微博扫描二维码登录。")
        with open('qrcode.png', 'wb') as f:
            qrcode, data = wb.get_login_qrcode()
            f.write(data)

        os.startfile('qrcode.png')

        login = wb.check_qrcode(qrcode)
        count = 0
        while not login:
            time.sleep(1)
            login = wb.check_qrcode(qrcode)
            print(f"\r等待扫码登录......({count}s)", end="")
            count += 1
        print("\r", end="")

        with open('login.json', 'w') as f:
            f.write(json.dumps(wb.get_cookies()))

        os.remove('qrcode.png')
        print("登录成功，已保存登录信息。")


comment_file = open('comment.txt', 'w', encoding='utf-8')

if __name__ == '__main__':
    login_to_weibo()

    if wb.get_user_id() == -1:
        print("登录失败，请重试。")
        exit()

    print(f"登录信息有效，获取到用户ID: {wb.get_user_id()}")

    # 获取用户动态
    page = 1
    data = wb.get_mymblog(uid=7467555881,
                          page=page)

    while data['since_id'] != "":
        since_id = data['since_id']
        for blog in data['list']:
            time.sleep(1)
            print("-" * 150)
            print("发布者：", blog['user']['screen_name'])
            print("发布者ID：", blog['user']['id'])
            print("发布时间：", blog['created_at'])
            print("发布内容：\n" + blog['text_raw'])
            print("博文ID：", blog['idstr'])

            print("正在获取评论......", end="")
            info = wb.get_comments(id=blog['idstr'],
                                   user_id=blog['user']['id'])
            i = 0
            while info['max_id'] != 0:
                for comment in info['data']:
                    i += 1
                    print(f"\r计数：{i}", comment['user']['screen_name'] + "：" + comment['text_raw'], end="")
                    print(comment['text_raw'], file=comment_file, flush=True)

                time.sleep(0.5)
                info = wb.get_comments(id=blog['idstr'],
                                       user_id=blog['user']['id'],
                                       max_id=info['max_id'],
                                       count=10)
            print("\r", end="")
            print(f"获取完毕。总共：{i}条")

        page += 1
        data = wb.get_mymblog(uid=7467555881,
                              page=page,
                              since_id=data['since_id'])
