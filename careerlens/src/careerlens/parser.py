from careerlens.models import JobPosting


def parse_job_posting(text: str) -> JobPosting:
    title = ""
    saw_title = False
    skills = []
    saw_skills = False
    responsibilities = []
    in_responsibilities = False
    saw_responsibilities = False
    remote = None
    salary = None
    lines = text.splitlines()
    for line in lines:
        if line.startswith("岗位名称："):
            saw_title = True
            title = line.removeprefix("岗位名称：").strip()
        elif line.startswith("工作方式："):
            work_mode = line.removeprefix("工作方式：").strip()
            if work_mode == "远程":
                remote = True
            elif work_mode == "线下":
                remote = False
            else:
                raise ValueError("不支持的工作方式：" + work_mode)
        elif line.startswith("薪资："):
            salary = line.removeprefix("薪资：").strip()
        elif line == "岗位职责：":
            saw_responsibilities = True
            in_responsibilities = True
        elif line.startswith("技能要求："):
            saw_skills = True
            in_responsibilities = False
            skills_text = line.removeprefix("技能要求：").strip()
            skills = skills_text.split()
        elif (
            in_responsibilities
            and line != ""
            and line[0].isdigit()
            and line[1:3] == ". "
        ):
            responsibility = line.split(". ", 1)[1]
            responsibilities.append(responsibility)
    if not saw_title:
        raise ValueError("缺少岗位名称")
    elif title == "":
        raise ValueError("岗位名称不能为空")
    if not saw_skills:
        raise ValueError("缺少技能要求")
    elif skills == []:
        raise ValueError("技能要求不能为空")
    if not saw_responsibilities:
        raise ValueError("缺少岗位职责")
    elif responsibilities == []:
        raise ValueError("岗位职责不能为空")
    if salary == "":
        raise ValueError("薪资不能为空")
    job_posting = JobPosting(
        title=title,
        skills=skills,
        responsibilities=responsibilities,
        remote=remote,
        salary=salary,
    )
    return job_posting
