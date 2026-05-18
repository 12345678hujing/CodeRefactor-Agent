# 架构设计文档

## 1. 系统架构总览

CodeRefactor-Agent 采用 **Supervisor + Specialist Agents** 架构模式。Orchestrator Agent 作为中央调度器，负责任务解析、子 Agent 路由、上下文管理和结果聚合。

### 1.1 架构图

```
                    ┌─────────────────────────────┐
                    │    User / CI Trigger         │
                    │  (GitHub Webhook / CLI)      │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │     Orchestrator Agent       │
                    │  ┌───────────────────────┐  │
                    │  │  Task Parser          │  │
                    │  └───────────────────────┘  │
                    │  ┌───────────────────────┐  │
                    │  │  Context Manager      │  │
                    │  │  (long-term memory)   │  │
                    │  └───────────────────────┘  │
                    │  ┌───────────────────────┐  │
                    │  │  Agent Router         │  │
                    │  └───────────────────────┘  │
                    └──────────┬──────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  CodeReview     │  │   Refactor      │  │    Test         │
│  Agent          │  │   Agent         │  │    Agent        │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ • Diff 解析      │  │ • 重构方案生成   │  │ • 测试运行       │
│ • 代码异味检测   │  │ • 代码转换执行   │  │ • 测试生成       │
│ • 安全漏洞扫描   │  │ • 依赖分析       │  │ • 覆盖率分析     │
│ • 规范检查       │  │ • 架构对齐       │  │ • 回归验证       │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌─────────────────────────────┐
                    │     Summary Agent            │
                    │  ┌───────────────────────┐  │
                    │  │  报告生成              │  │
                    │  │  · 问题清单            │  │
                    │  │  · 重构前后对比        │  │
                    │  │  · Changelog          │  │
                    │  │  · PR 描述            │  │
                    │  └───────────────────────┘  │
                    └─────────────────────────────┘
```

### 1.2 Agent 通信协议

Agent 之间通过 **结构化消息队列** 通信，消息格式：

```json
{
  "task_id": "uuid",
  "agent_from": "orchestrator",
  "agent_to": "code_review_agent",
  "task_type": "code_review",
  "payload": {
    "repo_path": "/path/to/repo",
    "diff_content": "...",
    "context": { "branch": "feature/xxx" }
  },
  "memory_refs": ["kb_entry_123", "kb_entry_456"]
}
```

## 2. 长短期记忆系统

### 2.1 短期记忆（Session Context）
- 当前任务链的完整上下文
- Agent 间传递的中间结果
- MaxTokens: 128K (利用长上下文能力)

### 2.2 长期记忆（Vector Store）
- 项目架构知识
- 历史重构记录
- 编码规范与最佳实践
- 存储引擎: ChromaDB + sentence-transformers

## 3. 多 Agent 协作流程

### 3.1 串行协作（默认模式）
```
Orchestrator → CodeReview → Refactor → Test → Summary → Output
```

每个 Agent 依赖前一个 Agent 的输出作为输入，形成处理流水线。

### 3.2 并行协作（大型项目模式）
```
                    ┌→ CodeReview (module A) ─┐
Orchestrator → Split┤                         ├→ Merge → Test → Summary
                    └→ CodeReview (module B) ─┘
```

按模块拆分任务，并行处理后再合并结果。

### 3.3 反馈循环
```
CodeReview → Refactor → Test
                  ↑          │
                  └── Fail ──┘ (Test failed, retry refactor)
```

测试失败时触发 Refactor Agent 重试，最多 3 次。

## 4. 工具调用接口

每个 Agent 可以调用以下工具：

| 工具名 | 功能 | 权限 |
|--------|------|------|
| `read_file` | 读取文件内容 | 只读 |
| `write_file` | 写入文件内容 | 读写 |
| `run_command` | 执行 shell 命令 | 受限沙箱 |
| `git_diff` | 获取 git diff | 只读 |
| `git_commit` | 创建 commit | 读写 |
| `search_code` | 代码搜索 (grep) | 只读 |
| `run_tests` | 运行测试 | 读写 |
| `query_knowledge_base` | 查询长期记忆 | 只读 |
