# CareerLens Week 2 学习记录

> 本文档由导师根据每天的真实对话、代码、命令、错误和验收结果维护。每日计划回答“准备学什么”，本文档记录“实际学到了什么”。

## Week 2 / Day 1

今天学习了使用字典、列表和嵌套结构表达一份岗位记录，并完成 `practice/week2/day1_job_record.py`。程序保存岗位名称、地点、任职要求、技能和职责，能够读取嵌套字段、修改技能列表、判断成员、统计职责数量、安全读取可选薪资，并遍历任职要求。

### 数据结构职责

- 字典适合表示包含多个命名字段的对象，例如岗位、地点和任职要求。
- 列表适合表示多项同类、有顺序的内容，例如技能和职责。
- 嵌套字典使用连续 `[]` 读取确定存在的字段，例如 `job["location"]["city"]`。
- `job.get("salary", "未提供")` 在可选字段不存在时返回默认值；`job["salary"]` 会产生 `KeyError`。
- 对字典使用 `in` 检查键，对列表使用 `in` 检查元素。
- `.items()` 在每轮循环中同时提供一个键和对应值。

### 修改与对象关系

```python
skills = job["requirements"]["skills"]
skills.append("pytest")
```

`skills` 是嵌套技能列表的另一个引用，不是自动复制的新列表。因此通过 `skills.append()` 修改后，原岗位字典中的技能列表也同步变化。

### 今天修正的认识

- 类型标注不会自动转换返回值。函数即使标注 `-> str`，实际 `return ["Python"]` 的类型仍是列表。
- Terminal 是显示与输入的终端窗口，Shell（当前为 Bash）解释命令，CLI 程序由 Shell 启动并接收文字参数，Python REPL 则显示 `>>>` 并只接受 Python 语句。
- 初版嵌套字典写在一行，随后按层级改成多行结构，使字段归属和括号更容易检查。
- `print()` 使用逗号输出多个参数时默认插入空格；`sep=""` 可把分隔符改为空字符串，使 `岗位：` 与字段值紧密连接。
- 变量 `skills`、`has_python`、`responsibility_count` 和 `salary` 分别体现数据类型、判断结果、统计含义和可选字段职责。

### 验收结果

最终程序正确输出岗位、城市、第一条职责、职责数量、追加后的技能、Python 成员判断和默认薪资，并正确遍历 `requirements`。学习者能够解释相关表达式的类型、`[]` 与 `.get()` 的区别、列表引用修改、`.items()` 和 `sep` 的作用。

## Week 2 / Day 2

今天学习了 Python 对象、JSON 文本和 JSON 文件的区别，并完成 `practice/week2/day2_json_roundtrip.py`。程序把包含中文、列表、布尔值和空值的岗位字典转换为 JSON 字符串，再还原为字典；随后写入 UTF-8 JSON 文件并重新读取。字符串往返与文件往返比较都为 `True`。

### JSON 类型与语法映射

- Python `dict` 对应 JSON object，`list` 对应 array，字符串和数字也有对应类型。
- Python 的 `False` / `None` 序列化后是 JSON 的 `false` / `null`。
- Python 字典显示形式不等于合法 JSON：Python 可以使用单引号、`False` 和 `None`，JSON 字段名与字符串必须使用双引号，并使用小写 `false` 和 `null`。
- `json.loads()` 读取非法 JSON 时产生 `json.decoder.JSONDecodeError`，错误信息会给出行、列和字符位置。

### 四个核心函数

```text
Python 对象 → dumps → JSON 字符串 → loads → Python 对象
Python 对象 → dump  → JSON 文件   → load  → Python 对象
```

- `dumps()` / `loads()` 中的 `s` 可记作 string，二者直接处理 JSON 字符串。
- `dump()` 接收 Python 对象和可写文件对象，把 JSON 写入文件，返回值通常是 `None`。
- `load()` 接收可读文件对象，返回解析后的 Python 对象。
- `roundtrip` 是“往返转换”：转换出去后再转换回来，并检查内容是否一致。
- `loaded_job` 表示“已经从外部数据加载回来的岗位对象”，名称反映了处理状态。

