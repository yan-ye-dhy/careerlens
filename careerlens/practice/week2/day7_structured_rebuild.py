import json
from dataclasses import asdict, dataclass


@dataclass
class JobSummary:
    title: str
    skills: list[str]
    remote: bool | None


def parse_job_summary(text: str) -> JobSummary:
    title = ""
    saw_title = False
    skills = []
    saw_skills = False
    remote = None

    lines = text.splitlines()
    for line in lines:
        if line.startswith("岗位名称："):
            saw_title = True
            title = line.removeprefix("岗位名称：").strip()
        elif line.startswith("技能要求："):
            saw_skills = True
            skills_text = line.removeprefix("技能要求：").strip()
            skills = skills_text.split()
        elif line.startswith("工作方式："):
            work_mode = line.removeprefix("工作方式：").strip()
            if work_mode == "远程":
                remote = True
            elif work_mode == "线下":
                remote = False
            else:
                raise ValueError("不支持的工作方式：" + work_mode)

    if not saw_title:
        raise ValueError("缺少岗位名称")
    elif title == "":
        raise ValueError("岗位名称不能为空")
    if not saw_skills:
        raise ValueError("缺少技能要求")
    elif skills == []:
        raise ValueError("技能要求不能为空")

    job_summary = JobSummary(
        title=title,
        skills=skills,
        remote=remote,
    )
    return job_summary


def job_summary_to_json(job_summary: JobSummary) -> str:
    job_dict = asdict(job_summary)
    json_text = json.dumps(job_dict, ensure_ascii=False, indent=2)
    return json_text
