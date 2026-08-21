from collections import Counter
from collections.abc import Callable
from pathlib import Path

from careerlens.models import BatchResult, JobPosting


def list_text_files_rebuild(
    input_directory: Path,
) -> list[Path]:
    if not input_directory.exists():
        raise FileNotFoundError("路径不存在：" + str(input_directory))
    elif not input_directory.is_dir():
        raise NotADirectoryError("不是目录：" + str(input_directory))

    text_paths: list[Path] = []
    for child_path in input_directory.iterdir():
        if child_path.is_file() and child_path.suffix.lower() == ".txt":
            text_paths.append(child_path)

    return sorted(text_paths)


def process_job_files_rebuild(
    input_directory: Path,
    extractor: Callable[[str], JobPosting],
) -> BatchResult:
    text_paths = list_text_files_rebuild(input_directory)

    jobs: dict[str, JobPosting] = {}
    failures: dict[str, str] = {}

    for text_path in text_paths:
        try:
            source_path = str(text_path)
            raw_text = text_path.read_text(encoding="utf-8")
            job_posting = extractor(raw_text)
        except (OSError, ValueError) as error:
            failures[source_path] = str(error)
        else:
            jobs[source_path] = job_posting

    return BatchResult(
        jobs=jobs,
        failures=failures,
    )


def count_job_skills_rebuild(
    job_postings: list[JobPosting],
) -> dict[str, int]:
    skill_counts = Counter()

    for job_posting in job_postings:
        unique_skills = set(job_posting.skills)
        skill_counts.update(unique_skills)

    return dict(skill_counts)


def skill_ranking_key_rebuild(
    skill_count: tuple[str, int],
) -> tuple[int, str]:
    skill, count = skill_count
    return (-count, skill)


def rank_skills_rebuild(
    skill_counts: dict[str, int],
) -> list[tuple[str, int]]:
    return sorted(skill_counts.items(), key=skill_ranking_key_rebuild)
