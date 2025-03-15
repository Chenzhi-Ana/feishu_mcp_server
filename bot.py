import os
import sys
import argparse
from urllib.parse import urlparse

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("错误: 无法导入mcp模块。请确保已安装mcp包。")
    print("可以使用以下命令安装: uv pip install mcp")
    sys.exit(1)

import base64
import hashlib
import hmac
import requests
from datetime import datetime

# 默认webhook配置
DEFAULT_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/3fa479c9-fb0a-477b-a216-3b02c748ea1c"
DEFAULT_WEBHOOK_SECRET = "3fa479c9-fb0a-477b-a216-3b02c748ea1c"

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description='飞书机器人MCP服务')
    parser.add_argument('--webhook', type=str, help='飞书机器人webhook地址，格式为URL或URL#SECRET')
    return parser.parse_args()

# 从webhook参数解析URL和密钥
def parse_webhook(webhook_param):
    if not webhook_param:
        return DEFAULT_WEBHOOK_URL, DEFAULT_WEBHOOK_SECRET
    
    # 检查是否包含#分隔符
    if '#' in webhook_param:
        url, secret = webhook_param.split('#', 1)
        return url, secret
    
    # 如果只有URL，尝试从URL中提取token作为密钥
    url = webhook_param
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    # 从路径中提取最后一个部分作为token/secret
    path_parts = path.strip('/').split('/')
    if path_parts:
        secret = path_parts[-1]
        return url, secret
    
    # 如果无法提取，使用默认密钥
    return url, DEFAULT_WEBHOOK_SECRET

# 解析参数
args = parse_args()
WEBHOOK_URL, WEBHOOK_SECRET = parse_webhook(args.webhook)

# Initialize FastMCP server
mcp = FastMCP("weather")

# 每次发送消息时获取当前时间戳
def get_timestamp():
    return int(datetime.now().timestamp())

def gen_sign(secret, timestamp):
    # 拼接时间戳以及签名校验
    string_to_sign = '{}\n{}'.format(timestamp, secret)

    # 使用 HMAC-SHA256 进行加密
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()

    # 对结果进行 base64 编码
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


@mcp.tool()
async def send_message(state: str) -> str:
    """
    发送飞书消息
    
    Args:
        state: 要发送的消息内容
    """
    timestamp = get_timestamp()
    sign = gen_sign(WEBHOOK_SECRET, timestamp)
    params = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "text",
        "content": {"text": state},
    }

    resp = requests.post(WEBHOOK_URL, json=params)
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") and result.get("code") != 0:
        print(f"发送失败：{result['msg']}")
        return "发送失败：" + result['msg']
    print("消息发送成功")
    return "消息发送成功"

if __name__ == "__main__":
    print("启动飞书机器人MCP服务...")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"脚本路径: {__file__}")
    print(f"使用的Webhook URL: {WEBHOOK_URL}")
    print(f"使用的Webhook密钥: {WEBHOOK_SECRET[:4]}{'*' * (len(WEBHOOK_SECRET) - 8)}{WEBHOOK_SECRET[-4:] if len(WEBHOOK_SECRET) > 8 else ''}")
    mcp.run(transport='stdio')