### 中文、排版与文件

- `ensure_ascii=False` 让中文直接保存在 JSON 中，而不是显示为 `\uXXXX` 转义。
- `indent=2` 使用两个空格缩进，只影响可读排版，不增加字段或改变数据。
- `encoding="utf-8"` 用于正确读写中文文本文件。
- `json.tool` 会解析后按工具自身默认设置重新输出，因此它显示 Unicode 转义不代表磁盘原文件保存的是转义内容；直接检查确认 `day2_job.json` 为 UTF-8 且包含中文原文。
- `data/processed/day2_job.json` 是可以由代码和输入数据重新生成的结果，因此继续由 Git 忽略。

### 命名学习规则补充

学习者提出：第一次出现新的英文函数、变量、文件或目录名时，应附中文直译、程序语境中的实际含义和命名理由。该规则已加入长期协作方法。`dump` 在程序中常译为“转储”，`load` 是“加载”，`day2_json_roundtrip.py` 表示 Day 2 的 JSON 往返转换练习。

### 验收结果

程序输出 `str` 与 `dict` 类型，字符串往返和文件往返均为 `True`；生成 JSON 通过 `python3 -m json.tool` 解析。学习者能解释四个函数的数据流、中文与缩进参数、Python/JSON 布尔与空值映射、非法 JSON 错误及文件命名。

## Week 2 / Day 3

今天学习了类型标注、类、实例和 `dataclass`，并在生产源码中创建 `src/careerlens/models.py`，定义 CareerLens 的第一种岗位数据模型 `JobPosting`。随后完成 `practice/week2/day3_model_demo.py`，创建模型实例、比较相等性、使用 `asdict()` 转为字典并生成可读中文 JSON。

### 类型标注与运行时边界

- `list[str]` 表示字符串列表。
- `str | None` 表示值可以是字符串或 `None`，但如果字段没有默认值，创建实例时仍必须明确传入参数。
- 类型标注不会自动转换或验证实际值；Python 默认仍可能让 `name=123` 进入标注为 `str` 的字段。
- 标注主要帮助程序员阅读、编辑器提示和静态类型检查工具，不能替代 Day 5 将学习的数据验证。

### 类、实例与数据类自动方法

- 类是创建同类对象的结构说明，实例是根据类创建的一条具体数据。
- `JobPosting` 是类，`job_posting` 是实例。
- `@dataclass` 根据字段自动生成常用行为：`JobPosting(...)` 触发 `__init__()` 接收并保存字段；打印实例使用可读的 `__repr__()`；`==` 使用 `__eq__()` 按字段比较。
- 两个字段相同的实例可以满足 `== True`，但 `is False`，说明内容相同不代表是内存中的同一个对象。
- `Course.__annotations__` 保存声明的字段类型，而 `type(wrong_course.name)` 显示运行时实际类型，两者可能不一致。

学习者指出：只列自动方法名称不足以帮助初学者理解，必须对应到示例中哪行代码触发以及产生什么结果。这条规则已加入长期协作方法。

### 模型与 JSON 衔接

`json.dumps(job_posting)` 会产生 `TypeError: Object of type JobPosting is not JSON serializable`，因为 JSON 模块默认只处理字典、列表、字符串、数字、布尔和空值等基础类型。正确数据流是：

```text
JobPosting 实例
→ asdict()
→ Python dict
→ json.dumps() / json.dump()
→ JSON 文本或文件
```

`asdict` 是 as dictionary，表示“转换成字典”。`day3_model_demo.py` 是 Day 3 数据模型演示文件。

### 模块职责

- `models.py` 是数据模型模块，只定义稳定字段结构，不读文件、不解析文本、不输出 JSON。
- Day 4 的 `parser.py` 将是解析器模块，计划把清洗文本按确定规则转换为 `JobPosting` 实例；Day 3 验收时学习者明确表示尚不知道 parser，当前只完成名称与预定数据流的初步说明，具体行为需要在 Day 4 重新从示例讲解。
- `json.dumps()` / `json.dump()` 负责把基础 Python 对象序列化为 JSON 字符串或文件。

