import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from careerlens.analysis import count_job_skills, rank_skills
from careerlens.batch import process_job_files
from careerlens.cleaner import clean_jd
from careerlens.parser import parse_job_posting


def create_argument_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        description="清洗招聘 JD 或导出结构化 JSON",
    )
    mode_group = argument_parser.add_mutually_exclusive_group()

    mode_group.add_argument(
        "--json",
        action="store_true",
        help="将单份 JD 导出为结构化 JSON",
    )
    mode_group.add_argument(
        "--batch-json",
        action="store_true",
        help="将输入目录中的多份 JD 导出为批量 JSON 报告",
    )
    argument_parser.add_argument(
        "input_path",
        help="输入文件或目录路径",
    )
    argument_parser.add_argument(
        "output_path",
        help="输出文件路径",
    )
    return argument_parser


def create_batch_report(input_directory: Path) -> dict:
    batch_result = process_job_files(input_directory)

    job_postings = list(
        batch_result.jobs.values()
    )
    skill_counts = count_job_skills(job_postings)
    ranked_skills = rank_skills(skill_counts)

    skill_ranking = [
        {
            "skill": skill,
            "count": count,
        }
        for skill, count in ranked_skills
    ]

    batch_report = asdict(batch_result)
    batch_report["skill_counts"] = skill_counts
    batch_report["skill_ranking"] = skill_ranking

    return batch_report


def main() -> int:
    argument_parser = create_argument_parser()
    arguments = argument_parser.parse_args()

    json_mode = arguments.json
    batch_json_mode = arguments.batch_json
    input_path = arguments.input_path
    output_path = arguments.output_path

    if batch_json_mode:
        try:
            json_data = create_batch_report(
                Path(input_path)
            )
        except OSError as error:
            print(
                "错误：批量输入无法处理：",
                error,
                sep="",
            )
            return 1
    else:
        try:
            with open(
                input_path,
                "r",
                encoding="utf-8",
            ) as input_file:
                raw_text = input_file.read()
        except FileNotFoundError:
            print(
                "错误：输入文件不存在：",
                input_path,
            )
            return 1

        cleaned_text = clean_jd(raw_text)

        if json_mode:
            try:
                job_posting = parse_job_posting(
                    cleaned_text
                )
            except ValueError as error:
                print(
                    "错误：岗位信息无法解析：",
                    error,
                    sep="",
                )
                return 1

            json_data = asdict(job_posting)

    try:
        output_file_path = Path(output_path)
        output_file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as output_file:
            if json_mode or batch_json_mode:
                json.dump(
                    json_data,
                    output_file,
                    ensure_ascii=False,
                    indent=2,
                )
            else:
                output_file.write(cleaned_text)
    except OSError as error:
        print(
            "错误：输出文件无法写入：",
            error,
            sep="",
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
