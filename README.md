# mcp-demo

> **MCP（Model Context Protocol）= 标准化的 Function Calling。**

一个**完整、可跑**的最小 MCP 示例：用约 30 行实现一个 stdio 的 **MCP 服务端**（暴露 `cat` 工具），再用约 30 行实现一个**客户端**（握手 → 列工具 → 调用）。

不依赖任何 MCP 库，只为了把"它到底是什么"讲透。

## 运行

```bash
python client.py
```

输出：

```
工具列表: {'tools': [{'name': 'cat', 'description': '读取一个文件的全部内容', ...}]}
调用结果: {'content': [{'type': 'text', 'text': 'your-hostname'}]}
```

## 三个角色

- **Host**：你的 LLM 应用（Claude Desktop / Cursor / 自己的 Agent）
- **Client**：Host 内部与 Server 通信的一小块
- **Server**：你写的进程，暴露 Tools / Resources / Prompts

## 本质

```
读一行 JSON  ->  按 method 分发  ->  写一行 JSON
```

还是那个循环：**问模型 → 执行工具 → 回喂结果**。MCP 只是把"工具"标准化，让任何 LLM 应用都能复用。

## 相关

- 文章：<https://embedai.com.cn/posts/mcp-in-30-lines>
- 姊妹仓库（Agent 主循环）：<https://github.com/zishuowang696/agent-from-scratch>

## 反馈

有问题或建议？到 GitHub 提 **[Issue](https://github.com/zishuowang696/mcp-demo/issues)**，或在文章下方评论。

## 许可

MIT
