import json
from pathlib import Path


job = {
    "title": "AI 应用开发实习生",
    "skills": ["Python", "Git", "SQL"],
    "remote": False,
    "salary": None,
}


readable_json = json.dumps(job, ensure_ascii=False, indent=2)
restored_job = json.loads(readable_json)

print("JSON 文本类型：", type(readable_json), sep="")
print(readable_json)
print("loads 结果类型：", type(restored_job), sep="")
print("字符串往返一致：", restored_job == job, sep="")


output_path = Path("data/processed/day2_job.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as output_file:
    dump_result = json.dump(job, output_file, ensure_ascii=False, indent=2)
with open(output_path, "r", encoding="utf-8") as input_file:
    loaded_job = json.load(input_file)

print("dump 返回值：", dump_result, sep="")
print("load 结果类型：", type(loaded_job), sep="")
print("文件往返一致：", job == loaded_job, sep="")
