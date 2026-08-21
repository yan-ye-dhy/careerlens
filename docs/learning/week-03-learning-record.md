# CareerLens Week 3 学习记录

> 本文档由导师根据每天真实发生的对话、代码、命令、错误、修复和验收结果维护。

## 当前状态

- Week 3 Day 1–Day 7 已完成。
- 本周 Python 工程衔接目标与周级验收均已完成，下一周开始 LLM 基础与结构化提取。
- 本周计划入口：[Week 3 学习计划](./week-03-plan.md)。

## Week 3 / Day 1

今天学习了简单列表与字典推导式、`sorted()` 与 `list.sort()`、排序 `key`、元组拆包和 `collections.Counter`，并新增 `src/careerlens/analysis.py` 与 `tests/test_analysis.py`。CareerLens 现在能从内存中的多个 `JobPosting` 统计技能被多少个岗位要求，并按“次数降序、名称升序”生成稳定排名。

### 推导式与排序基础

- 列表推导式由输出表达式、`for` 遍历来源和可选 `if` 筛选组成，会创建新列表，不自动修改原列表。
- 字典推导式使用 `key: value` 生成键值对；当天能够预测按次数筛选后的字典结果。
- `sorted(iterable)` 返回新的已排序列表，不修改输入；`list.sort()` 原地修改列表并返回 `None`，且只属于列表。
- 排名使用 `sorted()` 保留原始技能次数字典，减少不必要的副作用。
- Python 比较元组时先比较第一项，只有相同时才继续比较第二项；当前英文技能名在大小写统一时按默认字符串顺序排列。

### `key` 的准确理解

`skill_ranking_key()` 每次接收一个 `(技能名称, 次数)` 元组，返回 `(-次数, 技能名称)`：

```text
("Python", 3) → (-3, "Python")
("Git", 2)    → (-2, "Git")
("SQL", 2)    → (-2, "SQL")
```

`key` 的返回值只是临时比较依据，不会替换最终结果中的原始元素。负次数让默认升序产生次数降序；次数相同时继续使用技能名称升序，因此不依赖输入文件或首次出现顺序。

### 技能统计合同

当天共同确定：

- 统计值表示“多少个岗位要求该技能”，不是字符串总出现次数。
- 同一岗位内重复出现的技能先用 `set()` 去重，只贡献一次。
- 不同岗位分别贡献次数。
- 分析模块暂时区分 `Python` 与 `python`；技能别名与大小写规范化应由独立步骤负责，统计模块不静默改名。
- 公共计数结果返回 `dict[str, int]`，`Counter` 只作为函数内部工具。

### 新增模块与函数

`analysis.py` 是分析模块，只处理结构化岗位，不读取文件、不清洗或解析 JD、不写 JSON，也不处理命令行。

- `count_job_skills(job_postings: list[JobPosting]) -> dict[str, int]`：逐岗位去重并累计技能次数。
- `skill_ranking_key(skill_count: tuple[str, int]) -> tuple[int, str]`：生成次数降序、名称升序的排序依据。
- `rank_skills(skill_counts: dict[str, int]) -> list[tuple[str, int]]`：对字典键值对进行稳定且可预测的排名，不修改输入字典。

### 真实错误与定位

1. 初版使用 `Counter.update(unique_skills)`，通过类名调用，而真正应保存计数的是 `skill_counts = Counter()` 创建的实例。代码语法可编译但结果为空字典，说明 `py_compile` 只能证明语法可解析，不能证明业务逻辑正确。结合 Week 2 的类与实例概念后，改为实例调用。
2. 初版把包含全部键值对的 `skill_counts.items()` 命名为单数 `skill_count`，又提前调用 `skill_ranking_key(skill_count)`，产生 `ValueError: too many values to unpack (expected 2)`。
3. 进一步确认 `key=skill_ranking_key` 是把函数对象交给 `sorted()`；添加括号会在排序开始前立即调用函数。
4. 直接迭代字典只会得到键，因此排序输入应是 `skill_counts.items()`，其中每个元素才是 `(skill, count)` 元组。
5. 初版计数函数只标注 `-> dict`，随后补全为 `-> dict[str, int]`；`count_job` 改名为复数 `skill_counts`，使名称反映内容和类型。

### 测试与验收证据

当天测试覆盖：

- 同一岗位的重复技能只统计一次。
- 空岗位列表返回空字典。
- 次数降序且并列时名称升序。
- 空计数字典返回空列表。

新增 4 个测试全部通过，连同已有测试运行结果为：

```text
23 passed in 0.02s
```

测试编写属于当天已掌握语法的重复性工作，学习者提出不必耗时机械重写，导师提供了完整测试代码；学习者亲自保存、运行并确认四项合同。Day 5 学习参数化和临时目录时，再由学习者重点编写新的测试语法。

### 每日面试复习卡

#### 1. `sorted()` 与 `list.sort()` 有什么区别？

口述要点：`sorted()` 接收可迭代对象并返回新列表，不修改输入；`.sort()` 只属于列表，原地修改并返回 `None`。CareerLens 生成排名时保留原始次数字典，选择 `sorted()`。

项目证据：`rank_skills()` 对 `skill_counts.items()` 排序，验证后原字典内容不变。

掌握状态：已掌握。

#### 2. `Counter` 为什么适合技能统计？

口述要点：`Counter` 是 `dict` 的子类，专门累计元素次数；不存在的键读取为 `0`。本项目先对单个岗位技能使用 `set()` 去重，再用 `Counter.update()` 累加，使统计表示要求该技能的岗位数量。

项目证据：岗位 A 的 `['Python', 'Python', 'Git']` 对 `Python` 只贡献一次。

易错点：应由创建出的计数器实例调用 `update()`，不能用类名替代实例。

掌握状态：已掌握。

#### 3. 排序 `key` 函数负责什么？

口述要点：`sorted()` 把每个原始元素交给 `key` 函数，使用返回值比较位置，但最终返回原始元素。`(-count, skill)` 实现次数降序和名称升序。

项目证据：`skill_ranking_key(("SQL", 2))` 返回 `(-2, "SQL")`，最终列表仍保存 `("SQL", 2)`。

易错点：`key=skill_ranking_key` 传入函数对象；写括号会提前调用。

掌握状态：已掌握。

#### 旧题复习：JSON 与 `dataclass`

- `json.dumps()` 中的 `s` 表示 string，接收 Python 对象并返回 JSON 字符串；`json.dump()` 还接收可写文件对象，直接写入文件并通常返回 `None`。口述录入时曾把名称顺序打反，但此前已有正确代码、实验和解释证据，按打字颠倒记录，不判定为概念未掌握。
- `@dataclass` 为当前 `JobPosting` 自动生成 `__init__()`、`__repr__()` 和 `__eq__()`；类型标注用于说明、编辑器和静态检查，不会仅凭标注自动验证运行时值。