### 学习过程改进

学习者的 Python REPL 状态在隔天后丢失，因此提出实验必须给出完整可重建上下文。长期协作方法已增加规则：REPL 实验应提供启动命令、导入、定义、实验语句和结束缩进块所需的空行，不默认旧变量仍存在。

### 验收结果

`JobPosting` 能正确初始化、显示、读取字段和按字段比较；`asdict()` 返回字典，JSON 中正确显示中文、`false` 和 `null`。新增模型后运行 Week 1 回归测试，结果仍为 `8 passed`。学习者能够解释类型语法、类与实例、三个自动方法、类型标注边界，以及模型到 JSON 的数据流；`parser.py` 的具体职责仍需在 Day 4 学习。

## Week 2 / Day 4

今天从输入、规则和输出重新学习了 parser/解析器，并创建 `src/careerlens/parser.py`。核心函数 `parse_job_posting(text: str) -> JobPosting` 接收已经清洗的文本，逐行识别固定格式字段，最终返回 `JobPosting` 实例。`JobPosting` 同时补充了 `responsibilities: list[str]`，使数据模型与周目标和真实样本保持一致。

### 清洗与解析的区别

- `cleaner.py` 只规范空白和删除空行，不理解字段含义。
- `parser.py` 根据明确前缀、章节和编号规则，把清洗文本转换成结构化字段。
- `models.py` 定义 `JobPosting` 应包含哪些字段，不负责读取、解析或输出。
- `json.dumps()` / `json.dump()` 在模型先转为基础 Python 对象后，负责生成 JSON 字符串或文件。

完整数据流是：

```text
原始文本 → clean_jd() → 清洗文本 → parse_job_posting()
→ JobPosting → asdict() → JSON
```

### 字段识别方法

- `startswith(prefix)` 接收前缀字符串并返回 `bool`，用于判断当前行应进入哪条解析规则。
- `removeprefix(prefix)` 接收前缀字符串并返回去掉匹配前缀后的 `str`；原字符串不被修改。前缀不匹配时，返回内容不变的结果。
- 先判断再删除很重要：若每一行都直接用于覆盖字段，不匹配的行也会返回自身并覆盖此前正确结果。
- `strip()` 在严格清洗合同下常是冗余保护，但能确保提取出的字段值自身没有首尾空白；parser 不重复调用完整 `clean_jd()`。
- 技能文本使用无参数 `split()` 按空白拆成 `list[str]`。

### 跨行职责与状态变量

岗位名称、工作方式、薪资和技能的值都在标签同一行；岗位职责则跨越章节标题和多条后续行，因此需要 `in_responsibilities` 保存循环当前是否处于职责区段。

```text
初始                       False
遇到“岗位职责：”          True
读取编号职责               保持 True
遇到“技能要求：”          False
```

`remote` 保存岗位是否远程，是业务字段；`in_responsibilities` 保存解析流程状态，二者职责不同。

职责行采用当前限定格式 `1. 正文`：`line[0]` 仍是字符串字符而不是整数，`isdigit()` 只判断它是不是数字字符。`line.split(". ", 1)` 最多切分一次，返回列表；追加职责时必须取 `[1]` 的正文字符串。

### 真实错误与修复

1. 在 Git 仓库根目录使用 `PYTHONPATH=src` 时，Python 找不到实际位于 `careerlens/src` 的包，产生 `ModuleNotFoundError`。进入 Python 项目根目录后命令正确；相对路径会基于当前目录展开。
2. 初版写成 `from models import JobPosting`、`text.linesplit()` 和 `line.startwith()`，随后分别修正为包导入、`splitlines()` 和 `startswith()`。
3. 薪资赋值语句末尾误加冒号，导致整个模块出现 `SyntaxError`、无法导入；后续函数名和结果变量的 `NameError` 都是连锁错误。
4. 技能最初使用 `split(", ")`，但合同输入是空白分隔的 `Python Git SQL`，因此改为 `split()`。
5. 职责最初把 `split(". ", 1)` 的整个列表加入结果，得到嵌套列表；检查返回类型后改为取 `[1]`，最终保存职责正文字符串。
6. Day 4 演示标签曾误用中文分号 `；`，随后改为中文冒号 `：`。

