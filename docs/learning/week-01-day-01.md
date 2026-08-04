# CareerLens Week 1 Day 1 学习计划

> 本文档保存 Week 1 Day 1 的计划、进度与验收情况。当天完成后仍保留，到 Week 1 周复盘完成后再统一清理。

## 当前状态

- 周次：Week 1
- 学习日：Day 1
- 主题：Python 运行环境与基本表达式
- 状态：已完成
- 计划时长：约 2.5 小时

## 当日目标

完成后应当能够：

- 理解变量如何引用数据。
- 区分 `str`、`int`、`float`、`bool` 和 `list`。
- 对字符串和列表使用索引与切片。
- 使用常见字符串方法。
- 独立写出岗位摘要程序。
- 解释 `str` 与 `list` 在可变性上的区别。

## 阶段 1：环境确认

- [x] 在 VS Code 中确认当前窗口使用 WSL。
- [x] 运行 `pwd`，确认输出为 `/home/yanye/projects/careerlens-learning`。
- [x] 运行 `python3 --version`，确认 Python 可用。

## 阶段 2：数字、变量与基本类型（约 35 分钟）

必学：

- [Python 官方教程：把 Python 当作计算器](https://docs.python.org/zh-cn/3/tutorial/introduction.html#using-python-as-a-calculator)
- [Python 官方教程：编程的第一步](https://docs.python.org/zh-cn/3/tutorial/introduction.html#first-steps-towards-programming)

重点：

- [x] 数字运算和运算符。
- [x] 变量赋值。
- [x] `int`、`float`、`bool` 和 `str` 的基本区别。

辅助资料，只在文字资料难以理解时查看：

- [黑马程序员 Python 零基础教程](https://www.bilibili.com/video/BV1qW4y1a7fU/)：在选集中查找“字面量”“变量”“数据类型”和“运算符”。
- [北京理工大学嵩天 Python 课程](https://www.bilibili.com/video/BV1JL4y1x7xC/)：查看“Python 程序语法元素分析”相关部分。

## 阶段 3：字符串与列表（约 40 分钟）

必学：

- [Python 官方教程：文本](https://docs.python.org/zh-cn/3/tutorial/introduction.html#text)
- [Python 官方教程：列表](https://docs.python.org/zh-cn/3/tutorial/introduction.html#lists)

重点：

- [x] 下标从 `0` 开始。
- [x] 负数索引。
- [x] 切片的结束位置不包含在结果中。
- [x] 字符串不能通过索引修改单个字符。
- [x] 列表元素可以修改。

速查资料：

- [菜鸟教程：Python 3 字符串](https://www.runoob.com/python3/python3-string.html)
- [菜鸟教程：Python 3 列表](https://www.runoob.com/python3/python3-list.html)

## 阶段 4：交互式实验（约 30 分钟）

- [x] 使用 `python3` 进入交互式解释器。
- [x] 先预测结果，再亲手输入至少 20 条表达式。
- [x] 至少包含 4 条数字和变量表达式。
- [x] 至少包含 3 条布尔表达式。
- [x] 至少包含 5 条字符串表达式。
- [x] 至少包含 4 条索引或切片表达式。
- [x] 至少包含 4 条列表表达式。
- [x] 使用 `exit()` 退出解释器。

## 阶段 5：岗位摘要小程序（约 35 分钟）

在进入本阶段前，先讨论文件为什么存在、放在哪里，再由学习者创建。

候选文件：

```text
careerlens/
└── day1_job_summary.py
```

练习要求：

- [x] 保存岗位名称、城市、最低学历和技能列表。
- [x] 输出 `杭州 | AI Agent 实习生 | 本科 | Python, FastAPI`。
- [x] 分别使用索引、切片和字符串方法处理岗位名称。
- [x] 核心代码由学习者先尝试，AI 根据实际情况引导。

## 阶段 6：学习记录与验收（约 30 分钟）

- [x] 在新建 `README.md` 前理解它的当前职责。
- [x] 将当天不熟悉的语法记入 `README.md` 的“学习记录”。
- [x] 不看资料解释 `list` 与 `str` 的可变性差别。
- [x] 不借助 AI，从空文件写出岗位摘要程序。
- [x] 按原始 Week 1 计划完成 Day 1 验收。

## 当天完成后的保留规则

当且仅当所有 Day 1 验收项通过后：

1. 把学习总计划中 Day 1 的状态改为“已完成”。
2. 将本文档的当前状态改为“已完成”，保留计划和勾选记录。
3. 开始 Day 2 时新建 `week-01-day-02.md`，不覆盖本文档。
4. Week 1 复盘完成并保存周总结后，再统一清理本周的每日计划文档。
