job = {
    "title": "AI 应用开发实习生",
    "location": {
        "city": "杭州",
        "work_mode": "线下",
    },
    "requirements": {
        "education": "本科",
        "skills": ["Python", "Git", "SQL"],
    },
    "responsibilities": [
        "编写文本处理功能",
        "为核心函数补充测试",
    ],
}

skills = job["requirements"]["skills"]
skills.append("pytest")
has_python = "Python" in skills
responsibility_count = len(job["responsibilities"])
salary = job.get("salary", "未提供")

print("岗位：", job["title"], sep="")
print("城市：", job["location"]["city"], sep="")
print("第一条职责：", job["responsibilities"][0], sep="")
print("职责数量：", responsibility_count, sep="")
print("技能：", ", ".join(skills), sep="")
print("包含 Python：", has_python, sep="")
print("薪资：", salary, sep="")

for key, value in job["requirements"].items():
    print(key, value)
