import json
import sys
from dataclasses import asdict
from pathlib import Path

from careerlens.cleaner import clean_jd
from careerlens.parser import parse_job_posting


def main() -> int:
    json_mode = False

    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    elif len(sys.argv) == 4 and sys.argv[1] == "--json":
        json_mode = True
        input_path = sys.argv[2]
        output_path = sys.argv[3]
    else:
        print("用法：")
        print("  python3 -m careerlens.cli <输入路径> <输出路径>")
        print("  python3 -m careerlens.cli --json <输入路径> <输出路径>")
        return 1

    try:
        with open(input_path, "r", encoding="utf-8") as input_file:
            raw_text = input_file.read()
    except FileNotFoundError:
        print("错误：输入文件不存在：", input_path)
        return 1

    cleaned_text = clean_jd(raw_text)
    if json_mode:
        try:
            job_posting = parse_job_posting(cleaned_text)
        except ValueError as error:
            print("错误：岗位信息无法解析：", error, sep="")
            return 1
        job_dict = asdict(job_posting)

    output_file_path = Path(output_path)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output_file:
        if json_mode:
            json.dump(job_dict, output_file, ensure_ascii=False, indent=2)
        else:
            output_file.write(cleaned_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
