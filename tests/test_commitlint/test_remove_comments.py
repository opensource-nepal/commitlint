# type: ignore
# pylint: disable=all

from src.commitlint.commitlint import remove_comments


def test__remove_comments__no_comments():
    input_msg = "Commit message without comments"
    expected_output = "Commit message without comments"
    result = remove_comments(input_msg)
    assert result == expected_output


def test__remove_comments__with_comments():
    input_msg = "# Comment\nRegular text"
    expected_output = "Regular text"
    result = remove_comments(input_msg)
    assert result == expected_output


def test__remove_comments__with_diff_message():
    input_msg = (
        "Fix a bug\n"
        "# ------------------------ >8 ------------------------\n"
        "Diff message"
    )
    expected_output = "Fix a bug"
    result = remove_comments(input_msg)
    assert result == expected_output


def test__remove_comments__multiple_comments():
    input_msg = "New feature\n# Comment\n# Another comment"
    expected_output = "New feature"
    result = remove_comments(input_msg)
    assert result == expected_output


def test__remove_comments__comments_before_diff():
    input_msg = (
        "#Comments\n"
        "# ------------------------ >8 ------------------------\n"
        "Diff message"
    )
    expected_output = ""
    result = remove_comments(input_msg)
    assert result == expected_output
