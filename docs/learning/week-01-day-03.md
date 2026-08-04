# CareerLens Week 1 Day 3 学习计划

> 本文档保存 Week 1 Day 3 的计划、进度与验收情况。当天完成后仍保留，到 Week 1 周复盘完成后再统一清理。

## 当前状态

- 周次：Week 1
- 学习日：Day 3
- 主题：函数与字符串清洗
- 状态：已完成
- 计划时长：约 3 小时

## 当日目标

完成后应当能够：

- 使用 `def` 定义函数，理解参数、函数体、调用和返回值。
- 区分 `print()` 输出与 `return` 返回值。
- 使用 `strip()`、`split()`、`splitlines()` 和 `join()` 处理字符串。
- 理解“一个函数只承担一个主要职责”。
- 自己设计并实现三个 JD 清洗函数。
- 验证 `clean_jd()` 的幂等性：同一结果再清洗一次不会继续变化。

## 当日目标接口

```python
def normalize_whitespace(text: str) -> str:
    """合并每行内部的连续空白，去除每行首尾空白，并保留换行结构。"""


def remove_empty_lines(text: str) -> str:
    """删除空行，保留非空行的内容和原始顺序。"""


def clean_jd(text: str) -> str:
    """按固定顺序组合本模块的清洗规则。"""
```

### 规则边界

- “每行内部的连续空白”包括普通空格、Tab 等，最终合并为一个普通空格。
- `normalize_whitespace()` 保留行边界，不把整份 JD 合并成一行。
- `remove_empty_lines()` 只删除空行，不负责合并非空行内的空白。
- `clean_jd()` 只组合清洗规则，不读写文件。

## 目标示例

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

## 阶段 1：函数基础诊断（约 15 分钟）

- [x] 预测简单函数的返回值与输出。
- [x] 根据诊断结果决定必学资料范围。

## 阶段 2：函数、参数与返回值（约 40 分钟）

主学习资料：

- [菜鸟教程：Python 3 函数](https://www.runoob.com/python3/python3-function.html)：只学习“定义一个函数”、参数、函数调用和 `return`，暂不学匿名函数、不定长参数和强制位置参数。

可选参考：

- [Python 官方教程：定义函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)

学习点：

- [x] `def`、函数名、圆括号、参数、冒号和缩进的作用。
- [x] 定义函数与调用函数的区别。
- [x] 形参与调用时传入值的关系。
- [x] `return` 将结果交回调用方，`print()` 只把内容显示到终端。

## 阶段 3：字符串清洗方法（约 35 分钟）

主学习资料：

- [菜鸟教程：Python 去除字符串中的空格](https://www.runoob.com/python3/python-remove-space.html)
- [菜鸟教程：`split()`](https://www.runoob.com/python3/python3-string-split.html)
- [菜鸟教程：`join()`](https://www.runoob.com/python3/python3-string-join.html)
- [菜鸟教程：`splitlines()`](https://www.runoob.com/python3/python3-string-splitlines.html)

学习点：

- [x] `strip()` 去除首尾空白，不删除中间空白。
- [x] 不传分隔符的 `split()` 会按连续空白分割并忽略首尾空白。
- [x] `splitlines()` 把多行字符串分成行列表。
- [x] `join()` 使用指定分隔符连接一组字符串。

## 阶段 4：函数合同与项目位置（约 25 分钟）

在创建项目文件前，共同确认：

- [x] 三个函数各自的输入、输出、示例和单一职责。
- [x] 为什么清洗代码放在 `src/careerlens/cleaner.py`。
- [x] 为什么需要 `src/careerlens/__init__.py`。
- [x] 为什么不在 `cleaner.py` 中读写文件。

候选结构：

```text
careerlens/
└── src/
    └── careerlens/
        ├── __init__.py
        └── cleaner.py
```

## 阶段 5：分步实现（约 50 分钟）

- [x] 先用注释或自然语言写下每个函数的输入、输出和示例。
- [x] 独立实现 `normalize_whitespace()`。
- [x] 独立实现 `remove_empty_lines()`。
- [x] 独立实现 `clean_jd()`。
- [x] 通过目标示例。
- [x] 验证空字符串与纯空白字符串不会产生异常。
- [x] 验证 `clean_jd(clean_jd(text)) == clean_jd(text)`。

## 阶段 6：Day 3 验收（约 15 分钟）

- [x] 能解释为什么文件读写不应写进 `clean_jd()`。
- [x] 能解释 `text: str` 和 `-> str` 的作用，以及它们不会自动强制运行时类型。
- [x] 能解释三个函数的各自职责和调用关系。
- [x] 在 `README.md` 的学习记录中增加 Day 3 总结。

## 当天完成后的保留规则

1. 把学习总计划中 Day 3 的状态改为“已完成”。
2. 将本文档的当前状态改为“已完成”，保留计划和勾选记录。
3. 开始 Day 4 时新建 `week-01-day-04.md`，不覆盖本文档。
4. Week 1 复盘完成并保存周总结后，再统一清理本周的每日计划文档。
