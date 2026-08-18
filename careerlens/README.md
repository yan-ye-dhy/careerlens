# CareerLens

CareerLens 当前是一个本地 Python 命令行程序。它可以读取 UTF-8 招聘 JD，清洗文本空白，也可以按本周约定的固定格式提取岗位字段并导出结构化 JSON。

这是 Week 1 与 Week 2 的工程成果，重点练习 Python 数据结构、模块、文件读写、异常处理、数据模型、JSON、自动化测试和 CLI 整合。

## 当前功能

- 从命令行接收输入文件路径和输出文件路径。
- 保留 Week 1 文本清洗模式，输出规范化后的文本文件。
- 使用 `--json` 显式选择 Week 2 结构化 JSON 模式。
- 使用 `JobPosting` 数据模型表示岗位名称、技能、职责、工作方式和薪资。
- 使用确定性解析规则提取固定格式字段。
- 区分必填字段缺失、字段为空和字段值不受支持。
- 使用 UTF-8 保存中文，并在需要时自动创建输出目录。
- 输入文件或岗位内容不合法时显示清楚错误并返回非零退出码。
- 通过 pytest 自动检查文本清洗与岗位解析规则。

## 数据处理流程

文本清洗模式：

```text
原始 JD 文本 → clean_jd() → 清洗文本文件
```

JSON 导出模式：

```text
原始 JD 文本
→ clean_jd()
→ parse_job_posting()
→ JobPosting
→ asdict()
→ Python dict
→ json.dump()
→ JSON 文件
```

## 项目结构

```text
careerlens/
├── data/
│   ├── raw/
│   │   └── sample_jd.txt       # 脱敏的原始练习输入
│   └── processed/              # 本地生成结果，由 Git 忽略
├── practice/
│   ├── week1/                  # Week 1 Python 基础练习
│   └── week2/                  # Week 2 数据、JSON 与模型练习
├── src/
│   └── careerlens/
│       ├── __init__.py         # Python 包标识
│       ├── cleaner.py          # 文本清洗
│       ├── models.py           # JobPosting 数据模型
│       ├── parser.py           # 固定格式岗位解析
│       └── cli.py              # 参数、文件、异常与程序入口
├── tests/
│   ├── test_cleaner.py         # 文本清洗测试
│   └── test_parser.py          # 岗位解析测试
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

以下命令都从 `careerlens/` 项目目录执行。

### 输出清洗文本

```bash
PYTHONPATH=src python -m careerlens.cli \
  data/raw/sample_jd.txt \
  data/processed/sample_jd.txt
```

查看结果：

```bash
cat data/processed/sample_jd.txt
```

### 输出结构化 JSON

```bash
PYTHONPATH=src python -m careerlens.cli \
  --json \
  data/raw/sample_jd.txt \
  data/processed/sample_jd.json
```

查看磁盘中的 UTF-8 内容：

```bash
cat data/processed/sample_jd.json
```

验证 JSON 语法：

```bash
python -m json.tool data/processed/sample_jd.json
```

成功时退出码为 `0`。用法错误、输入文件不存在或岗位内容不符合解析规则时，程序显示错误并返回 `1`。

程序不会修改 `data/raw/sample_jd.txt`。只有读取、清洗、解析和模型转换全部成功后，才会创建或覆盖输出文件。

## JSON 字段

JSON 固定包含五个字段：

```text
title               岗位名称，字符串
skills              技能列表，字符串数组
responsibilities    岗位职责，字符串数组
remote              是否远程，true / false / null
salary              薪资原文，字符串或 null
```

`remote` 的含义：

```text
“远程”       → true
“线下”       → false
字段未提供   → null
其他内容     → 解析失败
```

固定保留值为 `null` 的可选字段，可以让不同岗位文件保持一致的数据结构。

## 测试方法

激活虚拟环境后，从项目目录执行：

```bash
PYTHONPATH=src python -m pytest -v
```

当前共有 19 个测试：8 个文本清洗测试和 11 个岗位解析测试，预期结果为 `19 passed`。

## 当前支持的清洗规则

- 合并每行内部的连续空白。
- 将 Tab 等行内空白规范为单个空格。
- 删除每行首尾空白。
- 删除空行和纯空白行。
- 保留非空行的原始顺序。
- 保留中文、英文、数字、编号和标点内容。
- 对同一文本重复清洗时保持结果稳定。

## 当前支持的解析格式

解析器面向已清洗的固定练习格式，例如：

```text
岗位名称：AI 应用开发实习生
工作方式：远程
薪资：15k-20k
岗位职责：
1. 编写文本处理功能
2. 为核心函数补充测试
技能要求：Python Git SQL
```

当前规则：

- `岗位名称：`、`岗位职责：` 和 `技能要求：` 是必填字段，标签存在但内容为空也会失败。
- `工作方式：` 与 `薪资：` 可以缺失。
- 工作方式只支持“远程”和“线下”。
- 职责只识别一位数字、英文句点和空格开头的行，例如 `1. 正文`。
- 技能使用空格或 Tab 等空白分隔。
- 没有明确规则的其他行会被忽略。

## 当前限制

- 解析器只支持上文约定的固定格式，不理解任意网站或公司的招聘 JD。
- 不使用 LLM、Prompt 或语义推理补全缺失字段。
- 不使用数据库，结果只保存在本地文本或 JSON 文件中。
- 不包含 FastAPI、Web 页面、RAG、向量检索或 Agent 工作流。

这些能力属于后续学习阶段，不是当前版本的缺陷。

## 数据与隐私

仓库中的 `data/raw/sample_jd.txt` 只使用虚构、脱敏的练习信息。不要把真实姓名、电话、邮箱、公司内部信息、未公开招聘内容或可识别个人经历提交到 Git。

## 学习记录

- [Week 1 学习记录](../docs/learning/week-01-learning-record.md)
- [Week 2 学习记录](../docs/learning/week-02-learning-record.md)
