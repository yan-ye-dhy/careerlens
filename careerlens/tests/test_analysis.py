from careerlens.analysis import count_job_skills, rank_skills
from careerlens.models import JobPosting


def test_count_job_skills_counts_each_skill_once_per_job():
    job_postings = [
        JobPosting(
            title="岗位 A",
            skills=["Python", "Python", "Git"],
            responsibilities=[],
            remote=None,
            salary=None,
        ),
        JobPosting(
            title="岗位 B",
            skills=["Python", "SQL"],
            responsibilities=[],
            remote=None,
            salary=None,
        ),
        JobPosting(
            title="岗位 C",
            skills=["Git", "SQL"],
            responsibilities=[],
            remote=None,
            salary=None,
        ),
    ]

    actual = count_job_skills(job_postings)
    expected = {
        "Python": 2,
        "Git": 2,
        "SQL": 2,
    }

    assert actual == expected


def test_count_job_skills_empty_input_returns_empty_dict():
    actual = count_job_skills([])
    expected = {}

    assert actual == expected


def test_rank_skills_orders_by_count_then_name():
    skill_counts = {
        "RAG": 1,
        "SQL": 2,
        "Python": 3,
        "Git": 2,
    }

    actual = rank_skills(skill_counts)
    expected = [
        ("Python", 3),
        ("Git", 2),
        ("SQL", 2),
        ("RAG", 1),
    ]

    assert actual == expected


def test_rank_skills_empty_input_returns_empty_list():
    actual = rank_skills({})
    expected = []

    assert actual == expected
