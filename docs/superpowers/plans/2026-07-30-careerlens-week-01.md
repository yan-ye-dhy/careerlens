# CareerLens Week 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用一周掌握 Python 最核心的语法、函数、容器和字符串处理，并独立完成 CareerLens 的第一个 JD 文本清洗程序。

**Architecture:** 本周只构建本地 Python 命令行程序，不接入 LLM、数据库或 Web 框架。程序从文本文件读取招聘 JD，完成可重复、可测试的文本规范化，再把结果写入新文件。

**Tech Stack:** Python 3.12+、标准库、pytest、Git

---

## 本周交付物

计划创建以下文件：

```text
careerlens/
├── README.md
├── requirements-dev.txt
├── data/
│   ├── raw/
│   │   └── sample_jd.txt
│   └── processed/
├── src/
│   └── careerlens/
│       ├── __init__.py
│       ├── cleaner.py
│       └── cli.py
└── tests/
    └── test_cleaner.py
```

文件职责：

- `cleaner.py`：只负责 JD 文本清洗，不读写文件。
- `cli.py`：只负责命令行参数、文件读写和调用清洗函数。
- `test_cleaner.py`：验证清洗规则和边界情况。
- `sample_jd.txt`：脱敏练习数据，不使用个人隐私。

## Day 1：Python 运行环境与基本表达式（2.5 小时）

### 学习

- [ ] 阅读 Python 官方教程第 3 章：数字、文本、列表。
- [ ] 理解变量、`str`、`int`、`float`、`bool`、索引和切片。
- [ ] 在交互式解释器中亲手输入至少 20 条表达式。

资料：

- <https://docs.python.org/zh-cn/3/tutorial/introduction.html>

### 练习

- [ ] 写一个程序，保存岗位名称、城市、最低学历和技能列表。
- [ ] 打印一行摘要：`杭州 | AI Agent 实习生 | 本科 | Python, FastAPI`。
- [ ] 分别使用索引、切片和字符串方法处理岗位名称。

### 验收

- [ ] 不看资料解释 `list` 与 `str` 的可变性差别。
- [ ] 不借助 AI，从空文件写出上述摘要程序。
- [ ] 将当天不熟悉的语法记入 `README.md` 的“学习记录”。

## Day 2：条件、循环、字典与集合（2.5 小时）

### 学习

- [ ] 阅读官方教程第 4 章中 `if`、`for`、`range()` 和函数入门。
- [ ] 阅读第 5 章中字典、集合和循环技巧。

资料：

- <https://docs.python.org/zh-cn/3/tutorial/controlflow.html>
- <https://docs.python.org/zh-cn/3/tutorial/datastructures.html>

### 练习

给定：

```python
skills = ["Python", "FastAPI", "Python", "RAG", "Git", "  SQL  "]
```

- [ ] 去除重复项和多余空格。
- [ ] 保留原始出现顺序。
- [ ] 统计每项技能出现次数。
- [ ] 输出出现次数最高的技能。

目标结果：

```text
cleaned: ['Python', 'FastAPI', 'RAG', 'Git', 'SQL']
counts: {'Python': 2, 'FastAPI': 1, 'RAG': 1, 'Git': 1, 'SQL': 1}
top: Python
```

### 验收

- [ ] 分别说明为什么会选择 `list`、`dict` 和 `set`。
- [ ] 能解释 `for skill in skills` 每次循环中变量的值。
- [ ] 不使用第三方库完成练习。

## Day 3：函数与字符串清洗（3 小时）

### 学习

- [ ] 阅读官方教程 4.8-4.9：定义函数、参数和返回值。
- [ ] 掌握 `strip()`、`split()`、`join()`、`replace()` 和 `lower()`。
- [ ] 理解“函数只承担一个职责”。

### 实现目标

在 `src/careerlens/cleaner.py` 中设计以下接口：

```python
def normalize_whitespace(text: str) -> str:
    """合并连续空白，并去除首尾空白。"""


def remove_empty_lines(text: str) -> str:
    """删除空行，保留非空行的原始顺序。"""


def clean_jd(text: str) -> str:
    """按固定顺序组合本模块的清洗规则。"""
```

- [ ] 先在纸上或注释中写出每个函数的输入、输出和例子。
- [ ] 独立实现三个函数。
- [ ] 确保同一文本执行两次 `clean_jd()` 的结果不再变化。

### 验收

输入：

```text

  AI Agent   实习生

要求： Python   FastAPI

```

预期输出：

```text
AI Agent 实习生
要求： Python FastAPI
```