掌握状态：已掌握，JSON 函数名称在后续随机复习中再抽查一次。

### Day 1 验收结论

学习者能够解释并实际使用简单推导式、`sorted()`、排序 `key`、元组比较、`Counter`、岗位内去重和明确返回类型；能够通过 Traceback 区分类与实例调用、函数对象与函数调用，并完成正常、空输入、重复技能和并列排序验证。Day 1 停止条件通过，今天不进入目录遍历或批量文件读取。

## Week 3 / Day 2

今天学习了 `pathlib.Path`、路径状态查询、目录遍历、通配匹配、路径组成与 UTF-8 文本读取，并新增 `src/careerlens/batch.py`。CareerLens 现在能验证输入目录，发现直接子目录中的文本文件，按路径稳定排序，并返回路径与文本内容组成的有序列表。

### 字符串路径与 `Path`

- 字符串路径只是文本；`Path` 是提供路径拼接、状态查询和文件系统读写方法的对象。
- 创建 `Path("missing.txt")` 只表示一个路径，不会创建文件，也不能证明文件存在。
- 在当前 Linux 环境中，`Path` 创建出的具体类型显示为 `PosixPath`，函数签名仍使用通用的 `Path`。
- `/` 在 `Path` 语境中用于拼接路径，不是数值除法。
- `.name`、`.suffix`、`.parent` 分别表示末段名称、含点的后缀和直接父路径；`.resolve()` 可得到规范化绝对路径。
- 相对路径依据启动程序时的当前工作目录解释，因此同一相对字符串在不同工作目录可能指向不同位置。

### 目录发现与读取合同

当天共同确定：

- 只读取输入目录的直接子文件，不递归进入子目录。
- 使用 `child_path.is_file()` 排除目录，即使目录名称以 `.txt` 结尾。
- 使用 `child_path.suffix.lower() == ".txt"` 接受 `.txt`、`.TXT` 等大小写形式。
- 结果显式使用 `sorted()`，不依赖 `iterdir()` 提供的文件系统顺序。
- 空目录是合法输入，返回空列表。
- 输入路径不存在时抛出 `FileNotFoundError`；路径存在但不是目录时抛出 `NotADirectoryError`。
- `read_text(encoding="utf-8")` 读取完整文件并自动关闭，返回 `str`；明确编码避免依赖系统默认解码规则。
- 批量读取返回 `list[tuple[Path, str]]`，保留路径以便后续将处理结果或失败原因对应到具体文件。

`iterdir()` 返回目录全部直接子路径；`glob("*.txt")` 只按名称模式匹配直接子路径，但匹配结果仍可能是目录，因此名称匹配不能替代文件类型检查。

### 新增模块与函数

`batch.py` 当前只负责批量输入发现和读取，不清洗文本、不解析岗位、不统计技能，也不处理 CLI。

- `list_text_files(input_directory: Path) -> list[Path]`：验证目录，筛选直接子级文本文件并稳定排序。
- `read_text_files(input_directory: Path) -> list[tuple[Path, str]]`：复用前一个函数，按顺序读取 UTF-8 文本并保留来源路径。

变量命名从容易误解为文件对象的 `text_files` / `text_file`，调整为 `text_paths` / `child_path`；空结果列表补充完整类型标注，使名称和类型与实际内容一致。

### 真实错误与定位

1. 初版写成 `from pathlib import path`。代码可通过语法编译，但导入模块时产生 `ImportError: cannot import name 'path'`，并提示 `Did you mean: 'Path'?`。由此再次确认 `py_compile` 不验证导入名称是否真实存在，Python 名称区分大小写。
2. 异常消息使用字符串与 `Path` 直接相加，产生 `TypeError: can only concatenate str (not "PosixPath") to str`。检查两侧类型后使用 `str(input_directory)` 明确转换，并同时修复两个异常分支。
3. 手动验证确认不存在路径准确产生 `FileNotFoundError`，现有普通文件作为目录输入准确产生 `NotADirectoryError`。
4. 临时目录包含 `a.TXT`、`b.txt`、`notes.md`、名为 `folder.txt` 的目录和嵌套 `nested/c.txt`；结果只保留并排序为 `a.TXT`、`b.txt`。空目录返回 `[]`。
5. 口述验收中两次把输入目录的 `is_dir()` 说成“判断是否为文件”。实际源码、异常分支和运行结果均正确，因此按术语表达说反处理，不判定为实现能力缺失；但 `is_file()` 与 `is_dir()` 行为并不相同，后续面试抽查要求准确表述。

### 测试与验收证据

Day 2 没有提前创建 `test_batch.py`，文件系统自动化测试按计划留到 Day 5 学习 `tmp_path` 时完成。当天通过 Git 忽略的 `tmp/` 手动验证：

- 不存在路径。
- 普通文件冒充输入目录。
- 空目录。
- 小写和大写文本后缀。
- 非文本文件。
- 名称带 `.txt` 的目录。
- 嵌套目录中的文本文件。
- 路径与读取后字符串的对应关系。

已有全部自动化测试继续通过：

```text
23 passed in 0.02s
```

临时输入、虚拟环境、pytest 缓存和生成结果继续被 Git 忽略。

### 每日面试复习卡

#### 1. 字符串路径和 `Path` 有什么区别？

口述要点：字符串只保存路径文字；`Path` 是路径对象，提供拼接、名称拆分、状态查询、目录遍历和读写方法。创建对象不代表实际文件存在。

项目证据：`Path("data/raw/missing_directory")` 可以成功创建，但 `.exists()` 为 `False`。

掌握状态：已掌握。

#### 2. `iterdir()`、`glob()` 和 `is_file()` 分别负责什么？

口述要点：`iterdir()` 产生全部直接子路径；`glob()` 按名称模式产生匹配路径；二者返回的路径可能包含目录，`is_file()` 才验证普通文件。文件系统顺序没有合同保证，项目使用 `sorted()` 明确顺序。

项目证据：名为 `folder.txt` 的目录未进入结果，嵌套 `c.txt` 也因当前非递归合同被忽略。

掌握状态：已掌握。

#### 3. 为什么批量读取结果要保留 `Path`？

口述要点：只返回字符串会失去来源；保留 `(Path, str)` 能把后续成功结果或错误原因对应到具体文件。`read_text(encoding="utf-8")` 返回字符串并自动关闭文件。

项目证据：`read_text_files()` 返回有序的 `list[tuple[Path, str]]`。

