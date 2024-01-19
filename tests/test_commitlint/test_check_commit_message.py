# type: ignore
# pylint: disable=all

from src.commitlint import check_commit_message
from src.commitlint.constants import COMMIT_MAX_LENGTH
from src.commitlint.messages import HEADER_LENGTH_ERROR, INCORRECT_FORMAT_ERROR


def test__check_commit_message__header_length_error():
    commit_message = "feat: " + "a" * (COMMIT_MAX_LENGTH + 1)
    success, errors = check_commit_message(commit_message)
    assert success is False
    assert HEADER_LENGTH_ERROR in errors


def test__check_commit_message__header_length_valid():
    commit_message = "feat: " + "a" * (COMMIT_MAX_LENGTH - 1)
    success, errors = check_commit_message(commit_message)
    assert success is False
    assert HEADER_LENGTH_ERROR in errors


def test__check_commit_message__incorrect_format_error():
    commit_message = "This is an invalid commit message"
    success, errors = check_commit_message(commit_message)
    assert success is False
    assert INCORRECT_FORMAT_ERROR in errors


def test__check_commit_message__incorrect_format_error_and_health_length_invalid():
    commit_message = "Test " + "a" * (COMMIT_MAX_LENGTH + 1)
    success, errors = check_commit_message(commit_message)
    assert success is False
    assert HEADER_LENGTH_ERROR in errors
    assert INCORRECT_FORMAT_ERROR in errors


def test__check_commit_message__valid():
    commit_message = "feat: add new feature"
    success, errors = check_commit_message(commit_message)
    assert success is True
    assert errors == []


def test__check_commit_message__valid_with_scope():
    commit_message = "feat(scope): add new feature"
    success, errors = check_commit_message(commit_message)
    assert success is True
    assert errors == []


def test__check_commit_message__empty_scope_error():
    commit_message = "feat(): add new feature"
    success, errors = check_commit_message(commit_message)
    assert success is False
    assert INCORRECT_FORMAT_ERROR in errors


def test__check_commit_message__valid_with_body():
    commit_message = "fix(scope): fix a bug\n\nThis is the body of the commit message."
    success, errors = check_commit_message(commit_message)
    assert success is True
    assert errors == []


def test__check_commit_message__header_line_error():
    commit_message = "feat(): add new feature\ntest"
    success, errors = check_commit_message(commit_message)
    assert success is False
    assert INCORRECT_FORMAT_ERROR in errors


def test__check_commit_message__with_comments():
    commit_message = "feat(scope): add new feature\n#this is a comment"
    success, errors = check_commit_message(commit_message)
    assert success is True
    assert errors == []


def test__check_commit_message__with_diff():
    commit_message = (
        "fix: fixed a bug\n\nthis is body\n"
        "# ------------------------ >8 ------------------------\nDiff message"
    )
    success, errors = check_commit_message(commit_message)
    assert success is True
    assert errors == []


def test__check_commit_message__ignored():
    commit_message = "Merge pull request #123"
    success, errors = check_commit_message(commit_message)
    assert success is True
    assert errors == []
