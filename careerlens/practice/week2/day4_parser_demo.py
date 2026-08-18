from careerlens.cleaner import clean_jd
from careerlens.parser import parse_job_posting


raw_text = """  岗位名称：AI 应用开发实习生
工作方式：远程
薪资：15k-20k

岗位职责：
  1. 编写文本处理功能
2. 为核心函数补充测试

技能要求：Python   Git\tSQL  """


cleaned_text = clean_jd(raw_text)
parsed_job = parse_job_posting(cleaned_text)

print("岗位名称：", parsed_job.title, sep="")
print("技能：", parsed_job.skills, sep="")
print("岗位职责：", parsed_job.responsibilities, sep="")
print("是否远程：", parsed_job.remote, sep="")
print("薪资：", parsed_job.salary, sep="")