掌握状态：已掌握。

#### 旧题复习：技能统计、排序和 JSON

- 同一岗位的技能先用 `set()` 去重，`Counter` 是字典子类，不存在键按 `0` 读取；普通字典访问不存在键会抛出 `KeyError`。
- `skill_ranking_key(("SQL", 2))` 返回 `(-2, "SQL")`，控制次数降序和并列名称升序。
- `json.dumps(job)` 返回 JSON 字符串；`json.dump(job, output_file)` 写入文件并通常返回 `None`。本次复习回答正确。

掌握状态：已掌握；目录验证时 `is_dir()` 的准确名称需要后续再抽查。

### Day 2 验收结论

学习者能使用 `Path` 查询文件系统、遍历直接子路径、筛选并稳定排序文本文件、读取 UTF-8 内容以及保留来源路径；能够根据 ImportError 和 TypeError 定位大小写导入与类型拼接问题，并实际验证缺失路径、非目录、空目录、混合文件和非递归边界。Day 2 停止条件通过，今天不进入逐文件清洗解析或失败隔离。

## Week 3 / Day 3

今天学习了循环中的 `try / except / else`、异常实例、多个异常类型、批次级与单文件异常边界，并在 `models.py` 中增加 `BatchResult`，在 `batch.py` 中增加 `process_job_files()`。CareerLens 现在能处理目录中的多份 JD：合法文件保存来源和 `JobPosting`，非法文件保存来源和具体失败原因，同时继续处理后续文件。

### `try / except / else` 执行路径

- `try` 只包围预期可能失败的操作。
- 如果没有异常，跳过 `except` 并执行 `else`。
- 如果出现匹配的异常，跳过 `try` 中剩余代码，执行对应 `except`，并跳过 `else`。
- 如果异常不匹配当前 `except`，`except` 和 `else` 都不执行，异常继续向外传播。
- 把成功结果写入 `else` 可以缩小受保护范围，避免把保存结果时出现的错误误判为输入转换错误。

最小实验将 `['10', 'bad', '20']` 转换为整数，最终得到 `[10, 20]` 和包含 `bad` 及具体 `ValueError` 消息的失败元组；中间失败没有阻止下一轮循环。

### 异常类、实例和字符串

`except ValueError as error` 中，`ValueError` 是要匹配的异常类，`error` 是本次捕获的具体异常实例。异常实例保存参数并实现字符串表示，因此：

- `type(error)` 显示实际异常类型。
- `error.args` 保存创建异常时收到的参数元组。
- `str(error)` 取得适合用户阅读和失败记录的消息。
- `repr(error)` 提供包含异常类型的开发者表示。

`except (OSError, ValueError) as error` 匹配两类中任意一种实际异常。`UnicodeError` 属于 `ValueError` 的子类范围，因此 UTF-8 解码错误也能由当前数据错误边界处理。没有使用宽泛的 `except Exception`，避免把 `TypeError`、`AttributeError` 或调用错误等程序缺陷伪装成普通坏 JD。

### 批次级与单文件异常边界

```text
list_text_files(input_directory)  # 循环和 try 之前
```

输入目录不存在或不是目录时，整个批次无法开始，异常直接向调用者传播。

进入文件循环后，每份文件独立执行：

```text
UTF-8 读取 → clean_jd() → parse_job_posting()
```

单文件 `OSError` 或 `ValueError` 被记录后，循环自然继续；其他未预期异常向外传播。这使批量处理既能保留尽可能多的合法结果，又不隐藏代码缺陷。

### 批量结果模型

新增：

```python
@dataclass
class BatchResult:
    jobs: dict[str, JobPosting]
    failures: dict[str, str]
```

- `jobs`：来源路径字符串到成功 `JobPosting` 的映射。
- `failures`：来源路径字符串到可读错误消息的映射。

`Path` 来自标准库但不是 JSON 支持的基础类型，也不是 `str` 子类；`asdict()` 不会自动把字典中的 `Path` 键改成字符串。因此在进入结果模型时显式使用 `str(text_path)`，为 Day 6 的 JSON 转换保留清楚合同。

### `process_job_files()`

函数签名：

```python
process_job_files(input_directory: Path) -> BatchResult
```

执行顺序：

1. 调用 `list_text_files()` 验证目录并取得稳定排序的路径。
2. 创建带完整类型标注的成功与失败字典。
3. 逐文件读取、清洗并解析。
4. 在 `except` 中保存 `str(error)`，在 `else` 中保存岗位实例。
5. 返回 `BatchResult(jobs=jobs, failures=failures)`。

`process_job_files()` 没有复用 `read_text_files()` 的一次性读取结果，因为读取本身必须位于每个文件各自的 `try` 内，才能隔离逐文件读取错误。多行数据类调用最终补齐尾随逗号，关键字参数使用 `jobs=jobs` 而不是普通赋值格式。

### 手动验证与证据

在 Git 忽略的 `tmp/day3_batch` 中准备：

```text
a_valid.txt    合法脱敏 JD
b_invalid.txt  空文本
c_valid.txt    合法脱敏 JD
```

实际结果：

```text
BatchResult 类型正确
jobs: a_valid.txt、c_valid.txt
failures: b_invalid.txt → 缺少岗位名称
成功数量: 2
失败数量: 1
```

位于非法文件之后的 `c_valid.txt` 仍成功，证明失败隔离生效。调用不存在目录时产生的 `FileNotFoundError` 直接向外传播，没有被转成空的批量结果；Traceback 显示错误发生于进入逐文件 `try` 之前。

Day 3 没有新增自动化文件测试，按计划留到 Day 5 使用 `tmp_path` 完成。现有全部自动化测试继续通过：

```text
23 passed in 0.02s
```

### 每日面试复习卡

#### 1. `try / except / else` 怎样执行？

口述要点：`try` 执行风险操作；匹配异常进入 `except`，未匹配异常继续传播；只有 `try` 完全没有异常才执行 `else`。成功结果放在 `else` 能缩小异常捕获范围。

项目证据：解析空的 `b_invalid.txt` 时执行 `except`，合法文件在 `else` 中进入 `jobs`。

掌握状态：已掌握。

#### 2. 为什么批量任务要区分两级错误？

口述要点：目录不可用意味着批次无法开始，应向外抛出；单文件格式错误不代表其他输入错误，应记录来源和原因后继续，以保留尽可能多的结果。

项目证据：两个合法文件与一个非法文件得到两个成功、一个失败；不存在目录仍抛出 `FileNotFoundError`。

掌握状态：已掌握。

#### 3. 为什么不直接捕获 `Exception`？

