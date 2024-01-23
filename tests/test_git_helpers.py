# type: ignore
# pylint: disable=all
import subprocess
from unittest.mock import patch

import pytest

from src.commitlint.exceptions import (
    GitCommitNotFoundException,
    GitInvalidCommitRangeException,
)
from src.commitlint.git_helpers import (
    get_commit_message_of_hash,
    get_commit_messages_of_hash_range,
)

DELIMITER = "========commit-delimiter========"


@pytest.fixture
def mock_subprocess():
    with patch("src.commitlint.git_helpers.subprocess") as mock_subprocess:
        mock_subprocess.PIPE = subprocess.PIPE
        mock_subprocess.CalledProcessError = subprocess.CalledProcessError
        yield mock_subprocess


def test_get_commit_message_of_hash_success(mock_subprocess):
    hash_value = "abc123"
    expected_output = "Commit message for abc123"
    mock_subprocess.check_output.return_value = expected_output

    result = get_commit_message_of_hash(hash_value)

    assert result == expected_output
    mock_subprocess.check_output.assert_called_once_with(
        ["git", "show", "--format=%B", "-s", hash_value],
        text=True,
        stderr=subprocess.PIPE,
    )


def test_get_commit_message_of_hash_failure(mock_subprocess):
    hash_value = "invalid_hash"

    mock_subprocess.check_output.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd=["git", "show", "--format=%B", "-s", hash_value]
    )

    with pytest.raises(GitCommitNotFoundException):
        get_commit_message_of_hash(hash_value)


@patch(
    "src.commitlint.git_helpers.get_commit_message_of_hash",
    return_value="From commit message",
)
def test_get_commit_messages_of_hash_range_success(
    _mock_get_commit_message_of_hash, mock_subprocess
):
    from_hash = "abc123"
    to_hash = "def456"
    expected_output = (
        "Commit message 1\n========commit-delimiter========\nCommit message 2"
    )
    mock_subprocess.check_output.return_value = expected_output

    result = get_commit_messages_of_hash_range(from_hash, to_hash)

    assert result == ["From commit message", "Commit message 1", "Commit message 2"]
    mock_subprocess.check_output.assert_called_once_with(
        [
            "git",
            "log",
            f"--format=%B{DELIMITER}",
            "--reverse",
            f"{from_hash}..{to_hash}",
        ],
        text=True,
        stderr=subprocess.PIPE,
    )


@patch(
    "src.commitlint.git_helpers.get_commit_message_of_hash",
    return_value="From commit message",
)
def test_get_commit_messages_of_hash_range_failure(
    _mock_get_commit_message_of_hash, mock_subprocess
):
    from_hash = "invalid_hash"
    to_hash = "def456"
    mock_subprocess.check_output.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=[
            "git",
            "log",
            f"--format=%B{DELIMITER}",
            "--reverse",
            f"{from_hash}..{to_hash}",
        ],
    )

    with pytest.raises(GitInvalidCommitRangeException):
        get_commit_messages_of_hash_range(from_hash, to_hash)
