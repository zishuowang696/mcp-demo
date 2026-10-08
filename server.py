"""最小 MCP 服务端（stdio）。

MCP Server 的本质：读一行 JSON（JSON-RPC）-> 按 method 分发 -> 写一行 JSON。
暴露一个工具：cat（读取文件内容）。
"""
import json
import subprocess
import sys

TOOLS = [
    {
        "name": "cat",
        "description": "读取一个文件的全部内容",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "文件路径"}},
            "required": ["path"],
        },
    }
]


def handle(msg: dict) -> dict:
    m = msg["method"]
    if m == "initialize":
        return {
            "protocolVersion": msg["params"]["protocolVersion"],
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "cat-mcp", "version": "0.1"},
        }
    if m == "tools/list":
        return {"tools": TOOLS}
    if m == "tools/call":
        path = msg["params"]["arguments"]["path"]
        out = subprocess.run(["cat", path], capture_output=True, text=True)
        return {"content": [{"type": "text", "text": out.stdout or out.stderr}]}
    return {}


for line in sys.stdin:
    req = json.loads(line)
    if "id" not in req:  # 通知（notification），不需要回
        continue
    res = handle(req)
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": res}) + "\n")
    sys.stdout.flush()
