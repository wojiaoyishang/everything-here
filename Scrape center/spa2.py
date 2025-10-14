import hashlib
import base64
import time

import requests


# spa6 少另一个 offset 传入，在 r 中删去 offset 即可
def sign(url, offset):
    t = str(int(time.time()))
    r = [url, str(offset), t]
    s = hashlib.sha1(','.join(r).encode('utf-8')).hexdigest()
    return base64.b64encode(s.encode() + ",".encode() + t.encode()).decode('utf-8')


print(sign('/api/movie', 0))
