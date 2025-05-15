__author__ = "Yishang"
__version__ = "1.0"

import js2py
import requests
from bs4 import BeautifulSoup


def import_js(filename):
    """导入 js 文件到 Python 模块"""
    js = []
    with open(filename, "r", encoding="utf-8") as f:
        exec(js2py.translate_js(f.read()) + "\njs.append(var.to_python())", {'js': js})
    return js[0]


class SupinetMusic:
    suapinet_verify = import_js("suapinet_verify.js")  # 导入验证模块

    def __init__(self, token=None, auto_flush=True, session=requests.Session()):
        """
        API 开放平台音乐获取API

        :param token: 如果指定 token 则使用用户指定的 token ，否则将自动获取 token 。
        :param auto_flush: 自动刷新 token ，当 token 到期时自动刷新。
        :param session: requests 请求的 session 。会保存在 self.session 中。
        """
        self.session = session
        self.auto_flush = auto_flush

        if token is not None:
            self.token = token
        else:
            self.get_token()

        session.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
            }
        )

        return

    def sign_sha1(self, text):
        """
        API 开发平台自制的一种算法。
        :return:
        """
        return self.suapinet_verify.sign_sha1(text)

    def sign_url(self, url):
        """
        为 URL 签名

        :param url: URL
        :return:
        """
        return self.suapinet_verify.sign_url(url)

    def get_token(self, token=None, auto_flush=True):
        """
        获取 token，如果指定 token 则使用用户指定的 token ，否则将自动获取 token 。

        :param token: token
        :param auto_flush: 自动重新获取 token
        :return:
        """
        if token is None:
            response = self.session.get("https://suapi.net/tool/music")

            assert response.status_code == 200, response.text + "\n服务器请求失败。"

            soup = BeautifulSoup(response.text, "lxml")
            self.token = soup.find(id='music-so').attrs['token']
        else:
            self.token = token

        self.auto_flush = auto_flush

        return self.token

    def request_api(self, api_type, **kwargs):
        """
        请求获取 API。 由于 API 开放平台的接口都是同一在一个接口请求的，所以这里写一个统一类。

        解析音乐请看：https://suapi.net/doc/65

        :param api_type: 接口类型
        :param word: 关键词
        :return:
        """
        URL = f"api?token={self.token}&type={api_type}"
        for key, value in kwargs.items():
            URL += f"&{key}={value}"

        # 进行签名
        URL = self.sign_url(URL)

        response = self.session.get("https://suapi.net/tool/" + URL, allow_redirects=False)

        if response.status_code == 302:
            return response.headers['location']

        assert response.status_code == 200, response.text + "\n服务器错误。"

        if response.json()['code'] == 403 and self.auto_flush:
            self.get_token()
            return self.request_api(api_type, **kwargs)
        elif response.json()['code'] != 200:
            assert False, str(response.json()['code']) + f"\n{response.json()['msg']}" + "\n服务器错误。"

        return response.json()['data']

    def splcloud(self, word):
        """
        获取联想关键词。

        返回值 Belike:

        {'album': {'count': 2, 'itemlist': [{'docid': '27214674', 'id': '27214674', 'mid': '001Pmc1i0wSykZ', 'name': '清明雨上',
                                         'pic': 'http://y.gtimg.cn/music/photo_new/T002R180x180M000001Pmc1i0wSykZ_1.jpg',
                                         'singer': '南辰Music/汪制富'},
                                        {'docid': '26695436', 'id': '26695436', 'mid': '000fI2tH2pjiQO', 'name': '清明雨上',
                                         'pic': 'http://y.gtimg.cn/music/photo_new/T002R180x180M000000fI2tH2pjiQO_1.jpg',
                                         'singer': '熏悟空'}], 'name': '专辑', 'order': 2, 'type': 3}, 'mv': {'count': 1,
                                                                                                              'itemlist': [{
                                                                                                                  'docid': '1373616',
                                                                                                                  'id': '1373616',
                                                                                                                  'mid': '000HiRS90mwk90',
                                                                                                                  'name': '清明雨上',
                                                                                                                  'singer': '许嵩',
                                                                                                                  'vid': 'i0024jthenm'}],
                                                                                                              'name': 'MV',
                                                                                                              'order': 3,
                                                                                                              'type': 4},
     'singer': {'count': 0, 'itemlist': [], 'name': '歌手', 'order': 1, 'type': 2}, 'song': {'count': 4, 'itemlist': [
        {'docid': '460874', 'id': '460874', 'mid': '0027bOQj10UqLl', 'name': '清明雨上', 'singer': '许嵩'},
        {'docid': '458735564', 'id': '458735564', 'mid': '003bAyKt39GCtQ', 'name': '清明雨上',
         'singer': '禾初初（HE改名版）'},
        {'docid': '105595898', 'id': '105595898', 'mid': '001SKFAA1XUOCj', 'name': '清明雨上', 'singer': '段银莹'},
        {'docid': '295767890', 'id': '295767890', 'mid': '0027WAYc0ii7HE', 'name': '清明雨上', 'singer': ''}],
                                                                                             'name': '单曲', 'order': 0,
                                                                                             'type': 1}}

        :return:
        """
        return self.request_api("splcloud", word=word)

    def so(self, word, page=1, per_page=10):
        """
        搜索歌曲。

        当 meta 中的 nextpage 为 -1 时，没有下一页。

        :param word: 关键词
        :param page: 第几页
        :param per_page: 每页个数
        :return:
        """
        return self.request_api("so", word=word, page=page, per_page=per_page)

    def lrc(self, mid):
        """
        获取 lrc 歌词
        :param mid: 歌曲ID
        :return:
        """
        return self.request_api("lrc", mid=mid, format="json")

    def url(self, mid, size="m4a"):
        """
        获取歌曲链接。


        :param mid:  歌曲ID
        :param size: 留空默认m4a试听音质，可选参数：mp3:普通音质、hq:高品质、sq:无损、hires:HiRes音质。
        :return:
        """
        return self.request_api("url", mid=mid, size=size)



if __name__ == '__main__':
    # 由于音乐查询被关闭，所以该程序已经失效！
    sup = SupinetMusic()
    print(sup.url("001zMQr71F1Qo8", "mp3"))
