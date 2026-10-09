#!/usr/bin/env python3
"""麦当劳 MCP 连通性探针：验证 Token 有效并列出可用工具。

用法：
    MCD_MCP_TOKEN=你的token python3 scripts/mcp_probe.py
"""
import json
import os
import sys
import urllib.request

URL = "https://mcp.mcd.cn"


def rpc(token, method, params=None, req_id=1):
    body = json.dumps(
        {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}}
    ).encode()
    req = urllib.request.Request(
        URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {token}",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode().strip()
        return json.loads(raw) if raw else {}


def main():
    token = os.environ.get("MCD_MCP_TOKEN")
    if not token:
        print("请设置环境变量 MCD_MCP_TOKEN")
        sys.exit(1)
    init = rpc(token, "initialize", {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "mcd-probe", "version": "1.0"},
    })
    info = init.get("result", {}).get("serverInfo", {})
    print(f"✅ MCP 连接成功：{info.get('name')} v{info.get('version')}")
    tools = rpc(token, "tools/list", {}, 3).get("result", {}).get("tools", [])
    print(f"可用工具：{len(tools)} 个")
    for t in tools:
        print(f"  - {t['name']}")


if __name__ == "__main__":
    main()
