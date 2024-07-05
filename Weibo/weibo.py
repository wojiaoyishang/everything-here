"""
微博 API
"""
__author__ = 'Yishang'
__date__ = '2024/7/2 19:50'

import json
import random
import re

import requests


class Weibo:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }

    def __init__(self, sub=None, subp=None, session=requests.session()):
        """
        微博 API 类，在 Python 中调用微博。仅用于测试，不打算更新，欢迎在 Gitee 上提 PR 。
        sub subp 两个值一同保存登录信息，也用于验证。

        :param sub: sub 字段值。
        :param subp: subp 字段值。
        """
        self.session = session

        self.session.cookies.update({'sub': sub, 'subp': subp})

    def get_user_id(self) -> int:
        """
        获取用户ID，可以用于检查是否登录，登录返回用户ID，否则返回-1。
        :return: 用户ID。
        """
        response = self.session.get('https://weibo.com/ajax/log/action')

        if response.headers.get('X-Log-Uid') is not None:
            return response.headers.get('X-Log-Uid')

        return -1

    def get_login_qrcode(self) -> tuple:
        """
        获取登录的二维码，返回二维码编号（qrid）和png图片二进制字节数据
        :return: (qrid, 二进制数据)
        """
        params = {
            'entry': 'miniblog',
            'source': 'miniblog',
            'disp': 'popup',
            'url': 'https://weibo.com/',
            # 重定向
        }

        # 先获取 X-Csrf-Token
        self.session.get('https://passport.weibo.com/sso/signin', params=params)

        params = {
            'entry': 'miniblog',
            'size': '180',
        }

        headers = {
            'X-Csrf-Token': self.session.cookies.get('X-CSRF-TOKEN'),
            'Referer': 'https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&disp=popup&url=https%3A%2F%2Fweibo.com'
        }
        response = self.session.get('https://passport.weibo.com/sso/v2/qrcode/image', params=params,
                                    headers=headers)

        qrid = response.json()['data']['qrid']

        return qrid, self.session.get(response.json()['data']['image']).content

    def check_qrcode(self, qrid: str) -> bool:
        """
        获取登录二维码的扫码状态，如果是 False 则为尚未扫码，反之，则已经登录。
        :param qrid: 二维码编号
        :return: 是否成功
        """
        params = {
            'entry': 'miniblog',
            'source': 'miniblog',
            'url': 'https://weibo.com/',  # 重定向地址
            'qrid': qrid,  # 二维码id
            'disp': 'popup',
        }

        headers = {
            'X-Csrf-Token': self.session.cookies.get('X-CSRF-TOKEN'),
            'Referer': 'https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&disp=popup&url=https%3A%2F%2Fweibo.com'
        }

        response = self.session.get('https://passport.weibo.com/sso/v2/qrcode/check', params=params,
                                    allow_redirects=False,
                                    headers=headers)

        if response.json()['msg'] == 'succ':
            self.session.get(response.json()['data']['url'])
            return True

        return False

    def get_cookies(self) -> dict:
        """
        获取 sub subp 等 cookie 数据
        :return: 含有 cookie 的字典
        """
        return self.session.cookies.get_dict()

    def update_cookies(self, d) -> dict:
        """
        更新 cookie
        :param d: 字典
        :return:
        """
        self.session.cookies.update(d)

    def get_mymblog(self, uid: int, page: int, since_id=None):
        """
        获取用户动态

        :param uid: 用户ID
        :param page: 第几页
        :param since_id: 切片ID可空，由第一次请求获取用户动态的响应提供。当为空串时，获取完毕。
        :return: 用户动态 data 字段
        """
        params = {
            'uid': uid,
            'page': page,
            'feature': '0'
        }

        if since_id:
            params['since_id'] = since_id

        response = self.session.get('https://weibo.com/ajax/statuses/mymblog', params=params)

        if response.json()['ok'] != 1:
            raise RuntimeError("获取用户动态失败，内容如下：" + str(response.content.decode()))

        return response.json()['data']

    def get_hottimeline(self, max_id=0, count=10):
        """
        获取热点博文。

        :param max_id: 页数，可取值 0、1、2......
        :param count: 获取数量
        :return: hottimeline 数据
        """
        params = {
            'refresh': '2',
            'group_id': '102803',
            'containerid': '102803',
            'extparam': 'discover|new_feed',
            'max_id': str(max_id),
            'count': str(count),
        }

        response = self.session.get('https://weibo.com/ajax/feed/hottimeline', params=params)

        return response.json()

    def login_as_visitor(self):
        """
        获取游客 sub subp 等验证 cookie，登录之后不要随意调用。
        :return:
        """
        headers = {
            'Referer': 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2Fajax%2Ffeed%2Fhottimeline%3Fsince_id%3D0%26refresh%3D0%26group_id%3D102803%26containerid%3D102803%26extparam%3Ddiscover%257Cnew_feed%26max_id%3D0%26count%3D10&domain=weibo.com&ua=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F126.0.0.0%20Safari%2F537.36%20Edg%2F126.0.0.0&_rand=1719903158969&sudaref='
        }

        data = {
            'cb': 'visitor_gray_callback',
            'tid': '',
            'from': 'weibo',
        }

        response = self.session.post('https://passport.weibo.com/visitor/genvisitor2', headers=headers, data=data)

        match = re.match(r'window.visitor_gray_callback && visitor_gray_callback\(([\s\S]*)\);',
                         response.content.decode())
        data = json.loads(match.group(1))['data']
        # next = data['next']
        sub = data['sub']
        subp = data['subp']
        # tid = data['tid']
        # confidence = data['confidence']
        # new_tid = data['new_tid']

        # print("next:", next)
        # print("sub:", sub)
        # print("subp:", subp)
        # print("tid:", tid)
        # print("confidence:", confidence)
        # print("new_tid:", new_tid)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Referer': 'https://passport.weibo.com/'
        }

        params = {
            'a': 'crossdomain',
            's': sub,
            'sp': subp,
            'from': 'weibo',
            '_rand': random.random(),
            'entry': 'miniblog',
            'url': 'https://weibo.com/',
        }

        response = self.session.get('https://login.sina.com.cn/visitor/visitor', params=params, headers=headers,
                                    allow_redirects=False)

        if response.status_code != 302:
            raise RuntimeError('无法获取sub subp。' + response.content.decode())

        return sub, subp

    def get_status(self, mblogid):
        """
        获取博文信息，需要提供 OlqFvpir3 的 mblogid 。
        :param mblogid: 博文 mblogid
        :return:
        """
        params = {
            'id': mblogid,
            'locale': 'zh-CN',
        }

        response = self.session.get('https://weibo.com/ajax/statuses/show', params=params)

        return response.json()

    def get_comments(self, id, user_id, max_id=None, count=10):
        """
        获取评论

        :param id: 博文数字ID
        :param user_id: 博文发布者ID
        :param max_id: 上次请求时获取的max_id
        :param count: 每次获取几个
        :return:
        """
        params = {
            'flow': '0',
            'is_reload': '1',
            'id': id,
            'is_show_bulletin': '2',
            'is_mix': '0',
            'count': str(count),
            'uid': user_id,
            'fetch_level': '0',
            'locale': 'zh-CN',
        }

        if max_id:
            params['max_id'] = max_id

        response = self.session.get('https://weibo.com/ajax/statuses/buildComments', params=params)

        return response.json()

    def get_hot_search(self):
        """
        获取热榜
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

        response = requests.get('https://weibo.com/ajax/side/hotSearch', headers=headers)

        if response.json()['ok'] != 1:
            raise RuntimeError('无法获取热榜。' + response.content.decode())

        return response.json()['data']
