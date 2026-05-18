# Agent 工作流文档

## 完整运行示例：代码重构工作流

### 场景

对一个遗留 Python 项目进行代码审查和重构，涉及：
- 检测过长的函数和重复代码
- 识别未处理的异常
- 优化数据库查询性能
- 自动生成单元测试

### 工作流日志 (终端模拟)

```
$ python main.py review --path ./legacy-project --auto-refactor

╔══════════════════════════════════════════════════════╗
║         CodeRefactor-Agent v1.0                      ║
║  多 Agent 协作代码审查与重构系统                      ║
╚══════════════════════════════════════════════════════╝

[Orchestrator] 接收任务: review + refactor
[Orchestrator] 目标仓库: ./legacy-project
[Orchestrator] 检测到 48 个 Python 文件, 12,340 行代码
[Orchestrator] 调用长期记忆: 查询项目历史上下文...
[Memory] 找到 3 条相关历史记录
[Orchestrator] 启动 CodeReview Agent...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CodeReview Agent — 分析阶段
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[CodeReview] 正在扫描文件: services/order_service.py
[CodeReview]   ✓ 检测到函数过长: process_order() (156行)
[CodeReview]   ✓ 检测到重复代码: 数据库查询模式重复 5 次
[CodeReview]   ✓ 检测到未处理异常: except 语句未指定异常类型
[CodeReview]   ⚠ 检测到 SQL 注入风险: f-string 拼接查询
[CodeReview] 正在扫描文件: models/user.py
[CodeReview]   ✓ 检测到循环引用: models/__init__.py
[CodeReview]   ✓ 检测到硬编码配置: DATABASE_URL
[CodeReview] 正在扫描文件: utils/validators.py
[CodeReview]   ✓ 检测到冗余代码: validate_email() 与 validate_user() 重复逻辑
...

[CodeReview] 审查完成: 发现 23 个问题
  - 严重: 3 (SQL注入, 未处理异常, 硬编码密钥)
  - 中等: 12 (函数过长, 重复代码, 循环引用)
  - 建议: 8 (命名规范, 注释缺失, 类型提示)
[CodeReview] 生成问题清单: issues.json
[CodeReview] 结果发送至 Orchestrator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Refactor Agent — 重构阶段
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Orchestrator] 启动 Refactor Agent...
[Refactor] 加载问题清单: 23 issues (优先处理 15 个严重/中等)
[Refactor] 处理问题 #1: 重构 process_order() — 拆分为 4 个函数
  ✓ get_order_items() — 提取订单项逻辑 (32行)
  ✓ calculate_totals() — 提取计算逻辑 (28行)
  ✓ validate_order() — 提取验证逻辑 (25行)
  ✓ save_order() — 提取持久化逻辑 (35行)
[Refactor] 处理问题 #2: 修复 SQL 注入 — 替换为参数化查询
  ✓ 替换 f-string 查询为 ? 占位符
[Refactor] 处理问题 #3: 提取公共查询方法 — repository 模式
  ✓ 创建 OrderRepository 类
[Refactor] 处理问题 #4: 修复异常处理
  ✓ 所有 except 添加具体异常类型
[Refactor] 处理问题 #5: 消除重复代码
  ✓ 合并 validate_email() 和 validate_user() 为通用 validator
...

[Refactor] 重构完成: 修改 12 个文件, 新增 3 个文件
[Refactor] 代码变更: -340 行 / +520 行
[Refactor] 结果发送至 Orchestrator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Test Agent — 验证阶段
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Orchestrator] 启动 Test Agent...
[Test] 运行现有测试套件...
[Test] 执行: pytest tests/ -v --tb=short
============================= test session starts =============================
collected 156 items

tests/test_models.py ......F..FF...                                      FAILED
tests/test_services.py ..........                                        PASSED
tests/test_utils.py .............                                        PASSED

[Test] ❌ 3 个测试失败 (重构导致预期行为变更)
[Test] 分析失败原因:
  - test_user_creation: 字段名变更 (email → contact_email)
  - test_order_total: 计算逻辑提取后接口变更
  - test_inventory_check: 数据库查询方式变更
[Test] 自动修复测试用例...
[Test] 重新运行测试...
============================= test session starts =============================
collected 162 items

tests/test_models.py ............                                        PASSED
tests/test_services.py ..........                                        PASSED
tests/test_utils.py .............                                        PASSED
tests/test_refactored.py NEW .....                                       PASSED

[Test] ✅ 全部 162 项测试通过
[Test] 覆盖率: 78% → 85% (+7%)
[Test] 新增测试用例: 6 个 (覆盖新提取的函数)
[Test] 结果发送至 Orchestrator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Summary Agent — 报告生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Summary] 生成重构报告...
[Summary] 生成 PR 描述...
[Summary] 生成 Changelog...

═══════════════════════════════════════════════════
  📋 重构总结报告
═══════════════════════════════════════════════════

  项目: legacy-project
  分支: refactor/auto-code-review-20260518
  变更: +520 / -340 行, 15 个文件

  问题修复:
  ✅ [严重] SQL 注入风险 — 替换为参数化查询
  ✅ [严重] 未处理异常 — 所有 except 指定异常类型
  ✅ [严重] 硬编码密钥 — 移至环境变量
  ✅ [中等] process_order() 过长 — 拆分为 4 个方法
  ✅ [中等] 重复数据库查询 — 引入 Repository 模式
  ✅ [中等] 循环引用 — 重构 __init__.py
  ✅ [中等] 冗余验证逻辑 — 合并 validator
  ✅ [建议] 添加类型提示 — 8 个函数补充 type hints

  测试结果:
  ✅ 162/162 测试通过
  📈 覆盖率: 78% → 85%
  🆕 新增测试用例: 6 个

  Token 消耗统计:
  - CodeReview:  24,580 tokens
  - Refactor:    128,340 tokens
  - Test:        45,210 tokens
  - Summary:     12,480 tokens
  ─────────────────────────
  Total:        210,610 tokens

═══════════════════════════════════════════════════

[Orchestrator] 任务完成.
[Orchestrator] 自动创建 PR: refactor/auto-code-review-20260518
[Orchestrator] PR URL: https://github.com/user/legacy-project/pull/42
```

