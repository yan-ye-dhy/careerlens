from collections.abc import Callable
from pathlib import Path

from careerlens.cleaner import clean_jd
from careerlens.models import BatchResult, JobPosting
from careerlens.parser import parse_job_posting


def list_text_files(input_directory: Path) -> list[Path]:
    if not input_directory.exists():
        raise FileNotFoundError("输入目录不存在：" + str(input_directory))
    if not input_directory.is_dir():
        raise NotADirectoryError("输入路径不是目录：" + str(input_directory))

    text_paths: list[Path] = []

    for child_path in input_directory.iterdir():
        if child_path.is_file() and child_path.suffix.lower() == ".txt":
            text_paths.append(child_path)

    return sorted(text_paths)


def read_text_files(input_directory: Path) -> list[tuple[Path, str]]:
    text_paths = list_text_files(input_directory)

    loaded_texts: list[tuple[Path, str]] = []

    for text_path in text_paths:
        text = text_path.read_text(encoding="utf-8")
        loaded_texts.append((text_path, text))

    return loaded_texts


def process_job_files(
    input_directory: Path,
    extractor: Callable[[str], JobPosting] = parse_job_posting,
) -> BatchResult:
    text_paths = list_text_files(input_directory)

    jobs: dict[str, JobPosting] = {}

    failures: dict[str, str] = {}

    for text_path in text_paths:
        source_path = str(text_path)

        try:
            raw_text = text_path.read_text(encoding="utf-8")
            cleaned_text = clean_jd(raw_text)
            job_posting = extractor(cleaned_text)
        except (OSError, ValueError) as error:
            failures[source_path] = str(error)
        else:
            jobs[source_path] = job_posting

    batch_result = BatchResult(
        jobs=jobs,
        failures=failures,
    )

    return batch_result
