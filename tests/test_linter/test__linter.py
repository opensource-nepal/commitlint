# type: ignore
# pylint: disable=all

from unittest.mock import patch

import pytest

from commitlint.constants import COMMIT_HEADER_MAX_LENGTH
from commitlint.linter import lint_commit_message
from commitlint.messages import HEADER_LENGTH_ERROR, INCORRECT_FORMAT_ERROR

from ..fixtures.linter import LINTER_FIXTURE_PARAMS


@pytest.fixture(params=LINTER_FIXTURE_PARAMS)
def fixture_data(request):
    return request.param


def test_lint_commit_message(fixture_data):
    commit_message, expected_success, expected_errors = fixture_data
    success, errors = lint_commit_message(
        commit_message,
        skip_detail=False,
        disable_max_header_length=False,
        max_header_length=COMMIT_HEADER_MAX_LENGTH,
    )
    assert success == expected_success
    assert errors == expected_errors


def test__lint_commit_message__skip_detail(fixture_data):
    commit_message, expected_success, _ = fixture_data
    success, _ = lint_commit_message(
        commit_message,
        skip_detail=True,
        disable_max_header_length=False,
        max_header_length=COMMIT_HEADER_MAX_LENGTH,
    )
    assert success == expected_success


def test__lint_commit_message__remove_comments_if_strip_comments_is_True():
    commit_message = "feat(scope): add new feature\n#this is a comment"
    success, errors = lint_commit_message(
        commit_message,
        strip_comments=True,
        disable_max_header_length=False,
        max_header_length=COMMIT_HEADER_MAX_LENGTH,
    )
    assert success is True
    assert errors == []


@patch("commitlint.linter._linter.remove_comments")
def test__lint_commit_message__calls_remove_comments_if_strip_comments_is_True(
    mock_remove_comments,
):
    commit_message = "feat(scope): add new feature"
    mock_remove_comments.return_value = commit_message
    lint_commit_message(
        commit_message,
        strip_comments=True,
        disable_max_header_length=False,
        max_header_length=COMMIT_HEADER_MAX_LENGTH,
    )
    mock_remove_comments.assert_called_once()


def test__lint_commit_message__skip_detail_returns_header_length_error_message():
    commit_message = "Test " + "a" * (COMMIT_HEADER_MAX_LENGTH + 1)
    success, errors = lint_commit_message(
        commit_message,
        skip_detail=True,
        disable_max_header_length=False,
        max_header_length=COMMIT_HEADER_MAX_LENGTH,
    )
    assert success is False
    assert errors == [HEADER_LENGTH_ERROR]


def test__lint_commit_message__skip_detail_returns_invalid_format_error_message():
    commit_message = "Test invalid commit message"
    success, errors = lint_commit_message(
        commit_message,
        skip_detail=True,
        disable_max_header_length=False,
        max_header_length=COMMIT_HEADER_MAX_LENGTH,
    )
    assert success is False
    assert errors == [INCORRECT_FORMAT_ERROR]


def test__disable_header_length_check():
    commit_message = "feat: this is test for disabling the header length check (#77)"

    success, errors = lint_commit_message(
        commit_message,
        skip_detail=True,
        disable_max_header_length=True,
        max_header_length=COMMIT_HEADER_MAX_LENGTH,
    )
    assert success is True


def test__max_header_length_test():
    commit_message = "feat: this is test for disabling the header length check (#77)"
    success, errors = lint_commit_message(
        commit_message, skip_detail=True, max_header_length=20
    )
    assert success is False
    assert errors == [HEADER_LENGTH_ERROR]
