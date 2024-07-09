# API 开发平台 音乐解析爬虫

此项目是 [https://suapi.net/tool/music](ttps://suapi.net/tool/music) 的爬虫，可以在 Python 里面调用此网站获取音乐。

# 依赖

+ requests
+ js2py
+ bs4
+ lxml

# 架构说明

+ music_origin.js 是网页原来加密的 JavaScript 脚本
+ suapinet_verify.js 是经过解密后用于生成签名的 JavaScript 脚本
+ SuapinetMusic.py 是爬虫主程序

# 使用说明

## 解析音乐

```python
from SupinetMusic import SupinetMusic

sup = SupinetMusic()
print(sup.url("001zMQr71F1Qo8"))  # mid 是QQ音乐详情页的音乐ID，这个网站就是爬取QQ音乐的，允许VIP音乐。
```