口述要点：宽泛捕获会把预期坏数据和程序缺陷混在一起，可能隐藏 `TypeError`、`AttributeError` 等真实错误。当前只处理文件系统错误与解析合同使用的值错误。

项目证据：`except (OSError, ValueError)` 明确表达可恢复的单文件失败范围。

掌握状态：已掌握，口述时需使用“程序缺陷”而不是笼统“其他输入错误”。

#### 旧题复习：路径、统计与排序

- `is_file()` 判断普通文件，`is_dir()` 判断目录；批量发现路径后显式排序以获得跨运行可预测的结果。
- 同一岗位技能先用 `set()` 去重，只贡献一次。
- `skill_ranking_key(("SQL", 2))` 返回 `(-2, "SQL")`，分别控制次数降序和并列名称升序。

掌握状态：已掌握。

### Day 3 验收结论

学习者能解释异常类与实例、`str(error)`、匹配与未匹配异常、`else` 条件以及明确捕获范围的理由；能区分批次无法开始与单文件可恢复失败，并亲手实现带来源的成功/失败结果模型和逐文件隔离流程。实际验证证明中间坏文件不会阻止后续文件，目录级异常仍正确传播。Day 3 停止条件通过，今天不进入函数参数化提取器、自动化文件测试或 CLI。

## Week 3 / Day 4

今天学习了函数对象、函数调用、`callable()`、函数作为参数、`Callable` 类型标注与默认参数，并把 `process_job_files()` 中写死的固定解析器改成可替换提取器。当前仍默认使用固定规则解析，Week 4 可以传入遵守相同合同的 LLM 提取函数，而批量读取、清洗、失败隔离和统计流程不必重写。

### 函数对象与函数调用

最小实验定义 `double(number)`，再执行 `operation = double`：

- `double` 是函数对象本身。
- `double(4)` 才是调用函数并取得整数结果。
- `operation = double` 不会执行函数，而是让两个变量指向同一个函数对象；`operation is double` 为 `True`。
- `callable(double)` 为 `True`；`callable(double(5))` 会先得到整数 `10`，再检查整数是否可调用，因此为 `False`。
- 把 `double(5)` 传给需要函数的参数，实际传入的是整数，而不是函数。

随后使用 `apply_operation(value, operation)` 验证：函数可以作为实参传入另一个函数，函数内部的 `operation(value)` 会调用该参数当前指向的函数。

### `Callable` 与提取器合同

使用现代标准库位置导入：

```python
from collections.abc import Callable
```

`Callable[[str], JobPosting]` 逐部分表示：

- `Callable`：一个可调用对象。
- `[str]`：调用时接收一个字符串参数。
- `JobPosting`：调用后返回一个岗位模型实例。

CareerLens 的提取器合同确定为：输入经过 `clean_jd()` 清洗的字符串；成功时返回 `JobPosting`；无法形成合法岗位时可以抛出 `ValueError`。类型标注帮助人、编辑器和类型检查工具理解合同，但 Python 运行时不会自动强制验证返回类型。

### 项目改动

`process_job_files()` 改为：

```python
def process_job_files(
    input_directory: Path,
    extractor: Callable[[str], JobPosting] = parse_job_posting,
) -> BatchResult:
```

循环内部由：

```python
job_posting = parse_job_posting(cleaned_text)
```

改为：

```python
job_posting = extractor(cleaned_text)
```

不传 `extractor` 时继续使用 `parse_job_posting`，已有调用方式不变；显式传入其他函数时，只替换“清洗文本到岗位对象”这一步。

### 三条实际验证路径

使用 `tmp/day3_batch` 的两个合法文件和一个空文件验证：

1. 传入始终返回固定岗位的 `fake_extractor`：得到 3 个成功、0 个失败，证明空文本不再受固定解析规则限制，提取步骤确实已经替换。
2. 传入对空文本抛出 `ValueError` 的 `selective_extractor`：得到 2 个成功、1 个失败；失败消息为“提取器收到空文本”，证明原有逐文件失败隔离继续生效。
3. 不传提取器：得到 2 个成功、1 个失败，空文件消息恢复为固定解析器的“缺少岗位名称”，证明默认行为保持不变。

### 真实错误与定位

在 REPL 定义 `selective_extractor()` 时，在 `raise` 后输入了完全空白行，交互解释器提前结束函数定义；后续缩进的 `return` 因此产生 `IndentationError: unexpected indent`。已经保存的错误版本只在空文本时抛出异常，非空文本隐式返回 `None`。

批量结果表面仍显示 2 个成功、1 个失败，但检查 `result.jobs` 后发现两个值均为 `None`，类型为 `NoneType`。这说明：

- 只检查成功和失败数量不足以证明返回内容正确。
- `-> JobPosting` 不会在运行时阻止 `None`。
- REPL 中完全空白行会结束当前复合语句输入；`.py` 文件内部普通空行不具有这一交互含义。

重新连续输入完整函数体后，两个成功值均恢复为 `careerlens.models.JobPosting`，标题均为“有效文本岗位”。

### 架构边界

Week 4 接入 LLM 后：

- 继续复用 `cleaner.py`、`models.py`、`batch.py`、`analysis.py`、失败记录和 JSON 转换。
- 新 LLM 提取器替换当前固定解析器在该路径中的位置。
- `parser.py` 不原样参与 LLM 提取路径，但保留为确定性基线或回退方案。
- `cli.py` 的主体流程可以复用，但需要扩展提取器选择和相应配置。

### 测试与验收证据

默认参数验证与两种替换提取器均得到符合合同的结果。已有全部自动化测试继续通过：

```text
23 passed in 0.02s
```

Day 4 没有提前编写批量自动化测试；今天使用真实临时目录完成接口实验，Day 5 再使用 `tmp_path` 和参数化测试把行为固化。

### 每日面试复习卡

#### 1. 函数对象和函数调用有什么区别？

口述要点：函数名本身表示可保存和传递的函数对象；加括号才会调用并得到返回值。给另一个变量赋函数名不会执行函数，而是让变量指向同一对象。

项目证据：`operation = double` 后 `operation is double` 为 `True`，`operation(4)` 与 `double(4)` 都返回 `8`。

掌握状态：已掌握。

#### 2. `Callable[[str], JobPosting]` 表示什么？

口述要点：参数应是可调用对象，调用时接收一个字符串并返回 `JobPosting`；这是类型合同提示，不是运行时自动验证。

项目证据：错误的 `selective_extractor()` 虽标注返回 `JobPosting`，仍能实际返回 `None`，必须检查结果内容或使用测试发现。

掌握状态：已掌握。

#### 3. 为什么把提取器作为参数？

