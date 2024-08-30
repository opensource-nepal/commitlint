# type: ignore
# pylint: disable=all

import json
from unittest.mock import mock_open, patch

import pytest

from github_actions.action.event import GitHubEvent
from github_actions.action.run import get_push_commit_messages
from tests.fixtures.actions_env import set_github_env_vars


@pytest.fixture(scope="module", autouse=True)
def setup_env():
    set_github_env_vars()


def test__get_push_commit_messages__returns_push_commits():
    payload = {
        "commits": [
            {"message": "feat: valid message"},
            {"message": "fix(login): fix login message"},
        ]
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(payload))):
        commits = get_push_commit_messages(GitHubEvent())
        assert list(commits) == ["feat: valid message", "fix(login): fix login message"]
