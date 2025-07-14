import time
import asyncio
from fastmcp import Client
from fastmcp.client import SSETransport

import requests

transport = SSETransport("http://localhost:3000/sse")


async def sign(client, url, timestamp):
    res = await client.call_tool("sign", {"url": url, "timestamp": timestamp})
    return res.content[0].text


async def main():
    async with Client(transport) as client:
        mt = int(time.time())
        ms = await sign(client, "/api/v1/artworks/search", mt)
        response = requests.get("https://www.mihuashi.com/api/v1/artworks/search?page=1&type=recent", headers={
            'm-s': ms,
            'm-t': str(mt),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
        })
        print(response.content.decode())


asyncio.run(main())
