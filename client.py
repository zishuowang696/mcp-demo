"""最小 MCP 客户端（stdio）。

握手 -> 列工具 -> 调用，仅此三步。
启动 server.py 子进程，通过 stdin/stdout 收发 JSON-RPC。
"""
import json
import subprocess
import sys

proc = subprocess.Popen(
    [sys.executable, "server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
)
_id = 0


def rpc(method: str, params: dict | None = None, notify: bool = False):
    global _id
    msg = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        msg["params"] = params
    if not notify:
        _id += 1
        msg["id"] = _id
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    return None if notify else json.loads(proc.stdout.readline())


# 1) 握手
rpc(
    "initialize",
    {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "demo", "version": "0.1"},
    },
)
rpc("notifications/initialized", notify=True)

# 2) 列工具  3) 调用
print("工具列表:", rpc("tools/list"))
print("调用结果:", rpc("tools/call", {"name": "cat", "arguments": {"path": "/etc/hostname"}}))
