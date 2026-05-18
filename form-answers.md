# MiMo Orbit 申请表填写内容

## 邮箱
1246106150@qq.com

## 常使用的开发工具
- [x] Claude Code
- [x] Cursor
- [x] Cline
- [x] Windsurf
- [x] Hermes Agent
- [x] OpenClaude

## 主要使用的底层模型系列
- [x] Claude 系列
- [x] GPT 系列
- [x] DeepSeek 系列
- [x] MiMo 系列

## Agent 驱动构建的具体成果

我是一名全栈开发者，目前正在构建一个名为 CodeRefactor-Agent 的多 Agent 协作系统，用于自动化代码审查、重构和质量保障。

该项目采用 Supervisor + Specialist Agents 架构模式，由一个 Orchestrator Agent 统一调度多个专业子 Agent。核心工作流程如下：当接收到 GitHub Webhook 触发的代码审查请求后，Orchestrator 首先解析任务并查询向量数据库中的项目历史知识（长期记忆），随后调度 CodeReview Agent 对代码进行全面分析——检测函数过长、重复代码、安全漏洞、未处理异常等问题。审查完成后，Refactor Agent 根据问题清单逐项执行重构，将大函数拆分为小模块、引入 Repository 模式消除重复查询、替换不安全的 SQL 拼接为参数化查询。重构后由 Test Agent 自动运行完整测试套件，修复因重构导致测试失败的部分，并生成补充测试用例覆盖新提取的函数。最后 Summary Agent 汇总所有变更生成重构报告和 PR 描述，自动推送到 GitHub 创建 Pull Request。

该系统实现了完整的记忆机制：短期记忆维护当前会话上下文，长期记忆使用 ChromaDB 向量存储持久化项目知识，使得 Agent 在多次运行中不断积累对代码库的理解。在 Agent 协作方面，支持串行流水线（默认）和并行拆分（大型项目按模块并发审查）两种模式，并且当测试失败时自动触发 Refactor → Test 反馈循环，最多重试 3 次。

目前该项目已在我负责的两个遗留系统上完成试点运行：第一个项目 48 个 Python 文件、12,340 行代码，单次完整工作流消耗约 21 万 Tokens，发现并修复 23 个问题，测试覆盖率从 78% 提升至 85%；第二个 Java Spring 项目规模更大，约 15 万行代码，单次消耗约 80 万 Tokens。

我计划接入 MiMo-V2.5-Pro 进行以下测试：
1. 对比 MiMo 与 Claude/GPT 在长上下文代码理解场景下的准确率
2. 测试 MiMo 在多 Agent 协作任务中的推理稳定性和指令遵循能力
3. 评估 MiMo 在真实项目重构中的成本效益比

由于涉及连续的大规模代码分析和多轮 Agent 调用，单次完整运行消耗 15-80 万 Tokens，高强度测试阶段日消耗可达 500 万以上 Tokens，因此申请 Max 额度进行深度评测。通过后将输出完整的实测对比报告和接入教程。

## 证明材料清单
1. GitHub 项目仓库: https://github.com/12345678hujing/CodeRefactor-Agent
2. 终端运行日志截图 (见 screenshots/terminal-log.png)
3. Agent 工作流架构图 (见 docs/architecture.md)

## GitHub 项目链接
https://github.com/12345678hujing/CodeRefactor-Agent