### 导入路径认识

在 Python 项目根目录运行 `PYTHONPATH=src` 时，`src` 是模块搜索起点，`careerlens` 是包名，`parser` 是模块名，`parse_job_posting` 是函数名。`src` 不写进 import，因为它是源码布局目录，不是 Python 包。

### 当前能力边界

解析器目前只明确支持：

- `岗位名称：` 前缀行。
- `工作方式：` 前缀行，其中只有值恰好为“远程”时得到 `True`。
- `薪资：` 前缀行。
- 完全相等的 `岗位职责：` 章节标题。
- 职责区段中一位数字加英文句点和空格的编号行。
- `技能要求：` 前缀行和空白分隔技能。

岗位简介、加分项和其他未写规则的行会被分支自然跳过。字段标签、章节顺序、编号或技能分隔方式不同的任意 JD 可能无法正确解析。缺失工作方式时的 `False` 同时可能表示“明确非远程”或“根本没有识别到字段”，语义不足留到 Day 5 处理。

### 验收结果

固定格式演示正确得到标题、3 项技能、2 条职责、远程状态和薪资；真实脱敏样本正确得到标题、3 项技能和4 条职责，缺失工作方式与薪资分别暂得 `False` 和 `None`。Day 3 模型演示继续运行，Week 1 回归测试保持 `8 passed`。学习者能解释各模块职责、两个前缀方法、职责状态、编号切分、当前支持格式及限制。

## Week 2 / Day 5

今天为确定性解析器增加了字段合同、错误处理和自动化测试。`JobPosting.remote` 从 `bool` 改为 `bool | None`，解析器由此能够准确表达明确远程、明确线下和未提供工作方式三种状态。新增 `tests/test_parser.py`，最终包含 11 个解析器测试；与原有 8 个清洗测试一起运行，结果为 `19 passed`。

### 缺失、空值与不支持值

- 字段缺失表示整份输入中没有对应标签，例如没有 `岗位名称：`。
- 字段为空表示标签已识别，但标签后的内容为空，例如只有 `岗位名称：`。
- 不支持值表示字段和值都存在，但当前合同不知道如何解释，例如 `工作方式：混合办公`。
- 岗位名称、技能要求和岗位职责是必填字段；工作方式和薪资是可选字段。
- 工作方式为“远程”时保存 `True`，“线下”时保存 `False`，字段缺失时保存 `None`，其他值抛出包含实际内容的 `ValueError`。

### 状态变量与字段值

`saw_title`、`saw_skills` 和 `saw_responsibilities` 记录标签是否曾经出现，字段变量则保存解析后的内容。标题缺失和标题为空都会得到 `title == ""`，但前者的 `saw_title` 是 `False`，后者是 `True`，因此必须组合判断。

薪资没有增加原计划中的 `saw_salary`。学习者主动指出：`salary` 初始值 `None` 已经表示字段缺失，而识别到空薪资后结果是 `""`，直接使用 `salary == ""` 即可识别空值。若使用 `if not salary`，则会把 `None` 与空字符串混为一类。

### `raise` 与异常测试

- `raise ValueError(...)` 主动抛出值错误，抛出后当前函数不再继续执行。
- `ValueError` 适合输入文本已经取得、但字段内容不符合解析合同的情况。
- `FileNotFoundError` 适合准备读取的文件路径不存在的情况。
- `pytest.raises(ValueError, match="...")` 监视缩进代码，要求它抛出指定异常且错误信息匹配；若函数正常返回、异常类型不对或文本不匹配，测试都会失败。
- 期待异常的测试通过，表示非法输入被按照合同正确拒绝，并不表示程序发生意外故障。

### 真实错误与定位

