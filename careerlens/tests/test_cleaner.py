from careerlens.cleaner import normalize_whitespace, remove_empty_lines, clean_jd


def test_normalize_continuous_spaces():
    input_text = "AI   Agent"
    actual = normalize_whitespace(input_text)
    expected = "AI Agent"
    assert actual == expected


def test_normalize_tab_and_newline():
    input_text = "AI\tAgent\nPython"
    actual = normalize_whitespace(input_text)
    expected = "AI Agent\nPython"
    assert actual == expected


def test_normalize_leading_and_trailing_whitespace():
    input_text = "  AI Agent  "
    actual = normalize_whitespace(input_text)
    expected = "AI Agent"
    assert actual == expected


def test_remove_multiple_empty_lines():
    input_text = "AI\n\n   \nPython"
    actual = remove_empty_lines(input_text)
    expected = "AI\nPython"
    assert actual == expected


def test_clean_jd_empty_text():
    input_text = ""
    actual = clean_jd(input_text)
    expected = ""
    assert actual == expected


def test_clean_jd_whitespace_only():
    input_text = "   \n\t\n"
    actual = clean_jd(input_text)
    expected = ""
    assert actual == expected


def test_clean_jd_mixed_chinese_english_and_punctuation():
    input_text = "  技能要求： Python   Git，熟悉 Agent！  "
    actual = clean_jd(input_text)
    expected = "技能要求： Python Git，熟悉 Agent！"
    assert actual == expected


def test_clean_jd_is_idempotent():
    input_text = "  AI   Agent\n\n技能： Python\tGit  "
    cleaned_once = clean_jd(input_text)
    cleaned_twice = clean_jd(cleaned_once)
    assert cleaned_once == cleaned_twice
