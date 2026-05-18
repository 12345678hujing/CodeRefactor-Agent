# CodeRefactor-Agent

多 Agent 协作的自动化代码审查与重构系统。

## 项目概述

CodeRefactor-Agent 是一个基于大语言模型的多 Agent 协作系统，能够自动分析代码仓库结构、识别技术债务和代码异味、生成重构方案、执行重构并自动运行测试验证。

## 核心架构

```
┌─────────────────────────────────┐
│      Orchestrator Agent         │  ← 任务编排与状态管理
│  (Supervisor + Router)          │
└──────────┬──────────┬───────────┘
           │          │
    ┌──────▼──┐  ┌───▼────────┐
    │ Code    │  │  Refactor  │
    │ Review  │  │  Agent     │
    │ Agent   │  │            │
    └────┬─────┘  └─────┬──────┘
         │              │
    ┌────▼─────┐  ┌────▼──────┐
    │  Test    │  │  Summary  │
    │  Agent   │  │  Agent    │
    └──────────┘  └───────────┘
```

## 核心功能

- **代码审查**: 自动扫描 PR/commit diff，检测代码异味、安全漏洞、性能问题
- **智能重构**: 根据架构规范生成重构方案并执行
- **自动化测试**: 重构后自动运行单元测试 + 生成补充测试用例
- **长短期记忆**: 使用向量存储维护项目上下文知识库
- **多 Agent 协作**: 每个 Agent 专注单一职责，Orchestrator 统一编排

## 技术栈

- **底层模型**: Claude Sonnet 4.6 / GPT-4o / MiMo-V2.5-Pro
- **Agent 框架**: OpenClaude / Claude Code CLI
- **工具链**: Git CLI, pytest, ESLint, Pylint
- **向量存储**: ChromaDB (本地), FAISS
- **CI/CD**: GitHub Actions

## 工作流程

1. 触发方式: GitHub Webhook / CLI 手动触发 / 定时任务
2. Orchestrator 接收任务，创建子 Agent
3. CodeReview Agent 分析代码，输出问题清单
4. Refactor Agent 生成重构代码
5. Test Agent 运行测试，确保通过
6. Summary Agent 生成重构报告 + Changelog
7. 自动创建 PR 或提交 commit

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填写 API Key

# 运行代码审查
python main.py review --path ./target-project

# 运行代码重构
python main.py refactor --path ./target-project --issue-list issues.json
```

## 项目结构

```
CodeRefactor-Agent/
├── main.py                    # 入口：CLI 调度
├── orchestrator/              # 编排器
│   ├── __init__.py
│   └── supervisor.py          # 任务路由与状态管理
├── agents/                    # Agent 实现
│   ├── __init__.py
│   ├── code_review_agent.py
│   ├── refactor_agent.py
│   ├── test_agent.py
│   └── summary_agent.py
├── memory/                    # 记忆模块
│   ├── __init__.py
│   ├── vector_store.py
│   └── knowledge_base.py
├── tools/                     # 工具函数
│   ├── __init__.py
│   ├── git_ops.py
│   ├── file_ops.py
│   └── test_runner.py
├── docs/                      # 文档
│   ├── architecture.md
│   └── workflow.md
├── screenshots/               # 运行截图
├── requirements.txt
└── .env.example
```
