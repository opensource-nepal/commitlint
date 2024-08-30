# type: ignore
# pylint: disable=all
import os
from unittest.mock import patch

import pytest

from github_actions.action.run import check_commit_messages
from tests.fixtures.actions_env import set_github_env_vars

# Constants
STATUS_SUCCESS = "success"
STATUS_FAILURE = "failure"
INPUT_FAIL_ON_ERROR = "fail_on_error"


@pytest.fixture(scope="module", autouse=True)
def setup_env():
    set_github_env_vars()


@patch("github_actions.action.run.run_commitlint")
@patch("github_actions.action.run.write_line_to_file")
@patch("github_actions.action.run.write_output")
@patch.dict(os.environ, {**os.environ, "GITHUB_STEP_SUMMARY": "summary_path"})
def test__check_commit_messages__all_valid_messages(
    mock_write_output,
    mock_write_line_to_file,
    mock_run_commitlint,
):
    commit_messages = ["feat: valid commit 1", "fix: valid commit 2"]
    mock_run_commitlint.return_value = (True, None)

    check_commit_messages(commit_messages)

    mock_run_commitlint.assert_any_call("feat: valid commit 1")
    mock_run_commitlint.assert_any_call("fix: valid commit 2")
    mock_write_line_to_file.assert_called_once_with(
        "summary_path", "commitlint: All commits passed!"
    )
    mock_write_output.assert_any_call("status", STATUS_SUCCESS)
    mock_write_output.assert_any_call("exit_code", 0)


@patch("github_actions.action.run.run_commitlint")
@patch("github_actions.action.run.write_line_to_file")
@patch("github_actions.action.run.write_output")
@patch.dict(os.environ, {**os.environ, "GITHUB_STEP_SUMMARY": "summary_path"})
def test__check_commit_messages__partial_invalid_messages(
    mock_write_output,
    mock_write_line_to_file,
    mock_run_commitlint,
):
    commit_messages = ["feat: valid commit", "invalid commit message"]
    mock_run_commitlint.side_effect = [
        (True, None),
        (False, "Error: invalid commit format"),
    ]

    with pytest.raises(SystemExit):
        check_commit_messages(commit_messages)

    mock_run_commitlint.assert_any_call("feat: valid commit")
    mock_run_commitlint.assert_any_call("invalid commit message")
    mock_write_line_to_file.assert_called_once_with(
        "summary_path", "commitlint: 1 commit(s) failed!"
    )
    mock_write_output.assert_any_call("status", STATUS_FAILURE)
    mock_write_output.assert_any_call("exit_code", 1)


@patch("github_actions.action.run.run_commitlint")
@patch("github_actions.action.run.write_line_to_file")
@patch("github_actions.action.run.write_output")
@patch.dict(
    os.environ,
    {
        **os.environ,
        "GITHUB_STEP_SUMMARY": "summary_path",
        "INPUT_FAIL_ON_ERROR": "False",
    },
)
def test__check_commit_messages__fail_on_error_false(
    mock_write_output,
    mock_write_line_to_file,
    mock_run_commitlint,
):
    commit_messages = ["invalid commit message"]
    mock_run_commitlint.return_value = (False, "Invalid commit format")

    check_commit_messages(commit_messages)

    mock_run_commitlint.assert_called_once_with("invalid commit message")
    mock_write_line_to_file.assert_called_once_with(
        "summary_path", "commitlint: 1 commit(s) failed!"
    )
    mock_write_output.assert_any_call("status", STATUS_FAILURE)
    mock_write_output.assert_any_call("exit_code", 1)
