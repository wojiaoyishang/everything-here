import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from starlette.background import BackgroundTask

import httpx


async def on_startup():
    client = httpx.AsyncClient(timeout=None)
    app.state.client = client


async def on_shutdown():
    client = app.state.client
    await client.aclose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def proxy_to_response(request: Request, path) -> httpx.Response:
    target_url = f"https://api.siliconflow.cn/v1/{path}"
    query_params = dict(request.query_params)

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in ["host", "content-length"]
    }

    client = app.state.client

    try:
        client_request = client.build_request(
            method=request.method,
            url=target_url,
            params=query_params,
            headers=headers,
            content=await request.body()
        )

        return await client.send(client_request, stream=True)

    except httpx.TimeoutException:
        return {"error": "Gateway timeout"}, 504
    except Exception as e:
        return {"error": str(e)}, 500


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def reverse_proxy(request: Request, path: str):
    if path == "chat/completions":  # 生成回应
        return await chat_completions(request, path)

    response = await proxy_to_response(request, path)

    return StreamingResponse(
        response.aiter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type"),
        background=BackgroundTask(response.aclose)
    )


async def chat_completions(request: Request, path: str):
    response = await proxy_to_response(request, path)

    json_body = json.loads(await request.body())
    streaming = json_body.get("stream", False)

    if not streaming:
        return Response(
            await response.aread(),
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
            background=BackgroundTask(response.aclose)
        )

    async def streaming_data():
        is_thinking = False
        async for data in response.aiter_lines():

            # 处理思考段
            if data[:12] == 'data: [DONE]':
                continue

            if data[:5] == 'data:':

                chunk = json.loads(data[5:])
                for choices in chunk.get('choices'):
                    delta = choices.get('delta')

                    if delta is None:
                        continue

                    content = delta.get('content')
                    reasoning_content = delta.get('reasoning_content')

                    if content is not None and is_thinking:
                        is_thinking = False
                        delta['content'] += '</think>'

                    if reasoning_content is None:
                        continue

                    if not is_thinking:
                        is_thinking = True

                        if content is None:
                            delta['content'] = ''
                            content = ''

                        delta['content'] += '<think>'

                    if content is None:
                        delta['content'] = reasoning_content

                yield 'data: ' + json.dumps(chunk) + '\n'

                continue

            yield data + '\n'

    return StreamingResponse(
        streaming_data(),
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type"),
        background=BackgroundTask(response.aclose)
    )
