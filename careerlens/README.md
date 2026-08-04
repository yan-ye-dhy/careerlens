# CareerLens

CareerLens 当前是一个本地 Python 命令行程序。它从 UTF-8 文本文件读取招聘 JD，规范化空白字符、删除空行，再将结果写入新的文本文件，同时保留原始输入。

这是 Week 1 的工程版本，重点是练习 Python 核心语法、模块、文件读写、异常处理、自动化测试和 Git。

## 当前功能

- 从命令行接收输入文件路径和输出文件路径。
- 使用 UTF-8 读取和写入中文招聘文本。
- 调用独立的文本清洗模块处理 JD。
- 在需要时自动创建输出文件的父目录。
- 输入文件不存在时显示清楚错误并返回非零退出码。
- 通过 pytest 自动检查主要清洗规则和边界情况。

## 项目结构

```text
careerlens/
├── data/
│   ├── raw/
│   │   └── sample_jd.txt       # 脱敏的原始练习输入
│   └── processed/              # 运行程序后生成的处理结果
├── practice/
│   └── week1/                  # Week 1 的 Python 基础练习
├── src/
│   └── careerlens/
│       ├── __init__.py         # Python 包标识
│       ├── cleaner.py          # 只负责字符串清洗
│       └── cli.py              # 参数、文件、异常与程序入口
├── tests/
│   └── test_cleaner.py         # cleaner.py 的自动化测试
├── README.md
└── requirements-dev.txt        # 开发和测试依赖
```

`.venv/`、Python 缓存、pytest 缓存和 `data/processed/` 都是本机生成内容，不属于项目源码，也不进入 Git 提交。

## 环境准备

需要 Python 3.12 或兼容版本。在本项目目录中执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

虚拟环境只需创建一次。以后重新打开终端时，在项目目录执行 `source .venv/bin/activate` 即可重新激活。

## 运行方法

从 `careerlens/` 项目目录执行：

```bash
PYTHONPATH=src python -m careerlens.cli data/raw/sample_jd.txt data/processed/sample_jd.txt
```

参数顺序为：

```text
python -m careerlens.cli <输入路径> <输出路径>
```

查看生成结果：

```bash
cat data/processed/sample_jd.txt
```

程序不会修改 `data/raw/sample_jd.txt`。如果输出目录不存在，CLI 会在写入前创建它。

## 测试方法

激活虚拟环境后，从项目目录执行：

```bash
PYTHONPATH=src python -m pytest -v
```

当前测试覆盖 8 种行为，预期结果为 `8 passed`。

## 当前支持的清洗规则

- 合并每行内部的连续空白。
- 将 Tab 等行内空白规范为单个空格。
- 删除每行首尾空白。
- 删除空行和纯空白行。
- 保留非空行的原始顺序。
- 保留中文、英文、数字、编号和标点内容。
- 对同一文本重复清洗时保持结果稳定。

## 当前限制

- 不使用 LLM 理解文本，也不提取学历、薪资或技能等结构化字段。
- 不使用数据库，结果只保存在本地文本文件中。
- 不包含 RAG、知识库或向量检索。
- 不包含 Agent、工具调用或自主工作流。
- 不提供 Web 页面或 HTTP API。

这些能力属于后续学习阶段，不是 Week 1 版本的缺陷。

## 数据与隐私

仓库中的 `data/raw/sample_jd.txt` 只使用虚构、脱敏的练习信息。不要把真实姓名、电话、邮箱、公司内部信息、未公开招聘内容或可识别个人经历提交到 Git。

## 学习记录

Week 1 的每日学习内容、真实错误和关键认识保存在 [Week 1 学习记录](../docs/learning/week-01-learning-record.md)。
