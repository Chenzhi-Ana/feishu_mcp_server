# 飞书MCP机器人
[![smithery badge](https://smithery.ai/badge/@Chenzhi-Ana/feishu_mcp_server)](https://smithery.ai/server/@Chenzhi-Ana/feishu_mcp_server)

## 目标
通过将飞书机器人用MCP server 代理，可以让cursor或者Claude的用户，可以结合LLM的模型后使用飞书机器人执行业务逻辑

```
+----------------+      +-------------+      +-------------+      +----------------+
|                |      |             |      |             |      |                |
| Claude/Cursor  |----->| MCP Client  |----->| MCP Server  |----->| 飞书机器人      |
|                |      |             |      |             |      |                |
+----------------+      +-------------+      +-------------+      +----------------+


调用流程说明:
1. Claude/Cursor 通过 MCP Client 发送请求
2. MCP Client 将请求转发给 MCP Server
3. MCP Server 处理请求并调用飞书机器人API
4. 飞书机器人与飞书API交互

``

## 配置
uv --directory YOUR_PATH run bot.py --webhook YOUR_WEB_HOOK

替换这两部分为你的路径和机器人地址即可

### Installing via Smithery

To install feishu_mcp_server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@Chenzhi-Ana/feishu_mcp_server):

```bash
npx -y @smithery/cli install @Chenzhi-Ana/feishu_mcp_server --client claude
```

### Installing Manually
