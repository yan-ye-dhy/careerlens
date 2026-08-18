import json
from dataclasses import asdict

from careerlens.models import JobPosting


job_posting = JobPosting(
    title="AI 应用开发实习生",
    skills=["Python", "Git", "SQL"],
    responsibilities=[
        "编写文本处理功能",
        "为核心函数补充测试",
    ],
    remote=False,
    salary=None,
)


same_job_posting = JobPosting(
    title="AI 应用开发实习生",
    skills=["Python", "Git", "SQL"],
    responsibilities=[
        "编写文本处理功能",
        "为核心函数补充测试",
    ],
    remote=False,
    salary=None,
)


job_dict = asdict(job_posting)
json_text = json.dumps(job_dict, ensure_ascii=False, indent=2)

print("实例类型：", type(job_posting).__name__, sep="")
print("岗位名称：", job_dict["title"], sep="")
print("相同字段实例相等：", job_posting == same_job_posting, sep="")
print("asdict 结果类型：", type(job_dict).__name__, sep="")
print(json_text)
