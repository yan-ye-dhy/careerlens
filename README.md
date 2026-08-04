# CareerLens

CareerLens 是一个以 AI/Agent 应用开发求职为目标的学习项目。项目通过逐周构建可运行功能，练习 Python、后端、RAG、Agent、测试、评测和工程交付。

当前完成 Week 1：本地 JD 文本清洗程序。

## 当前进度

- Python 核心语法、函数与常用容器
- 字符串清洗与模块拆分
- 命令行参数与文件读写
- 异常处理与退出码
- pytest 自动化测试
- Git 与项目文档

当前程序可以读取脱敏招聘 JD，规范化空白和空行，并将结果写入新文件。暂不包含 LLM 提取、数据库、RAG、Agent 或 Web API。

## 主要入口

- [CareerLens 项目与运行说明](careerlens/README.md)
- [学习总计划](docs/learning/careerlens-learning-master-plan.md)
- [Week 1 学习记录](docs/learning/week-01-learning-record.md)
- [学习与项目协作方法](docs/learning/careerlens-collaboration-method.md)
- [AI/Agent 求职学习路线设计](docs/superpowers/specs/2026-07-30-ai-agent-career-roadmap-design.md)

## 仓库结构

```text
careerlens/
├── README.md          # 项目安装、运行和测试说明
├── src/               # CareerLens 源码
├── tests/             # 自动化测试
├── data/              # 脱敏输入与本地生成结果
└── practice/          # Week 1 基础练习

docs/
├── learning/          # 学习计划、进度与记录
└── superpowers/       # 路线设计和详细实施计划
```

## 数据与隐私

仓库只应包含虚构或脱敏的练习数据。真实姓名、联系方式、公司内部信息、未公开材料和个人简历不得提交。
