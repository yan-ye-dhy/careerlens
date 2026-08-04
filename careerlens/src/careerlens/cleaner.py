def normalize_whitespace(text: str) -> str:
    """合并每行内部的连续空白、去除每行首尾空白，但保留行结构"""
    lines = text.splitlines()
    normalized_lines = []
    for line in lines:
        normalized_line = " ".join(line.split())
        normalized_lines.append(normalized_line)
    normalized_text = "\n".join(normalized_lines)
    return normalized_text


def remove_empty_lines(text: str) -> str:
    """删除空行，保留非空行的内容与顺序"""
    lines = text.splitlines()
    non_empty_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        non_empty_lines.append(line)
    result = "\n".join(non_empty_lines)
    return result


def clean_jd(text: str) -> str:
    """清洗JD，使其输出规范化，按固定顺序组合前两个规则"""
    normalized_text = normalize_whitespace(text)
    cleaned_text = remove_empty_lines(normalized_text)
    return cleaned_text