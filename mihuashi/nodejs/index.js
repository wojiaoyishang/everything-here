const express = require('express');
const bodyParser = require('body-parser');
const {McpServer} = require('@modelcontextprotocol/sdk/server/mcp.js');
const {SSEServerTransport} = require('@modelcontextprotocol/sdk/server/sse.js');
const { z } = require('zod')

const {Ee} = require('./signer')

const app = express();
app.use(bodyParser.json());

const server = new McpServer({name: 'sse-tools', version: '1.0.0'});


// =============== 注册工具开始 ===============

server.tool('sign', {url: z.string(), timestamp: z.number()}, async ({url, timestamp}) => {
    var signer = await Ee();
    return {
        content: [
            {type: 'text', text: signer.sign(url, timestamp)}
        ]
    };
});



// =============== 注册工具结束 ===============


let transport = null;

// SSE 连接入口：客户端用 GET 建立 SSE 流
app.get('/sse', (req, res) => {
    transport = new SSEServerTransport('/msg', res);
});

// POST 消息入口：客户端向 /msg 发 RPC 请求
app.post('/msg', async (req, res) => {
    if (!transport) return res.status(400).end();
    await transport.handlePostMessage(req, res, req.body); // 处理 JSON-RPC 消息
});

const port = 3000;
app.listen(port, () => console.log(`MCP SSE server listening at http://localhost:${port}`));