- [ ] 能解释为什么文件读写不应写进 `clean_jd()`。
- [ ] 能解释类型标注的作用。

## Day 4：文件、模块与异常（3 小时）

### 学习

- [ ] 阅读官方教程第 6、7、8 章的模块、文件与异常基础。
- [ ] 理解 `with open(..., encoding="utf-8")`。
- [ ] 理解 `try`、`except` 和异常信息。

资料：

- <https://docs.python.org/zh-cn/3/tutorial/modules.html>
- <https://docs.python.org/zh-cn/3/tutorial/inputoutput.html>
- <https://docs.python.org/zh-cn/3/tutorial/errors.html>

### 实现目标

在 `src/careerlens/cli.py` 中实现命令：

```powershell
python -m careerlens.cli data/raw/sample_jd.txt data/processed/sample_jd.txt
```

行为要求：

- [ ] 使用 UTF-8 读取输入文件。
- [ ] 调用 `clean_jd()`。
- [ ] 创建输出目录并写入结果。
- [ ] 输入文件不存在时打印清楚的错误并返回非零退出码。
- [ ] 不在 `cli.py` 中重复实现清洗逻辑。

### 验收

- [ ] 正常输入能生成清洗文件。
- [ ] 不存在的输入路径不会产生 Python traceback 给普通用户。
- [ ] 原始文件保持不变。

## Day 5：pytest 与测试思维（3 小时）

### 学习

- [ ] 理解“输入、行为、预期输出”。
- [ ] 安装 pytest，并理解测试通过与失败的输出。
- [ ] 区分正常情况、边界情况和异常情况。

准备：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pytest
python -m pip freeze > requirements-dev.txt
```

### 测试要求

在 `tests/test_cleaner.py` 中至少覆盖：

- [ ] 普通连续空格。
- [ ] Tab 与换行。
- [ ] 首尾空白。
- [ ] 多个空行。
- [ ] 空字符串。
- [ ] 纯空白字符串。
- [ ] 中文、英文和标点混合。
- [ ] `clean_jd()` 的幂等性。

运行：

```powershell
python -m pytest -v
```

预期：

```text
8 passed
```

### 验收

- [ ] 故意破坏一个清洗函数并观察测试失败。
- [ ] 根据失败信息定位到具体测试。
- [ ] 恢复实现并确认全部测试通过。

## Day 6：整合、重构与 Git（4 小时）

### 整合

- [ ] 准备一份 200-500 字的脱敏 JD。
- [ ] 从命令行完成读取、清洗和输出。
- [ ] 确认源文件、处理后文件和代码职责清楚。
- [ ] 删除没有使用的函数和重复代码。

### README

在 `README.md` 中写清：

- [ ] 项目当前解决什么问题。
- [ ] 环境安装命令。
- [ ] 运行命令。
- [ ] 测试命令。
- [ ] 当前支持的清洗规则。
- [ ] 当前不支持的能力：LLM 提取、数据库、RAG 和 Agent。

### Git

- [ ] 检查 `.venv/`、缓存和个人数据没有进入版本控制。
- [ ] 查看每个变更，提交一个语义清楚的 commit。

建议提交信息：

```text
feat: add initial JD text cleaner
```

### 验收

- [ ] 删除 `data/processed/sample_jd.txt` 后，可以通过 README 重建。
- [ ] `python -m pytest -v` 全部通过。
- [ ] `git status` 干净。

## Day 7：闭卷复现与周复盘（2 小时）

### 闭卷复现

- [ ] 不看旧代码，用 30-45 分钟重新写一个简化版清洗函数。
- [ ] 不借助 AI，解释数据从输入文件到输出文件的完整路径。
- [ ] 口述 `list`、`dict`、函数、模块、异常和测试分别解决什么问题。

### 复盘

在 `README.md` 的学习记录中回答：

1. 本周新增了什么可运行功能？
2. 哪部分代码仍无法脱离 AI 解释？
3. 本周最有价值的错误是什么？
4. 哪些测试证明功能正确？
5. 下周最需要补的知识是什么？

## 本周停止条件

满足以下条件才进入第二周：

- [ ] 能在空白文件中独立写出包含函数、循环、字典和文件读写的小程序。
- [ ] 能运行并解释全部测试。
- [ ] 能从命令行清洗一份真实但脱敏的 JD。
- [ ] 能解释项目三个 Python 文件的职责。
- [ ] 核心清洗函数不是由 AI 整段生成后直接粘贴。

若未全部满足，不是失败：第二周前 2-4 小时继续补齐，不应带着明显欠账进入 JSON、模块设计和 LLM API。

