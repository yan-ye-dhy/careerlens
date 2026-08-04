import sys
from pathlib import Path

from careerlens.cleaner import clean_jd


def main() -> int:
    if len(sys.argv) != 3:
        print("用法：python3 -m careerlens.cli <输入路径> <输出路径>")
        return 1
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    try:
        with open(input_path, "r", encoding="utf-8") as input_file:
            raw_text = input_file.read()
    except FileNotFoundError:
        print("错误：输入文件不存在：", input_path)
        return 1
    cleaned_text = clean_jd(raw_text)
    output_file_path = Path(output_path)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(cleaned_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())