口述要点：批量模块只依赖统一的输入输出合同，不必写死固定解析实现；默认参数保留旧行为，显式参数可以替换实现。

项目证据：同一批量函数分别使用固定解析器、假提取器和选择性提取器，读取、清洗和失败隔离代码均未改写。

掌握状态：已掌握。

#### 旧题复习：异常边界与架构复用

- 输入目录不存在意味着批次无法开始，应向外抛出；单文件 `ValueError` 不影响其他独立文件，应记录后继续。
- LLM 提取路径复用清洗、模型、批量处理、统计和 JSON；固定 `parser.py` 被新提取器替换，但保留为基线或回退。

掌握状态：已掌握；最初把 `parser.py` 列为 LLM 路径直接复用模块，经数据流对照后已准确修正。

### Day 4 验收结论

学习者能区分函数对象和调用结果，解释 `callable()`、函数参数、`Callable` 与默认参数；亲手完成可替换提取器接口，并用默认、成功替换和失败替换三条路径验证行为。能够根据 `IndentationError` 和结果中的 `NoneType` 定位 REPL 函数提前结束问题，并理解类型标注不会自动运行时校验。全部 23 个既有测试通过，Day 4 停止条件通过；今天未接入 LLM、未改 CLI、未增加抽象类或提前编写 Day 5 测试。

## Week 3 / Day 5

今天学习了 pytest fixture、`tmp_path`、参数化测试和异常断言，并新增 `tests/test_batch.py`，把 Day 2–Day 4 的目录筛选、内容读取、失败隔离和可替换提取器手工实验固化为 6 项自动化测试。全部回归测试由 23 项增加到 29 项。

### fixture 与 `tmp_path`

pytest 根据测试函数参数名称查找 fixture。测试函数写出 `tmp_path` 后，pytest 会为该次测试调用准备一个独立临时目录，并把对应的 `Path` 对象作为实参传入：

```python
def test_example(tmp_path: Path):
    ...
```

- 真正触发 fixture 查找的是名称 `tmp_path`。
- `: Path` 是帮助人和工具理解类型的标注，不负责选择 fixture。
- 改成未定义的 `temporary_directory: Path` 不会仅凭类型标注自动获得目录。
- 每个测试调用拥有独立目录；参数化展开后的每组调用也彼此隔离。
- 测试文件不会写入项目的 `data/` 或手工 `tmp/` 目录。

通过 `Path.write_text()` 在临时目录中创建 UTF-8 输入，通过 `read_text()`、`is_file()` 和项目批量函数检查结果。`write_text()` 创建的是普通文件，与名称是否带 `.txt` 无关；`mkdir()` 创建的是目录，即使名称为 `folder.txt` 也仍是目录。

### 参数化测试

使用：

```python
@pytest.mark.parametrize(
    ("path_kind", "expected_error"),
    [
        ("missing", FileNotFoundError),
        ("file", NotADirectoryError),
    ],
    ids=[
        "missing-path",
        "file-path",
    ],
)
```

- 第一部分定义每组数据对应的测试函数参数名。
- 第二部分提供两组实际参数，因此同一个测试函数形成两个独立测试调用。
- `ids` 只控制报告中的可读用例名称，不改变测试逻辑；报告实际显示 `[missing-path]` 与 `[file-path]`。
- `tmp_path` 没有出现在参数化名称中，由 pytest fixture 系统另外提供。

测试内根据 `path_kind` 准备不存在路径或普通文件路径，再将异常类交给 `pytest.raises()`。

### 异常断言

```python
with pytest.raises(expected_error):
    list_text_files(input_path)
```

虽然没有普通 `assert`，`pytest.raises()` 本身就是异常断言上下文：抛出预期类型则通过；没有异常会报告类似 `DID NOT RAISE`；抛出其他类型也会失败。参数化的两个用例分别验证 `FileNotFoundError` 与 `NotADirectoryError`。

### 新增批量测试

`tests/test_batch.py` 最终包含 5 个测试函数，其中一个参数化展开为两项，共 6 项：

1. `test_list_text_files_filters_and_sorts`：使用 `.txt`、`.TXT`、`.md` 和名为 `folder.txt` 的目录，验证普通文本文件筛选与稳定排序。
2. `test_list_text_files_rejects_invalid_input`：参数化验证缺失路径和普通文件路径的两类明确异常。
3. `test_process_job_files_isolates_failure_and_uses_extractor`：两个合法文件夹住一个空白文件，使用假提取器验证清洗文本、成功来源、`JobPosting` 类型和失败原因。
4. `test_read_text_files_returns_source_path_and_text`：验证返回 `(Path, str)`，并保留输入文本两侧空格，避免把清洗职责错误放到读取函数。
5. `test_read_text_files_empty_directory_returns_empty_list`：验证独立空临时目录返回空列表。

批量处理测试不仅检查 2 个成功和 1 个失败，还使用 `isinstance(..., JobPosting)` 防止 Day 4 曾出现的“数量正确但成功值为 `None`”问题。两个成功岗位标题断言为 `岗位 A` 和 `岗位 C`，证明假提取器收到的是 `clean_jd()` 处理后的字符串；中间空文件失败而后续文件成功，证明失败隔离。

### 字典遍历复习

```python
list(result.jobs)
```

默认遍历字典键，等价于 `list(result.jobs.keys())`，得到来源路径字符串列表；它是 Python 列表，不是链表。`values()` 得到岗位值，`items()` 得到 `(来源路径, JobPosting)` 键值对元组。

### 真实疑问与修正

1. 对 `ids` 的用途提出疑问后，直接从 `-v` 报告定位到 `[missing-path]` 和 `[file-path]`，确认它只是可读报告标识，不是执行条件。
2. 对没有普通 `assert` 仍通过提出疑问，明确 `pytest.raises()` 是异常断言，预期异常本身就是成功条件。
3. 最初把 `write_text()` 理解为可能“变成 txt”，通过无后缀的 `input` 文件和名为 `folder.txt` 的目录区分：文件系统类型由创建操作和实际状态决定，不由后缀决定。
4. 预测清洗结果时写成 `岗位A`、`岗位C`，重新沿 `split()` 与单空格 `join()` 数据流确认正确结果为 `岗位 A`、`岗位 C`。
5. 测试文件初次保存时标准库导入与第三方 `pytest` 之间缺少空行；按标准库、第三方、项目模块三组修正。`git diff --check` 不检查导入分组，因此仍需要人工审阅或格式工具。

### 测试与验收证据

批量测试单独运行：

```text
6 passed in 0.02s
```

全部回归测试：

```text
29 passed in 0.03s
```

