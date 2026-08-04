# CareerLens Week 1 Day 4 学习计划

> 本文档保存 Week 1 Day 4 的计划、进度与验收情况。当天完成后仍保留，到 Week 1 周复盘完成后再统一清理。

## 当前状态

- 周次：Week 1
- 学习日：Day 4
- 主题：文件、模块与异常
- 状态：已完成
- 计划时长：约 3 小时

## 当日目标

完成后应当能够：

- 理解 Python 模块、包和 `import` 的基本关系。
- 理解 `python3 -m careerlens.cli` 是按模块运行程序。
- 使用 `sys.argv` 获取输入路径和输出路径。
- 使用 `with open(..., encoding="utf-8")` 读写文本。
- 理解 `try`、`except`、具体异常类型和错误信息。
- 在输入文件不存在时，向普通用户显示清楚错误，不显示 traceback，并返回非零退出码。
- 从命令行读取一份脱敏 JD，调用 Day 3 的 `clean_jd()`，并将结果写入新文件。

## 当日目标数据流

```text
命令行参数
→ cli.py 获取输入/输出路径
→ UTF-8 读取 data/raw/sample_jd.txt
→ 调用 cleaner.py 的 clean_jd()
→ 创建输出目录
→ UTF-8 写入 data/processed/sample_jd.txt
```

`cleaner.py` 仍只处理字符串；`cli.py` 负责与用户、命令行和文件系统交互。

## 目标命令

从项目根目录 `careerlens/` 运行：

```bash
PYTHONPATH=src python3 -m careerlens.cli data/raw/sample_jd.txt data/processed/sample_jd.txt
```

当前没有安装 CareerLens 包，因此使用 `PYTHONPATH=src` 告诉 Python 从 `src/` 寻找 `careerlens` 包。

## 阶段 1：现有基础诊断（约 15 分钟）

- [x] 预测简单文件读写、导入和异常处理代码的行为。
- [x] 根据诊断结果决定哪些资料必学。

## 阶段 2：模块、包与命令行参数（约 35 分钟）

可选查阅资料：

- [菜鸟教程：Python 3 模块](https://www.runoob.com/python3/python3-module.html)：只学 `import`、模块搜索路径和 `__name__`，暂不深入高级导入。
- [菜鸟教程：Python `sys` 模块](https://www.runoob.com/python3/python-sys.html)：只学 `sys.argv`、`sys.path` 和退出状态。

学习点：

- [x] `from careerlens.cleaner import clean_jd` 各部分对应的包、模块和函数。
- [x] `sys.argv[0]` 是程序名，后续元素是用户提供的参数。
- [x] `PYTHONPATH=src` 为什么能让 Python 找到 `src/careerlens/`。
- [x] 退出码 `0` 表示成功，非零值表示失败。

## 阶段 3：文件读写与 UTF-8（约 35 分钟）

可选查阅资料：

- [菜鸟教程：Python 3 输入和输出](https://www.runoob.com/python3/python3-inputoutput.html)：只学“读写文件”部分，重点看 `open()` 参数、`r` / `w` 模式表与 `read()`。
- [菜鸟教程：Python 3 `open()` 函数](https://www.runoob.com/python3/python3-func-open.html)：查看文件模式完整表和 `encoding` 参数。
- [菜鸟教程：Python 3 File `read()`](https://www.runoob.com/python3/python3-file-read.html)：学习读取内容和返回值。
- [菜鸟教程：Python 3 File `write()`](https://www.runoob.com/python3/python3-file-write.html)：学习写入字符串、覆盖与返回的字符数。
- [菜鸟教程：Python `with` 关键字](https://www.runoob.com/python3/python3-with-keyword.html)：重点看“为什么需要 with 语句”。
- [Python 从入门到深入：文件操作](https://pythonhowto.readthedocs.io/zh_CN/latest/file.html)：只用于理解中文文本为什么应明确指定 UTF-8。

学习点：

- [x] `"r"` 与 `"w"` 模式的区别，以及 `"w"` 会覆盖已有文件。
- [x] `encoding="utf-8"` 对中文文本的作用。
- [x] `with` 代码块结束后文件会被正确关闭。
- [x] `read()` 返回字符串，`write()` 将字符串写入文本文件。

## 阶段 4：异常处理（约 30 分钟）

可选查阅资料：

- [菜鸟教程：Python 3 错误和异常](https://www.runoob.com/python3/python3-errors-execptions.html)：只学异常类型、`try` / `except`、`as error` 和 `FileNotFoundError`，暂不学自定义异常。

可选参考：

- [Python 官方教程：错误和异常](https://docs.python.org/zh-cn/3/tutorial/errors.html)

学习点：

- [x] `try` 放可能失败的操作，`except FileNotFoundError` 只处理输入文件不存在。
- [x] 为什么不应默认使用空的 `except:` 吞掉所有错误。
- [x] 开发者用 traceback 定位问题，普通 CLI 用户需要简短、可执行的错误信息。

## 阶段 5：项目结构与 CLI 合同（约 25 分钟）

创建文件前共同确认：

- [x] `src/careerlens/cli.py` 只负责参数、文件、错误处理和调用 `clean_jd()`。
- [x] `data/raw/sample_jd.txt` 是脱敏的练习输入，不包含个人隐私。
- [x] `data/processed/` 只保存程序生成的处理结果。
- [x] 为什么原始输入文件不应被原地覆盖。

候选结构：

```text
careerlens/
├── data/
│   └── raw/
│       └── sample_jd.txt
└── src/
    └── careerlens/
        ├── __init__.py
        ├── cleaner.py
        └── cli.py
```

`data/processed/` 由 CLI 在需要时创建，这能验证“输出目录不存在也能成功”的行为。

## 阶段 6：分步实现 CLI（约 50 分钟）

- [x] 由学习者创建 `cli.py`、`data/raw/`，并确认 AI 提案的脱敏 `sample_jd.txt`。
- [x] 先实验 `sys.argv` 中三个元素的含义。
- [x] 使用 UTF-8 和 `with open(...)` 读取输入文本。
- [x] 调用 `clean_jd()`，不在 `cli.py` 重复实现清洗规则。
- [x] 创建输出文件的父目录。
- [x] 使用 UTF-8 写入清洗结果。
- [x] 在输入文件不存在时显示清楚错误并返回非零退出码。
- [x] 在参数数量错误时显示用法并返回非零退出码。

## 阶段 7：Day 4 验收（约 10 分钟）

- [x] 正常输入能生成清洗文件。
- [x] 删除输出目录后，CLI 仍能重新创建它并成功写入。
- [x] 不存在的输入路径不会向普通用户显示 traceback。
- [x] 失败情况下 `echo $?` 显示非零退出码。
- [x] 对比运行前后的原始文件，确认它没有改变。
- [x] 用自己的话解释数据从输入路径到输出文件的完整过程。
- [x] 在 `README.md` 的学习记录中增加 Day 4 总结。

## 当天完成后的保留规则

1. 把学习总计划中 Day 4 的状态改为“已完成”。
2. 将本文档的当前状态改为“已完成”，保留计划和勾选记录。
3. 开始 Day 5 时新建 `week-01-day-05.md`，不覆盖本文档。
4. Week 1 复盘完成并保存周总结后，再统一清理本周的每日计划文档。
