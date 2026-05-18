#!/usr/bin/env python3
"""生成终端日志截图"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 680
BG = (18, 18, 18)
GREEN = (0, 200, 80)
WHITE = (220, 220, 220)
GRAY = (140, 140, 140)
CYAN = (80, 200, 255)
YELLOW = (255, 200, 50)
RED = (255, 80, 80)
BLUE = (80, 160, 255)
MAGENTA = (200, 120, 255)

lines = [
    (GRAY, "$ python main.py review --path ./legacy-project --auto-refactor"),
    (None, None),
    (GREEN, "╔══════════════════════════════════════════════════════════════╗"),
    (GREEN, "║           CodeRefactor-Agent v1.0                            ║"),
    (GREEN, "║    多 Agent 协作代码审查与重构系统                            ║"),
    (GREEN, "╚══════════════════════════════════════════════════════════════╝"),
    (None, None),
    (CYAN,  "  [Orchestrator] 接收任务: review + refactor"),
    (CYAN,  "  [Orchestrator] 目标仓库: ./legacy-project"),
    (CYAN,  "  [Orchestrator] 检测到 48 个 Python 文件, 12,340 行代码"),
    (CYAN,  "  [Orchestrator] 调用长期记忆: 查询项目历史上下文..."),
    (GRAY,  "  [Memory] 找到 3 条相关历史记录"),
    (CYAN,  "  [Orchestrator] 启动 CodeReview Agent..."),
    (None, None),
    (YELLOW, "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"),
    (YELLOW, "    CodeReview Agent — 分析阶段"),
    (YELLOW, "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"),
    (None, None),
    (WHITE,  "  [CodeReview] 正在扫描文件: services/order_service.py"),
    (GREEN,  "  [CodeReview]   ✓ 检测到函数过长: process_order() (156行)"),
    (GREEN,  "  [CodeReview]   ✓ 检测到重复代码: 数据库查询模式重复 5 次"),
    (GREEN,  "  [CodeReview]   ✓ 检测到未处理异常"),
    (RED,    "  [CodeReview]   ⚠ 检测到 SQL 注入风险: f-string 拼接查询"),
    (WHITE,  "  [CodeReview] 正在扫描文件: models/user.py"),
    (GREEN,  "  [CodeReview]   ✓ 检测到循环引用: models/__init__.py"),
    (WHITE,  "  [CodeReview] 正在扫描文件: utils/validators.py"),
    (GREEN,  "  [CodeReview]   ✓ 检测到冗余代码"),
    (None, None),
    (BLUE,   "  [CodeReview] 审查完成: 发现 23 个问题"),
    (RED,    "    - 严重: 3 (SQL注入, 未处理异常, 硬编码密钥)"),
    (YELLOW, "    - 中等: 12 (函数过长, 重复代码, 循环引用)"),
    (GRAY,   "    - 建议: 8 (命名规范, 注释缺失, 类型提示)"),
    (None, None),
    (CYAN,  "  [Orchestrator] 启动 Refactor Agent..."),
    (WHITE,  "  [Refactor] 处理问题 #1: 重构 process_order()"),
    (WHITE,  "    ✓ 拆分为 4 个独立函数 (get/calculate/validate/save)"),
    (WHITE,  "  [Refactor] 处理问题 #2: 修复 SQL 注入"),
    (WHITE,  "    ✓ 替换 f-string 查询为参数化查询 (? 占位符)"),
    (None, None),
    (CYAN,  "  [Orchestrator] 启动 Test Agent..."),
    (WHITE,  "  [Test] 运行测试套件: pytest tests/ -v"),
    (GREEN,  "  [Test] ✅ 162/162 测试通过"),
    (GREEN,  "  [Test] 📈 覆盖率: 78% → 85% (+7%)"),
    (None, None),
    (MAGENTA,"  ══════════════════════════════════════════════════════════"),
    (MAGENTA,"  📋 重构总结报告"),
    (MAGENTA,"  ══════════════════════════════════════════════════════════"),
    (WHITE,  "    变更: +520 / -340 行    测试: ✅ 162/162 通过"),
    (WHITE,  "    Token 消耗: 210,610 tokens"),
    (GREEN,  "    ✅ 任务完成. PR 已自动创建."),
]

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

font = None
for path in [
    "C:/Windows/Fonts/consola.ttf",
    "C:/Windows/Fonts/consolab.ttf",
    "C:/Windows/Fonts/cour.ttf",
]:
    if os.path.exists(path):
        try:
            font = ImageFont.truetype(path, 14)
            break
        except:
            continue

if font is None:
    font = ImageFont.load_default()

y = 12
for color, text in lines:
    if text is None:
        y += 6
        continue
    if color:
        draw.text((14, y), text, fill=color, font=font)
    y += 19

out = "D:/ZDH/CodeRefactor-Agent/screenshots/terminal-log.png"
img.save(out, "PNG")
print(f"saved: {out}")