测试覆盖分析、批量、清洗和解析四个模块，所有旧功能保持通过。

### 每日面试复习卡

#### 1. pytest fixture 与 `tmp_path` 是什么？

口述要点：fixture 是 pytest 在测试执行前提供的资源；pytest 按参数名识别内置 `tmp_path`，为每次测试调用注入独立临时目录的 `Path` 对象。类型标注不负责注入。

项目证据：6 项批量测试反复使用同名 `tmp_path`，空目录测试不会看见其他测试创建的文件。

掌握状态：已掌握；口述类型时由小写 `path` 修正为类名 `Path`。

#### 2. 参数化测试解决什么问题？

口述要点：一份测试逻辑配多组输入和预期，每组作为独立用例执行和报告；能减少重复，并准确定位失败数据。参数名与测试函数形参对应，`ids` 只改善报告名称。

项目证据：一个测试函数分别显示 `[missing-path]` 和 `[file-path]` 两项通过。

掌握状态：已掌握。

#### 3. `pytest.raises()` 为什么不需要普通 `assert`？

口述要点：它本身断言缩进代码必须抛出指定异常；未抛异常或类型不匹配均失败。

项目证据：同一参数化测试分别确认缺失路径和非目录路径的异常合同。

掌握状态：已掌握。

#### 旧题复习：类型标注与技能计数

- `-> JobPosting` 只表达预期合同，不进行运行时强制验证；批量测试用 `isinstance()` 检查真实成功值类型。
- 每个岗位先用 `set()` 对技能去重，再调用 `Counter.update()`，确保同一岗位的一项技能只贡献一次，符合岗位需求频率的业务含义。

掌握状态：已掌握。

### Day 5 验收结论

学习者能解释 pytest 按名称注入 fixture、`tmp_path` 的 `Path` 类型和逐用例隔离；能逐部分解释参数化的参数名称、数据组与执行次数，并从 `ids` 识别具体报告用例；能解释 `pytest.raises()` 的断言行为。亲手完成 6 项批量测试，覆盖筛选排序、缺失和非目录错误、原样读取、空目录、可替换提取器与单文件失败隔离，并补充值类型断言防止 `None` 混入。全部 29 项测试通过，Day 5 停止条件通过；今天未修改生产业务、CLI 或接入 LLM。

## Week 3 / Day 6

今天学习了 Python 标准库 `argparse`，用结构化参数规则替换 `cli.py` 中手工检查 `sys.argv` 数量和位置的分支；在保留文本清洗与单份 JSON 两种旧命令的基础上，新增 `--batch-json` 模式，将批量岗位、逐文件失败原因和技能统计写入 UTF-8 JSON 报告。

### 从手工 `sys.argv` 到 argparse

原 CLI 通过 `len(sys.argv)`、`sys.argv[1]` 等固定位置区分两种命令。增加第三种模式会继续扩大条件分支，因此改为：

```text
ArgumentParser()  创建并保存命令规则的解析器对象
add_argument()    登记位置参数或可选参数
parse_args()      读取并解析实际命令行
Namespace         用属性保存解析结果的对象
```

最初面对完整示例时，学习者把 `arguments.input_path` 回答为笼统的“输入路径”，把 `arguments.json` 误认为字符串 `--json`，并明确提出看不懂每个调用。随后将过程拆成“创建表单、登记字段、提交、取得结果”：

- `input_path` 和 `output_path` 不带横线，是按声明和传入顺序匹配的必填位置参数。
- `--json` 与 `--batch-json` 按选项名称匹配，不依赖固定位置。
- `action="store_true"` 让开关出现时属性为 `True`，未出现时默认为 `False`，不会保存选项字符串本身。
- argparse 去掉选项前导横线并把中间连字符改为下划线，因此 `--batch-json` 保存为 `arguments.batch_json`。
- REPL 自动显示的 `_StoreTrueAction(...)` 是 `add_argument()` 返回的内部规则对象，不是业务输出。

用显式列表分别解析无模式、`--json` 和 `--batch-json`，得到符合预测的三个 `Namespace`。互斥组产生：

```text
[--json | --batch-json]
```

同时传入两个模式时 argparse 明确提示冲突并抛出 `SystemExit(2)`。导师最初误称 REPL 会返回 Python 提示符；实际未捕获的 `SystemExit` 结束了解释器并回到 Shell，`echo $?` 为 `2`，已按真实证据修正。

### 参数解析函数

新增：

```python
create_argument_parser() -> argparse.ArgumentParser
```

该函数只声明程序说明、互斥模式、输入路径和输出路径，`main()` 继续负责业务流程。`--help` 自动显示模式与路径帮助并返回 `0`；缺少两个位置参数自动显示用法错误并返回 `2`。

第一步只替换参数解析后，旧文本清洗和单份 JSON 分别运行成功，证明重构没有同时改变业务结果，再继续接入批量功能。

### 批量报告组装

新增：

```python
create_batch_report(input_directory: Path) -> dict
```

数据流：

```text
process_job_files()
→ BatchResult
→ jobs.values()
→ list[JobPosting]
→ count_job_skills()
→ dict[str, int]
→ rank_skills()
→ list[tuple[str, int]]
→ 带 skill / count 字段的字典列表
```

`asdict(batch_result)` 创建包含 `jobs` 和 `failures` 的新字典，并递归把内部 `JobPosting` 转换为普通字典。随后：

```python
batch_report["skill_counts"] = skill_counts
batch_report["skill_ranking"] = skill_ranking
```

为报告增加统计和排名两项，不会向原 `BatchResult` 数据类动态添加字段。

学习者指出 `skill_ranking` 外层中括号代表列表。准确类型是字典组成的列表：Python `list` 转为 JSON 数组，每个 Python `dict` 转为 JSON 对象；不是“一个 JSON 字典”。将排名元组转换为 `{"skill": ..., "count": ...}` 是为了让两个值的含义自解释。

手动调用报告函数得到：

```text
顶层键：jobs、failures、skill_counts、skill_ranking
成功：2
失败：1
技能次数：Git / Python / SQL 均为 2
排名：Git、Python、SQL
```

成功岗位值类型为 `dict`，证明嵌套数据已可 JSON 序列化。对紧凑表达式 `next(iter(batch_report["jobs"].values()))` 提出疑问后，将其拆为取得值视图、建立迭代器、取第一个值三个步骤，并明确空集合时会抛出 `StopIteration`，这里只用于临时检查。

### 三模式 CLI

最终命令合同：

```bash
python -m careerlens.cli INPUT_FILE OUTPUT_FILE
python -m careerlens.cli --json INPUT_FILE OUTPUT_FILE
python -m careerlens.cli --batch-json INPUT_DIRECTORY OUTPUT_FILE
```

