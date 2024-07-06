# Python 微博爬虫

## 目标 

- 获取微博热榜
- 获取微博博文
- 获取博文评论

## 实践

使用 Python 爬虫进行词频统计，分析网友评论倾向。

- 获取某一条博文的所有评论
- 分词、统计词频
- 制作词云

# 流程与分析

### 获取 XSRF-TOKEN

需要先获取 `XSRF-TOKEN` ，请求如下接口即可：（这一步不定需要，但是前端每一部请求都携带有 XSRF-TOKEN 所以还是要获取一下）
_GET_ https://weibo.com/newlogin

参数：

```python
params = {
    'tabtype': 'weibo',
    'gid': '102803',  # 貌似是固定的
    'openLoginLayer': '0',
    'url': 'https://weibo.com/',
}
```

### 热榜请求

URL：_GET_ https://weibo.com/ajax/side/hotSearch

不需要任何验证，直接可以请求。

### 获取推荐博文

URL：_GET_ https://weibo.com/ajax/feed/hottimeline

参数：

```python
params = {
    'since_id': '0',
    'refresh': '0',
    'group_id': '102803',
    'containerid': '102803',
    'extparam': 'discover|new_feed',
    'max_id': '0',
    'count': '10',
}
```

如果没有进行游客验证会被重定向到：_GET_ https://passport.weibo.com/visitor/visitor 进行游客验证。

参数：

```python
params = {
    'entry': 'miniblog',
    'a': 'enter',
    'url': ''  # 自定义来时的链接
}
```

**经过测试发现不需要先访问这个地址，可以直接去游客验证请求**

游客验证请求（获取门票）：

_POST_ https://passport.weibo.com/visitor/genvisitor2

参数：

```python
params = {
    'cb': 'visitor_gray_callback',
    'tid': '',  # 可以不填
    'from': 'weibo',
}
```

服务器会响应类似如下的内容：

```angular2html
window.visitor_gray_callback &&
visitor_gray_callback({"retcode":20000000,"msg":"succ","data":
        {"next":"cross_domain","sub":"_2AkMR3yxzf8NxqwFRmfwTyWLmZIhzzAjEieKng92oJRMxHRl-yj9kqhQItRB6Ol8CnIdwUDcyy_MV5xEsWRW6mxQNIM5P",
        "subp":"0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhKudzL7vNo6rVgM_I8.Nfw","alt":"","savestate":0,
        "tid":"01Aa9SQlUD5uH1PaX5dB4hUTYf1vHk_1S3H6bnpEw2bN1p","new_tid":false,"confidence":90}});
```

我们需要用到其中的几个参数：`sub`、`subp`。可以使用正则表达式匹配。

然后用如上的参数重新去请求：

GET https://login.sina.com.cn/visitor/visitor

```python
params = {
    'a': 'crossdomain',  # 踩的坑：`a` 参数是固定 `crossdomain` 而不是服务器传来的 `next` 参数值。
    's': sub,
    'sp': subp,
    'from': 'weibo',
    '_rand': random.random(),
    'entry': 'miniblog',
    'url': 'https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=0&group_id=102803&containerid=102803&extparam=discover%7Cnew_feed&max_id=0&count=10',
}
```

触发 302 跳转则代表验证通过。

### 获取长文本

GET https://weibo.com/ajax/statuses/longtext

参数：

```python
params = {
    'id': ''  # 博文 mblogid
}
```

### 扫码登录

+ 前置验证
  请求 _GET_ https://passport.weibo.com/sso/signin 获取 `X-CSRF-TOKEN`

参数：

```python
params = {
    'entry': 'miniblog',
    'source': 'miniblog',
    'disp': 'popup',
    'url': 'https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F',  # 重定向
}
```

+ 获取二维码门票

请求 _GET_ https://passport.weibo.com/sso/v2/qrcode/image

参数：

```python
params = {
    'entry': 'miniblog',
    'size': '180',
}
```

请求标头带上 `X-Csrf-Token`

```python
headers = {
    'Referer': 'https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&disp=popup&url=https%3A%2F%2Fweibo.com'
}
```

**需要先获取 `X-Csrf-Token` 。**

响应：