1. 最小 `parse_level()` 实验确认 `raise` 会停止函数，并使用 `pytest.raises()` 捕获 `ValueError`。
2. 曾尝试把 `parser.py` 当作可执行脚本运行；进一步明确 `parser.py` 是供导入的功能模块，验证行为必须导入并调用 `parse_job_posting()`。`-m` 后使用点分模块名 `careerlens.parser`，不写 `.py`。
3. 测试文件最初用普通双引号书写多行文本，产生 `SyntaxError: unterminated string literal`，改为三引号字符串。
4. 列表预期被写成带外层引号的字符串形式，产生 `SyntaxError`；修正为真正的列表对象后继续测试。
5. 导入函数时把 `parse` 误写为 `psrse`，根据 `ImportError` 的文件、行号和名称提示修正。
6. 合法测试把实际薪资 `15k-20k` 错写为预期 `15K-20K`。解析器合同要求保留原文，因此修改测试预期，而不是错误地修改功能实现迎合测试。
7. 异常测试中的多行字符串为了排版加入前导空格，导致 `startswith()` 无法识别技能和职责标签。根据 pytest 的 expected/actual 消息定位后，删除字符串内容中的缩进；这也说明测试通过有时可能受验证顺序影响，每个用例应确保除目标错误外的字段均合法。

### 验收结果

11 个解析器测试覆盖完整合法输入、缺失可选字段、明确线下、不支持工作方式、必填字段缺失与为空以及空薪资。Day 3、Day 4 演示保持正常，真实脱敏样本缺少工作方式时得到 `None`，完整测试套件为 `19 passed`。学习者能够解释三类无效输入、远程三态、状态变量、`raise`、`pytest.raises()` 以及 `ValueError` 与 `FileNotFoundError` 的适用边界。

## Week 2 / Day 6

今天把 Week 1 文本清洗 CLI 与 Week 2 解析器、数据模型和 JSON 写入连接成完整流程。原有两路径命令继续输出清洗文本；新增显式 `--json` 模式，从脱敏 JD 生成包含五个固定字段的 UTF-8 JSON。项目内部 README 已更新实际功能、命令、字段合同、测试数量和当前限制。

### CLI 接口与参数

比较了三种接口方案：根据后缀自动切换、显式 `--json` 和子命令。最终选择 `--json`，因为它在保留 Week 1 行为的同时明确表达用户意图，不会因误写输出后缀而静默执行另一种功能，也不提前引入子命令解析复杂度。

```text
python -m careerlens.cli input.txt output.txt
→ 文本清洗模式

python -m careerlens.cli --json input.txt output.json
→ 结构化 JSON 模式
```

`--json` 对 `sys.argv` 来说只是普通 `str`，Python 不会自动理解其含义；CLI 必须使用 `sys.argv[1] == "--json"` 判断。新命令共有四个元素：模块文件路径、`--json`、输入路径和输出路径。

### 完整类型与模块数据流

```text
输入文件
→ raw_text: str
→ clean_jd()
→ cleaned_text: str
→ parse_job_posting()
→ job_posting: JobPosting
→ asdict()
→ job_dict: dict
→ json.dump()
→ JSON 文件，函数返回 None
```

`JobPosting` 是 JSON 模块不认识的自定义实例，因此必须先由 `asdict()` 转成基础字典。`ensure_ascii=False` 让中文直接写入文件，`indent=2` 控制可读缩进，文件以 `encoding="utf-8"` 打开以正确读写中文。

### 可选字段与稳定结构

原始样本没有工作方式和薪资，但解析器明确把两者保存为 `None`，`JobPosting` 固定包含这两个字段，`asdict()` 也不会自动删除它们，因此 JSON 中得到 `"remote": null` 和 `"salary": null`。这表示字段已属于稳定结构，但来源没有提供答案。

`null` 不表示“字段被识别但为空”。空薪资或空工作方式会触发解析错误，不生成 JSON；明确线下得到 `false`，明确远程得到 `true`，缺失才得到 `null`。

### 错误边界与输出安全

- 参数不合法时，CLI 不依赖异常，主动打印两种用法并返回 `1`。
- 输入文件不存在时，`open()` 产生 `FileNotFoundError`，CLI 捕获后打印文件错误并返回 `1`。
- 岗位字段不合法时，解析器抛出 `ValueError`，CLI 使用 `except ValueError as error` 捕获具体异常对象、显示原始原因并返回 `1`。
- `raise ValueError(...)` 不会把异常作为普通返回值交给 `job_posting`，而是立即中断解析并跳到匹配的 `except`。