批量分支调用 `create_batch_report(Path(input_path))`；单文件分支继续读取并清洗，只有 `--json` 时执行固定解析。两个 JSON 分支共享 `json_data` 与 `json.dump()`，文本分支写入 `cleaned_text`。

批量 JSON 包含：

- `jobs`：来源路径到岗位字典。
- `failures`：来源路径到逐文件失败消息。
- `skill_counts`：每项技能出现于多少岗位。
- `skill_ranking`：次数降序、并列名称升序的带字段排名。

两个合法文件和一个空文件生成报告并返回 `0`；单文件失败已经记录，是批量命令的正常结果，不代表整个命令失败。不存在输入目录和普通文件冒充输入目录均显示明确消息、返回 `1`，且不创建输出报告。

### 输出文件错误处理

输出目录创建与文件写入最终放入 `try / except OSError`。把已有目录 `data/processed` 当成输出文件时，程序捕获 `IsADirectoryError`，显示：

```text
错误：输出文件无法写入：[Errno 21] Is a directory: 'data/processed'
```

退出码为 `1`，没有暴露完整 Traceback。只捕获文件系统错误；JSON 类型错误等程序缺陷继续暴露。

### 真实错误与定位

1. `json.dump()` 关键字误写为 `ndent=2`。它是语法上合法的关键字参数，因此 `py_compile` 不会确认其是否被目标函数接受；实际调用时才会失败。修正为 `indent=2`。
2. 添加输出 `try` 时，第 117 行 `try:` 只有 3 个前导空格，产生 `IndentationError: unindent does not match any outer indentation level`。通过带行号和不可见字符检查确认没有 Tab，而是少一个空格；调整为与 `except`、`return 0` 同级的 4 个空格。
3. `IndentationError` 属于代码解析/编译阶段的结构错误，模块尚未进入 `main()` 就失败，`py_compile` 能发现；这与语法合法但调用合同错误的 `ndent` 不同。
4. 使用 Shell 续行符验证 `json.tool` 时，在反斜杠后插入空行，终端显示 `>` 续行提示；补齐命令后两份 JSON 仍正确验证为退出码 `0`。

### 退出码合同与最终证据

```text
成功或正常显示 --help                 0
程序处理错误（输入、输出、解析）       1
argparse 用法错误                      2
```

最终回归：

```text
text_exit=0
single_json_exit=0
batch_json_exit=0
conflict_exit=2
single_valid_json=0
batch_valid_json=0
```

互斥命令没有创建输出文件；`git diff --check` 无错误；全部自动化测试继续通过：

```text
29 passed in 0.04s
```

### 每日面试复习卡

#### 1. argparse 怎样把命令行转换为程序可用的数据？

口述要点：`ArgumentParser` 保存规则，`add_argument()` 登记位置或可选参数，`parse_args()` 解析命令行并返回 `Namespace`；位置参数按顺序，可选参数按名称，`store_true` 把开关映射为布尔属性。

项目证据：`--batch-json` 映射为 `arguments.batch_json`，无开关时两个模式属性均为 `False`。

掌握状态：已掌握。

#### 2. 互斥参数与退出码有什么意义？

口述要点：互斥组把无效组合声明在参数规则中，由 argparse 自动拒绝；成功为 `0`，程序处理错误为 `1`，命令用法错误为 `2`。

项目证据：同时传入 `--json --batch-json` 显示明确冲突、返回 `2` 且不创建输出文件。

掌握状态：已掌握；初次把用法错误回答为 `1`，经实际输出修正为 `2`。

#### 3. `py_compile` 能检查什么、不能检查什么？

口述要点：它能检查代码能否解析和编译，例如缩进结构；不执行程序，也不验证目标函数是否接受某个语法合法的关键字参数。

项目证据：三空格 `try` 产生 `IndentationError`，而 `ndent=2` 能编译但会在 `json.dump()` 调用时失败。

掌握状态：已掌握。

#### 旧题复习：批量失败边界与 LLM 替换

- 单文件解析失败被记录后继续，批量报告成功生成返回 `0`；整个输入目录不可用时批次无法开始，返回 `1`。
- Week 4 直接复用清洗、模型、批量、分析、报告和 JSON；CLI 增加提取器选择；固定 `parser.py` 被 LLM 提取器替换，但保留为基线或回退。

掌握状态：已掌握；最初再次把 `parser.py` 列为 LLM 路径直接复用，经接口边界复核后准确修正。

### Day 6 验收结论

学习者从看不懂完整 argparse 示例开始，通过逐调用拆解掌握了解析器、位置参数、布尔开关、命名空间、属性映射和互斥组；亲手把 CLI 扩展为文本、单份 JSON、批量 JSON 三模式，并组装包含成功、失败、技能计数和稳定排名的报告。能够根据运行阶段区分 `ndent` 调用错误与缩进解析错误，补充受控输出文件错误处理。三模式、帮助、参数缺失、模式冲突、两类批次输入错误、输出错误和 JSON 有效性均已验证，全部 29 项测试通过。Day 6 停止条件通过；今天未接入 LLM、未更新 README、未提交 Git，也未提前开始 Day 7 周总结。

## Week 3 / Day 7

今天没有增加生产功能，而是在不查看或导入生产版 `batch.py` 与 `analysis.py` 的条件下，重新实现简化批处理流程，并完成 Week 3 架构口述、随机复习和周级回归验收。

### 闭卷复现成果

练习文件：

```text
practice/week3/day7_batch_rebuild.py
```

独立复现四项能力：

- `list_text_files_rebuild()`：验证输入目录，只保留直属普通 `.txt` 文件，后缀大小写不敏感并稳定排序。
- `process_job_files_rebuild()`：读取 UTF-8 文本，把函数对象作为提取器传入，逐文件保存成功岗位或失败消息。
- `count_job_skills_rebuild()`：同一岗位技能先去重，再累计岗位出现次数并返回普通字典。
- `rank_skills_rebuild()`：对字典键值对按次数降序、名称升序排序，不修改输入字典。

手动验证的混合目录包含普通文本文件、非文本文件和名为 `folder.txt` 的目录；结果只保留并排序正确的文本文件。不存在目录时准确产生 `FileNotFoundError`。

假提取器验证结果：

```text
成功：a_valid.txt、c_valid.TXT
失败：b_invalid.txt → 空文本
技能：Python 2、Git 1、SQL 1
排名：Python 2、Git 1、SQL 1
```

中间文件失败没有阻止后续文件成功，证明逐文件失败隔离生效。

### 真实错误与定位

