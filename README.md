# CareerLens

CareerLens 是一个以 AI/Agent 应用开发求职为目标的学习项目。项目通过逐周构建可运行功能，练习 Python、后端、RAG、Agent、测试、评测和工程交付。

当前完成 Week 2：程序在保留 JD 文本清洗功能的基础上，可以按固定规则提取岗位字段并导出结构化 JSON。

## 当前进度

- Python 核心语法、函数与常用容器
- 嵌套字典、列表与岗位结构化数据
- JSON 字符串、文件与 UTF-8 往返转换
- 类型标注、`dataclass` 与岗位数据模型
- 字符串清洗与模块拆分
- 确定性字段解析与输入验证
- 命令行参数与文件读写
- 异常处理与退出码
- pytest 自动化测试（当前 19 个）
- Git 与项目文档

当前程序可以读取脱敏招聘 JD：默认模式规范化空白和空行并输出文本；`--json` 模式继续解析岗位名称、技能、职责、工作方式和薪资，输出 UTF-8 JSON。解析器只支持项目约定的固定格式，暂不包含 LLM 提取、数据库、RAG、Agent 或 Web API。

## 主要入口

- [CareerLens 项目与运行说明](careerlens/README.md)
- [学习总计划](docs/learning/careerlens-learning-master-plan.md)
- [Week 1 学习记录](docs/learning/week-01-learning-record.md)
- [Week 2 学习计划](docs/learning/week-02-plan.md)
- [Week 2 学习记录](docs/learning/week-02-learning-record.md)
- [学习与项目协作方法](docs/learning/careerlens-collaboration-method.md)
- [AI/Agent 求职学习路线设计](docs/superpowers/specs/2026-07-30-ai-agent-career-roadmap-design.md)

## 仓库结构

```text
careerlens/
├── README.md          # 项目安装、运行和测试说明
├── src/               # CareerLens 源码
├── tests/             # 自动化测试
├── data/              # 脱敏输入与本地生成结果
└── practice/          # Week 1 与 Week 2 独立练习

docs/
├── learning/          # 学习计划、进度与记录
└── superpowers/       # 路线设计和详细实施计划
```

## 数据与隐私

仓库只应包含虚构或脱敏的练习数据。真实姓名、联系方式、公司内部信息、未公开材料和个人简历不得提交。
