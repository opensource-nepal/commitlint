# type: ignore
# pylint: disable=all

from commitlint.linter.utils import remove_diff_from_commit_message


def test__remove_diff_from_commit_message__without_diff():
    input_msg = "Commit message without diff"
    expected_output = "Commit message without diff"
    result = remove_diff_from_commit_message(input_msg)
    assert result == expected_output


def test__remove_diff_from_commit_message__with_diff():
    input_msg = (
        "Fix a bug\n"
        "# ------------------------ >8 ------------------------\n"
        "Diff message"
    )
    expected_output = "Fix a bug"
    result = remove_diff_from_commit_message(input_msg)
    assert result == expected_output


def test__remove_diff_from_commit_message__strips_commit_message():
    input_msg = "Commit message\n "
    expected_output = "Commit message"
    result = remove_diff_from_commit_message(input_msg)
    assert result == expected_output
