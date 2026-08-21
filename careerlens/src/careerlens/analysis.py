from collections import Counter

from careerlens.models import JobPosting


def count_job_skills(job_postings: list[JobPosting]) -> dict[str, int]:
    skill_counts = Counter()
    for job_posting in job_postings:
        unique_skills = set(job_posting.skills)
        skill_counts.update(unique_skills)
    return dict(skill_counts)


def skill_ranking_key(skill_count: tuple[str, int]) -> tuple[int, str]:
    skill, count = skill_count
    return (-count, skill)


def rank_skills(skill_counts: dict[str, int]) -> list[tuple[str, int]]:
    skill_count_items = skill_counts.items()
    sorted_skill_counts = sorted(skill_count_items, key=skill_ranking_key)
    return sorted_skill_counts
