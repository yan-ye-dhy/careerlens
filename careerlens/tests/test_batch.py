from pathlib import Path

import pytest

from careerlens.batch import (
    list_text_files,
    process_job_files,
    read_text_files,
)
from careerlens.models import JobPosting


def test_list_text_files_filters_and_sorts(tmp_path: Path):
    (tmp_path / "b.txt").write_text(
        "岗位 B",
        encoding="utf-8",
    )
    (tmp_path / "a.TXT").write_text(
        "岗位 A",
        encoding="utf-8",
    )
    (tmp_path / "notes.md").write_text(
        "说明",
        encoding="utf-8",
    )
    (tmp_path / "folder.txt").mkdir()

    actual = list_text_files(tmp_path)
    expected = [
        tmp_path / "a.TXT",
        tmp_path / "b.txt",
    ]

    assert actual == expected


@pytest.mark.parametrize(
    ("path_kind", "expected_error"),
    [
        ("missing", FileNotFoundError),
        ("file", NotADirectoryError),
    ],
    ids=[
        "missing-path",
        "file-path",
    ],
)
def test_list_text_files_rejects_invalid_input(
    tmp_path: Path,
    path_kind: str,
    expected_error: type[Exception],
):
    input_path = tmp_path / "input"

    if path_kind == "file":
        input_path.write_text(
            "不是目录",
            encoding="utf-8",
        )

    with pytest.raises(expected_error):
        list_text_files(input_path)


def test_process_job_files_isolates_failure_and_uses_extractor(
    tmp_path: Path,
):
    first_valid_path = tmp_path / "a_valid.txt"
    invalid_path = tmp_path / "b_invalid.txt"
    second_valid_path = tmp_path / "c_valid.txt"

    first_valid_path.write_text(
        "  岗位   A  ",
        encoding="utf-8",
    )
    invalid_path.write_text(
        "   \n\t\n",
        encoding="utf-8",
    )
    second_valid_path.write_text(
        "岗位   C",
        encoding="utf-8",
    )

    def fake_extractor(cleaned_text: str) -> JobPosting:
        if not cleaned_text:
            raise ValueError("提取器收到空文本")
        return JobPosting(
            title=cleaned_text,
            skills=["Demo"],
            responsibilities=[],
            remote=None,
            salary=None,
        )

    result = process_job_files(
        tmp_path,
        extractor=fake_extractor,
    )

    actual_job_paths = list(result.jobs)
    expected_job_paths = [
        str(first_valid_path),
        str(second_valid_path),
    ]

    assert actual_job_paths == expected_job_paths
    assert isinstance(
        result.jobs[str(first_valid_path)],
        JobPosting,
    )
    assert isinstance(
        result.jobs[str(second_valid_path)],
        JobPosting,
    )
    assert result.jobs[str(first_valid_path)].title == "岗位 A"
    assert result.jobs[str(second_valid_path)].title == "岗位 C"
    assert result.failures == {
        str(invalid_path): "提取器收到空文本",
    }


def test_read_text_files_returns_source_path_and_text(
    tmp_path: Path,
):
    text_path = tmp_path / "sample.txt"
    text_path.write_text(
        "  岗位 A  ",
        encoding="utf-8",
    )

    actual = read_text_files(tmp_path)
    expected = [
        (
            text_path,
            "  岗位 A  ",
        ),
    ]

    assert actual == expected


def test_read_text_files_empty_directory_returns_empty_list(
    tmp_path: Path,
):
    actual = read_text_files(tmp_path)
    expected = []

    assert actual == expected