1. 初次使用列表保存 `jobs` 和 `failures`，随后根据“来源路径必须映射岗位或错误消息”的访问需求修正为字典。
2. REPL 定义假提取器时，在函数体中间输入空行，导致函数提前结束；非空文本隐式返回 `None`。成功数量表面正确，但访问 `.skills` 时产生 `AttributeError`。重新连续输入完整函数，并检查结果值的实际类型后修复。
3. 技能计数初版返回 `Counter`；根据公开函数合同改为 `dict(skill_counts)`，让调用者得到明确的普通字典。
4. `Counter.update(unique_skills)` 会遍历集合中的每项技能并各加一次；这里先用 `set()` 去重，保证同一岗位的一项技能只贡献一次。
5. 排名键初版写成花括号，返回 `set`：`{'SQL', -2}`。改为圆括号后返回有顺序的元组 `(-2, 'SQL')`，才能表达第一排序条件和第二排序条件。
6. 直接迭代字典只能得到键；排名必须使用 `skill_counts.items()` 取得 `(skill, count)` 键值对。

### 架构口述结果

能够按类型说明完整生产数据流：

```text
CLI 参数
→ 输入 Path
→ list[Path]
→ 原始 str
→ 清洗后的 str
→ 可替换 extractor
→ JobPosting 或失败 str
→ BatchResult
→ 技能计数与排名
→ asdict() 生成普通字典
→ json.dump() 写入批量 JSON 报告
```

模块职责已能区分：

- `cleaner.py`：文本清洗。
- `parser.py`：固定格式基线/回退提取器。
- `models.py`：岗位与批量结果的数据模型。
- `batch.py`：目录发现、读取、提取调用和失败隔离。
- `analysis.py`：技能计数与稳定排名。
- `cli.py`：命令行解析、模式选择、报告组装和文件输出。

输入目录不可用时批次无法开始，应直接向外报错；单个 JD 失败时其他文件仍有处理价值，应记录失败后继续。`Callable[[str], JobPosting]` 让未来 LLM 提取器遵守相同输入输出合同，下游批量、统计和 JSON 流程无需重写。

### 周级验收证据

以下检查均通过：

```text
Day 7 练习文件 py_compile 成功
文本清洗 CLI 成功
单份 JSON CLI 成功且 JSON 语法有效
批量 JSON CLI 成功且 JSON 语法有效
29 passed
git diff --check 无错误
```

两份 README 已更新为 Week 3 实际状态，说明三种 CLI、批量失败隔离、技能统计、29 项测试和固定解析器的基线/回退定位。

### Day 7 验收结论

闭卷复现的四个函数通过约定样例；学习者能够从错误输出定位返回类型、容器类型、REPL 控制流和排序输入问题，并能口述完整架构、错误边界和 LLM 替换位置。Week 3 的功能、测试、文档与说明已一致，满足进入 Week 4 的学习条件。

## Week 3 总结

### 本周完成的项目能力

- 从指定目录稳定发现并读取多份 UTF-8 `.txt` JD。
- 使用 `BatchResult` 保存来源路径、成功岗位和失败原因。
- 隔离单文件错误，同时让批次级错误继续向调用者传播。
- 用函数参数建立可替换提取器接口，固定解析器保留为基线或回退。
- 按“包含该技能的岗位数量”计数，并产生稳定排名。
- 使用 `tmp_path`、参数化和异常断言覆盖真实文件流程。
- 使用 argparse 提供文本、单份 JSON、批量 JSON 三种互斥清楚的 CLI 模式。
- 自动化测试从 19 项增加到 29 项，已有清洗与解析功能保持通过。

### 本周筛选后的核心面试题

1. `sorted()` 与 `list.sort()` 有什么区别？——前者返回新列表且可接收任意可迭代对象；后者原地修改列表并返回 `None`。本项目用 `sorted()` 保留输入统计数据。
2. `Counter` 为什么适合技能统计？——它是用于计数的字典子类，不存在键按 `0` 读取；项目先按岗位去重再调用 `update()`。
3. 排序 `key` 函数怎样实现多条件排序？——每个元素映射为临时比较值；`(-count, skill)` 表示次数降序、名称升序，最终结果仍保存原始元组。
4. 字符串路径和 `Path` 有什么区别？——字符串只是文字，`Path` 提供拼接、状态查询、目录遍历和读写；创建 `Path` 不代表路径存在。
5. 为什么还要对后缀匹配结果调用 `is_file()`？——名称以 `.txt` 结尾的路径仍可能是目录，后缀不能代表文件系统类型。
6. `try / except / else` 怎样执行？——匹配异常进入 `except`；没有异常才进入 `else`；不匹配异常继续向外传播。
7. 为什么不直接捕获 `Exception`？——会把坏输入与 `TypeError`、`AttributeError` 等程序缺陷混在一起，隐藏真实错误。
8. 批量任务为什么区分批次级和单文件错误？——目录不可用意味着无法开始；单文件失败不应丢失其他独立文件的结果。
9. 函数对象和函数调用有什么区别？——函数名可以保存和传递；加括号才执行。`key=ranking_key` 和 `extractor=parse_job_posting` 都传入函数对象。
10. `Callable[[str], JobPosting]` 表示什么？——可调用对象接收一个字符串并返回岗位实例；它是类型合同提示，不自动做运行时校验。
11. pytest 的 `tmp_path` 与参数化分别解决什么问题？——前者为每次测试提供独立临时目录；后者让一份测试逻辑用多组数据分别执行和报告。
12. argparse 怎样区分位置参数和可选参数？——位置参数按顺序匹配；`--json` 等可选参数按名称匹配，`store_true` 将是否出现保存为布尔值。
13. `py_compile` 能检查什么？——能发现语法和缩进结构错误，但不执行代码，也不验证目标函数是否接受语法合法的关键字。
14. 固定解析器与未来 LLM 提取器是什么关系？——二者遵守相同的“清洗字符串到 `JobPosting`”合同；LLM 提取器提高格式适应性，固定解析器保留为可预测的基线或回退。
15. Python 对象如何进入批量 JSON？——`asdict()` 把数据类递归转换为基础容器，再由 `json.dump()` 写入文件；来源 `Path` 在模型入口处显式转为字符串。

### Week 3 最终结论

Week 3 已完成。学习者已经具备用 Python 组织批量输入、数据模型、可替换处理步骤、失败隔离、统计、测试和 CLI 的基础工程能力。固定规则解析仍有明确格式限制，但项目已经把“提取器”从下游流程中解耦；Week 4 可以开始大模型基础和第一次 LLM 结构化提取，而不需要推翻现有批量与报告架构。
