# type: ignore
# pylint: disable=all
import os
import subprocess
from unittest.mock import patch

from github_actions.action.run import run_commitlint


@patch("subprocess.check_output", return_value="feat: valid commit message")
@patch.dict(os.environ, {**os.environ, "INPUT_VERBOSE": "False"})
def test__run_commitlint__success(mock_check_output):
    commit_message = "feat: add new feature"

    result = run_commitlint(commit_message)

    assert result == (True, None)
    mock_check_output.assert_called_once_with(
        ["commitlint", commit_message, "--hide-input"],
        text=True,
        stderr=subprocess.PIPE,
    )


@patch("subprocess.check_output")
@patch.dict(os.environ, {**os.environ, "INPUT_VERBOSE": "False"})
def test__run_commitlint__failure(mock_check_output):
    mock_check_output.side_effect = (
        subprocess.CalledProcessError(1, "cmd", output="", stderr="Error"),
    )

    commit_message = "invalid commit message"
    result = run_commitlint(commit_message)

    assert result == (False, "Error")
    mock_check_output.assert_called_once_with(
        ["commitlint", commit_message, "--hide-input"],
        text=True,
        stderr=subprocess.PIPE,
    )


@patch(
    "subprocess.check_output",
    return_value="feat: valid commit message",
)
@patch.dict(os.environ, {**os.environ, "INPUT_VERBOSE": "True"})
def test__run_commitlint__verbose(mock_check_output):
    commit_message = "feat: add new feature"

    result = run_commitlint(commit_message)

    assert result == (True, None)
    mock_check_output.assert_called_once_with(
        ["commitlint", commit_message, "--hide-input", "--verbose"],
        text=True,
        stderr=subprocess.PIPE,
    )