## 2. 多 Agent 协作示意图

```
时间线 ────────────────────────────────────────────────────────►

Orchestrator  │■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
              │    │           │           │           │
CodeReview    │    ■■■■■■■■■■■■           │           │
Agent         │    │  代码分析  │           │           │
              │    └───────────┘           │           │
Refactor      │                ■■■■■■■■■■■■■■■■■      │
Agent         │                │   代码重构    │      │
              │                └───────────────┘      │
Test          │                           ■■■■■■■■■■■■■
Agent         │                           │ 测试验证 │
              │                           └──────────┘
Summary       │                                      ■■■■■■
Agent         │                                      │报告 │
              │                                      └─────┘
              └────────────────────────────────────────────────►
                                                             时间
```

## 3. 记忆系统工作流

```
请求到达
    │
    ▼
查询短期记忆 (当前 Session)
    │
    ├── 命中 → 直接复用上下文
    │
    └── 未命中
         │
         ▼
    查询长期记忆 (Vector Store)
         │
         ├── 命中 → 加载相关历史知识 → 注入 Agent 上下文
         │
         └── 未命中 → 从零开始分析
                         │
                         ▼
                    任务完成后 → 生成知识摘要 → 存入 Vector Store
```

## 4. Token 消耗预估

| 任务类型 | 输入 Token | 输出 Token | 总计 |
|---------|-----------|-----------|------|
| 代码审查 (小型项目, <5000行) | ~8K | ~2K | ~10K |
| 代码审查 (中型项目, 1-5万行) | ~30K | ~8K | ~38K |
| 代码重构 (单文件) | ~15K | ~5K | ~20K |
| 代码重构 (多文件) | ~60K | ~20K | ~80K |
| 测试生成+验证 | ~25K | ~10K | ~35K |
| 报告生成 | ~10K | ~3K | ~13K |

单次完整工作流 (中型项目): **约 150K - 300K Tokens**
