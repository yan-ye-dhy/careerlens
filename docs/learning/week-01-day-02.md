# CareerLens Week 1 Day 2 学习计划

> 本文档保存 Week 1 Day 2 的计划、进度与验收情况。当天完成后仍保留，到 Week 1 周复盘完成后再统一清理。

## 当前状态

- 周次：Week 1
- 学习日：Day 2
- 主题：条件、循环、字典与集合
- 状态：已完成
- 计划时长：约 2.5 小时

## 当日目标

完成后应当能够：

- 使用 `if` 根据条件执行不同逻辑。
- 解释 `for skill in skills` 每次循环中变量的值。
- 使用列表保留有顺序的数据。
- 使用字典建立“技能名称 → 出现次数”的对应关系。
- 理解集合的去重能力及其不保证原始顺序的影响。
- 不使用第三方库，完成技能清理、去重、计数和最高频项统计。

## 今日目标数据

输入：

```python
skills = ["Python", "FastAPI", "Python", "RAG", "Git", "  SQL  "]
```

目标输出：

```text
cleaned: ['Python', 'FastAPI', 'RAG', 'Git', 'SQL']
counts: {'Python': 2, 'FastAPI': 1, 'RAG': 1, 'Git': 1, 'SQL': 1}
top: Python
```

## 阶段 1：现有基础诊断（约 10 分钟）

- [x] 不运行代码，预测简单 `if`、`for`、字典和集合表达式的结果。
- [x] 根据诊断结果决定哪些资料必学，避免重复学习已掌握内容。

## 阶段 2：条件与循环（约 35 分钟）

必学范围：

- [Python 官方教程：`if` 语句](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#if-statements)
- [Python 官方教程：`for` 语句](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#for-statements)
- [Python 官方教程：`range()`](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#the-range-function)

根据诊断结果选学：

- [黑马程序员 Python 零基础教程](https://www.bilibili.com/video/BV1qW4y1a7fU/)：在选集中查找“判断语句”、“for 循环”和“range”。

学习点：

- [x] `if` / `elif` / `else` 的执行顺序。
- [x] 缩进为什么会改变代码归属。
- [x] `for skill in skills` 中 `skill` 的变化过程。
- [x] `range()` 的起点、结束位置和步长。

## 阶段 3：字典、集合与循环技巧（约 40 分钟）

主学习资料：

- [菜鸟教程：Python 3 集合](https://www.runoob.com/python3/python3-set.html)：重点学习空集合、`add()`、`in` / `not in` 和集合去重。
- [菜鸟教程：Python 3 字典](https://www.runoob.com/python3/python3-dictionary.html)：重点学习创建字典、访问键、新增键值对和修改值。

可选参考，不要求当前通读：

- [Python 官方教程：集合](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#sets)
- [Python 官方教程：字典](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries)
- [Python 官方教程：循环的技巧](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#looping-techniques)

学习点：

- [x] 字典的键和值分别表示什么。
- [x] 如何读取、新增和更新字典中的计数。
- [x] 集合为什么能去重。
- [x] 为什么不应只把整个列表转成集合来完成“保留原始顺序”的去重。

## 阶段 4：小型交互式实验（约 25 分钟）

- [x] 在技能统计程序中亲手运行条件和循环，并观察首次出现与重复出现两类分支。
- [x] 亲手运行至少 3 个字典读写实验。
- [x] 亲手运行至少 2 个集合实验。
- [x] 记录至少一个与预测不同或曾经不确定的行为：`set("Python")` 会将字符串拆成字符，`{"Python"}` 才包含一个完整字符串。

## 阶段 5：技能统计程序（约 45 分钟）

在创建文件前，先讨论它为什么存在、是临时练习还是正式业务模块。

候选文件：

```text
careerlens/
└── day2_skill_stats.py
```

要求：

- [x] 去除每个技能名称首尾的多余空白。
- [x] 去除重复技能并保留原始出现顺序。
- [x] 统计清理后每项技能在原输入中出现的次数。
- [x] 找出出现次数最高的技能。
- [x] 得到与“今日目标数据”完全一致的三行输出。
- [x] 不使用第三方库。

## 阶段 6：Day 2 验收（约 15 分钟）

- [x] 分别说明本题中为什么选择 `list`、`dict` 和 `set`。
- [x] 能解释 `for skill in skills` 每次循环中 `skill` 的值。
- [x] 不使用第三方库完成练习。
- [x] 在 `README.md` 的学习记录中增加 Day 2 总结。

## 当天完成后的保留规则

1. 把学习总计划中 Day 2 的状态改为“已完成”。
2. 将本文档的当前状态改为“已完成”，保留计划和勾选记录。
3. 开始 Day 3 时新建 `week-01-day-03.md`，不覆盖本文档。
4. Week 1 复盘完成并保存周总结后，再统一清理本周的每日计划文档。
