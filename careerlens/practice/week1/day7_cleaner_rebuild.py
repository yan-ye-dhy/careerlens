def normalize_whitespace_simple(text: str) -> str:
    lines = text.splitlines()
    normalized_lines = []
    for line in lines:
        words = line.split()
        normalized_line = " ".join(words)
        normalized_lines.append(normalized_line)
    normalized_text = "\n".join(normalized_lines)
    return normalized_text


def remove_empty_lines_simple(text: str) -> str:
    lines = text.splitlines()
    non_empty_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        non_empty_lines.append(line)
    cleaned_text = "\n".join(non_empty_lines)
    return cleaned_text


def clean_jd_simple(text: str) -> str:
    normalized_text = normalize_whitespace_simple(text)
    cleaned_text = remove_empty_lines_simple(normalized_text)
    return cleaned_text