CLI 先读取、清洗、解析并转成字典，全部成功后才创建输出目录并以 `"w"` 打开文件。这样新输入处理失败时不会清空已有的正确输出，也不会留下虚假的空文件。当前实现尚不是针对写入中途故障的完整原子写入；临时文件写完后再替换正式文件属于后续工程增强。

### 真实错误与修正

1. 最初把变量 `json_mode` 写成 `json.mode`。点号表示访问对象属性，而下划线才组成变量名；同时错误参数分支遗漏 `return 1`，会继续访问未赋值的路径变量，随后一并修正。
2. 进一步明确 `sys.argv[0]` 是运行模块对应的文件路径，不是被调用的 `main()` 函数；`--json` 也不是 JSON 类型，而是普通字符串。
3. 首次写 `json.dump()` 时把 `ensure_ascii=False` 误写为不存在的 `ascii=False`，根据参数的完整英文含义修正。
4. 讨论了导入顺序：Python 真正要求的是来源分组清楚，同一组内字母排序属于团队或工具约定，不是语法硬性要求。
5. `json.tool` 命令粘贴时一度显示为 `.jon`，核对文件系统确认实际只有 `.json`，随后用正确路径重新验证并得到退出码 `0`。
6. 多个 Python 文件存在行尾空格或缺少末尾换行；学习者在 VS Code 启用 `Files: Trim Trailing Whitespace` 与 `Files: Insert Final Newline` 后保存，复查全部通过。

### 端到端验证

- 文本清洗模式成功生成文本并返回 `0`。
- `--json` 模式成功生成中文 JSON 并返回 `0`。
- `json.tool` 验证语法成功，`json.load()` 还原后得到 `dict`、字符串、列表和 `NoneType`。
- 输入文件不存在与技能为空都返回 `1`，且预先确认不存在的输出文件在失败后仍不存在。
- 原始样本运行前后 SHA-256 均为 `174f0850303e5fcb8d0d48f3c6f3ba1324bc851684202769d5bd7c7b408ece1a`。
- 完整自动化测试保持 `19 passed`。
- `data/processed/`、`tmp/`、虚拟环境和缓存继续由 Git 忽略。

### 交付决定

本日没有引入 CLI 自动化测试，避免在核心整合目标之外同时加入 `monkeypatch`、`tmp_path` 和 `capsys` 等新 pytest 概念；两种成功路径和两种失败路径已完成手动验证。公开根 README、Week 2 Git 提交和推送按学习者“每周结束统一更新一次”的决定，延后到 Day 7 周总结执行。

## Week 2 / Day 7

今天在不查看生产模型、解析器、CLI 和旧 Week 2 练习的条件下，新建 `practice/week2/day7_structured_rebuild.py`，闭卷重建简化的 `JobSummary` 数据类、`parse_job_summary()` 固定规则解析器和 `job_summary_to_json()` JSON 字符串转换函数。

### 闭卷实现结果

简化模型包含 `title: str`、`skills: list[str]` 和 `remote: bool | None`。解析器能够识别岗位名称、空白分隔技能以及远程/线下/缺失三种工作方式状态，并能区分标题或技能字段缺失与为空；不支持的工作方式抛出包含实际值的 `ValueError`。JSON 函数使用 `asdict()` 和 `json.dumps()`，返回中文不转义、缩进为 2 的 `str`。

实际验证结果：

- 远程、线下和未提供工作方式分别得到 `True`、`False`、`None`。
- 技能正确得到 `['Python', 'Git']`，不是带标签的长字符串。
- JSON 字符串直接显示中文，线下转换为 `false`。
- 混合办公、标题缺失、标题为空、技能缺失和技能为空分别得到约定的五种 `ValueError`。

### 闭卷中的真实错误

