import pytest

from careerlens.parser import parse_job_posting


VALID_TEXT = """岗位名称：AI 实习生
工作方式：远程
薪资：15k-20k
岗位职责：
1. 编写文本清洗功能
2. 补充自动化测试
技能要求：Python Git"""


def test_parse_valid_job_posting():
    result = parse_job_posting(VALID_TEXT)
    assert result.title == "AI 实习生"
    assert result.skills == ["Python", "Git"]
    assert result.responsibilities == ["编写文本清洗功能", "补充自动化测试"]
    assert result.remote is True
    assert result.salary == "15k-20k"


def test_parse_missing_title_raises_value_error():
    missing_title_text = """岗位职责：
1. 编写文本清洗功能
技能要求：Python"""

    with pytest.raises(ValueError, match="缺少岗位名称"):
        parse_job_posting(missing_title_text)


def test_parse_empty_title_raises_value_error():
    empty_title_text = """岗位名称：
岗位职责：
1. 编写文本清洗功能
技能要求：Python"""

    with pytest.raises(ValueError, match="岗位名称不能为空"):
        parse_job_posting(empty_title_text)


def test_parse_missing_skills_raises_value_error():
    missing_skills_text = """岗位名称：AI 实习生
岗位职责：
1. 编写文本清洗功能"""

    with pytest.raises(ValueError, match="缺少技能要求"):
        parse_job_posting(missing_skills_text)


def test_parse_empty_skills_raises_value_error():
    empty_skills_text = """岗位名称：AI 实习生
岗位职责：
1. 编写文本清洗功能
技能要求："""

    with pytest.raises(ValueError, match="技能要求不能为空"):
        parse_job_posting(empty_skills_text)


def test_parse_missing_responsibilities_raises_value_error():
    missing_responsibilities_text = """岗位名称：AI 实习生
技能要求：Python"""

    with pytest.raises(ValueError, match="缺少岗位职责"):
        parse_job_posting(missing_responsibilities_text)


def test_parse_empty_responsibilities_raises_value_error():
    empty_responsibilities_text = """岗位名称：AI 实习生
岗位职责：
技能要求：Python"""

    with pytest.raises(ValueError, match="岗位职责不能为空"):
        parse_job_posting(empty_responsibilities_text)


def test_parse_missing_optional_fields_returns_none():
    missing_optional_fields_text = """岗位名称：AI 实习生
岗位职责：
1. 编写文本清洗功能
技能要求：Python"""

    result = parse_job_posting(missing_optional_fields_text)
    assert result.remote is None
    assert result.salary is None


def test_parse_offline_work_mode_returns_false():
    offline_text = """岗位名称：AI 实习生
工作方式：线下
岗位职责：
1. 编写文本清洗功能
技能要求：Python"""

    result = parse_job_posting(offline_text)
    assert result.remote is False


def test_parse_unknown_work_mode_raises_value_error():
    unknown_work_mode_text = """岗位名称：AI 实习生
工作方式：混合办公
岗位职责：
1. 编写文本清洗功能
技能要求：Python"""

    with pytest.raises(ValueError, match="不支持的工作方式：混合办公"):
        parse_job_posting(unknown_work_mode_text)


def test_parse_empty_salary_raises_value_error():
    empty_salary_text = """岗位名称：AI 实习生
薪资：
岗位职责：
1. 编写文本清洗功能
技能要求：Python"""

    with pytest.raises(ValueError, match="薪资不能为空"):
        parse_job_posting(empty_salary_text)