```json
{
  "retcode": 20000000,
  "msg": "succ",
  "data": {
    "qrid": "2MmZmg8E_AAM_bZzVmsg0CUhy_3DqSvEHBnFyY29kZQ..",
    "image": "https:\/\/v2.qr.weibo.cn\/inf\/gen?api_key=a0241ed0d922e7286303ea5818292a76&data=https%3A%2F%2Fpassport.weibo.cn%2Fsignin%2Fqrcode%2Fscan%3Fqr%3D2MmZmg8E_AAM_bZzVmsg0CUhy_3DqSvEHBnFyY29kZQ..%26sinainternalbrowser%3Dtopnav%26showmenu%3D0&datetime=1719910719&deadline=0&level=M&logo=https%3A%2F%2Fimg.t.sinajs.cn%2Ft6%2Fstyle%2Fimages%2Findex%2Fweibo-logo.png&output_type=img&redirect=0&sign=75306149231bc90427b64f08148a6123&size=180&start_time=0&title=sso&type=url"
  }
}
```

+ 获取二维码图片（生成二维码图片）

这个其实就是上一个接口的 image 数据，格式为 png 。

请求 _GET_ https://v2.qr.weibo.cn/inf/gen

参数：

```python
params = {
    'api_key': 'a0241ed0d922e7286303ea5818292a76',
    'data': 'https://passport.weibo.cn/signin/qrcode/scan?qr=2MmZmg8E_AAM_bZzVmsg0CUhy_3DqSvEHBnFyY29kZQ..&sinainternalbrowser=topnav&showmenu=0',
    'datetime': '1719910719',
    'deadline': '0',
    'level': 'M',
    'logo': 'https://img.t.sinajs.cn/t6/style/images/index/weibo-logo.png',
    'output_type': 'img',
    'redirect': '0',
    'sign': '75306149231bc90427b64f08148a6123',
    'size': '180',
    'start_time': '0',
    'title': 'sso',
    'type': 'url',
}

```

+ 巡回查码

请求 _GET_ https://passport.weibo.com/sso/v2/qrcode/check

参数：

```python
params = {
    'entry': 'miniblog',
    'source': 'miniblog',
    'url': 'https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F',
    # 重定向地址
    'qrid': '2MmZmg8E_AAM_bZzVmsg0CUhy_3DqSvEHBnFyY29kZQ..',  # 二维码id
    'disp': 'popup',
}
```

未扫描情况响应：

```json
{
  "retcode": 50114001,
  "msg": "未使用",
  "data": null
}
```

已扫描情况响应：

```json
{
  "retcode": 20000000,
  "msg": "succ",
  "data": {
    "url": "跳转URL"
  }
}
```

请求标头带上 `X-Csrf-Token`

```python
headers = {
    'Referer': 'https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&disp=popup&url=https%3A%2F%2Fweibo.com'
}
```

+ 验证登录的方法

请求 _GET_ https://weibo.com/ajax/log/action

查看返回标头是否含有 `X-Log-Uid` 如果有则是用户ID。

### 获取评论

请求 _GET_ https://weibo.com/ajax/statuses/buildComments 获取评论。

参数：

```python
params = {
  'flow': '0',  # 按热度，1为按时间
  'is_reload': '1',
  'id': '博文数字ID',
  'is_show_bulletin': '2',
  'is_mix': '0',
  'count': '几个',
  'uid': '发文博主ID',
  'fetch_level': '0',
  'locale': 'zh-CN',
  'max_id': ''  # 用于下一趟加载评论，会这个值第一次请求这个接口时会提供，为0则已经获取全部
}
```

## 模块使用例子

```python
from weibo import Weibo

wb = Weibo()
```

### 游客登录

```python
wb.login_as_visitor()
print(wb.get_hottimeline())
```

### 扫码登录

```python
import time

qrcode, data = wb.get_login_qrcode()
login = wb.check_qrcode(qrcode)
count = 0
while not login:
    time.sleep(1)
    login = wb.check_qrcode(qrcode)
    print(f"\r等待扫码登录......({count}s)", end="")
    count += 1
print("\r", end="")
print("登录成功。")
```

### 获取动态

```python
# 获取用户动态
data = wb.get_mymblog(uid=7467555881,
                      page=0)

since_id = data['since_id']
for blog in data['list']:
    print("-" * 150)
    print("发布者：", blog['user']['screen_name'])
    print("发布时间：", blog['created_at'])
    print("发布内容：\n" + blog['text_raw'])
    print("博文ID：", blog['idstr'])
```

### 获取博文

```python
blog = wb.get_status("Nw310uTcQ")
print("发布者：", blog['user']['screen_name'])
print("博文发布时间：", blog['created_at'])
print("发布内容：\n" + blog['text_raw'])
print("博文数字ID：", blog['idstr'])
```


### 获取评论

```python
info = wb.get_comments(id=blog['idstr'],
                       user_id=blog['user']['id'],
                       count=10)

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
```

### 获取热榜

```python
for realtime in wb.get_hot_search()['realtime']:
    print(realtime['word'])
```