1. 练习文件首次回复完成时并未实际创建或保存，通过全仓库文件搜索确认后重新创建。
2. 初版把 `JobSummary` 拼成 `JobSummery`，漏掉 `dataclass` 导入和 `@dataclass`，并把字段标注的冒号写成赋值等号。通过无关的 `Course` 示例重新区分装饰器、类型标注和赋值。
3. 创建 `JobSummary` 时参数之间遗漏逗号，创建实例后遗漏 `return`；使用 `py_compile` 区分语法可解析与业务正确。
4. 技能分支调用 `removeprefix().strip()` 后没有保存返回值，随后仍拆分原始行，第一次得到 `['技能要求：Python', 'Git']`。重新联系字符串不可变规则，增加 `skills_text` 保存新字符串后修正。
5. 把独立函数 `asdict(job_summary)` 错记成不存在的实例方法 `job_summary.asdict()`；进一步确认 `@dataclass` 自动生成的常用方法不包含 `asdict()`。

这些问题主要是从空白文件复现时的细小语法与 API 调用记忆，不影响对数据流和设计原因的解释。按学习者决定，不单独安排补强时段，在 Week 3 的正常学习与复现中继续检查；若同类问题重复出现再安排专项补强。

### 周验收认识

- 脱敏是移除隐私和敏感信息，文本清洗是规范空白与格式，两者目的不同。
- `dumps` / `loads` 处理 JSON 字符串，`dump` / `load` 处理文件；`json.dump()` 返回 `None`。
- `cleaner.py`、`models.py`、`parser.py` 和 `cli.py` 分别负责清洗、数据结构、字段解析和命令行流程整合。
- parser 返回 `JobPosting` 而不直接生成 JSON，使解析结果能被 JSON、数据库、API 等不同消费者复用。
- 确定性规则的优势是相同输入与规则得到可重复、可测试的行为，而不是保证实现永远没有错误。
- 固定标签、一位数字职责编号、空白技能分隔和有限工作方式限制了当前适用范围；未来 LLM 可处理更多表达变化，但仍需验证其不稳定结果。
- 能准确写出 `PYTHONPATH=src .venv/bin/python -m careerlens.cli --json data/raw/sample_jd.txt data/processed/sample_jd.json`。

公开根 README 按“每周更新一次”的约定在 Day 7 更新，当前显示 Week 2 的结构化解析、JSON 导出和 19 个测试，并继续明确项目尚不包含 LLM、数据库、RAG、Agent 或 Web API。

## Week 2 周总结

Week 2 完成了从清洗文本到结构化 JSON 的第一条完整数据链：

```text
原始脱敏 JD
→ clean_jd()
→ 清洗字符串
→ parse_job_posting()
→ JobPosting
→ asdict()
→ dict
→ json.dump()
→ UTF-8 JSON 文件
```

### 本周交付

- 嵌套字典与列表岗位练习。
- Python 对象、JSON 字符串和 JSON 文件往返练习。
- `JobPosting` 数据模型与模型演示。
- 固定格式 JD 解析器与字段验证。
- 11 个解析器测试，加上原有测试共 `19 passed`。
- 保留文本模式并新增 `--json` 的 CLI。
- 项目内部运行说明与每周公开根 README。
- 独立闭卷结构化解析重建练习。

### 当前能力评估

Week 2 停止条件通过：学习者能够解释并实际操作嵌套数据、四个 JSON 函数、简单数据类、固定规则解析、预期异常测试和 CLI JSON 输出；核心解析逻辑经过逐步提示后由学习者亲手实现，并在 Day 7 从空白文件闭卷重建简化版本，而不是整段复制导师答案。

当前更稳定的是类型流、模块职责、错误语义和验证思路；仍需在后续实践中自然巩固装饰器、类型标注符号、字符串返回值保存、独立函数与实例方法区别以及多行调用标点。Week 3 可继续推进，但应在新任务中保留短复现检查，不带着错误理解进入后续阶段。

### 后续边界

当前解析器只适合约定格式，不能代表通用 JD 理解。Week 3 计划应在下一次学习前共同制定，并根据本周复盘决定继续 Python 工程基础还是为 HTTP、FastAPI 和后端阶段做衔接；在明确计划前不自动引入 LLM、数据库或复杂框架。
