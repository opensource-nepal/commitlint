# type: ignore
# pylint: disable=all
import json
import os
from unittest.mock import mock_open, patch

import pytest

from github_actions.action.event import GitHubEvent
from github_actions.action.run import (
    MAX_PR_COMMITS,
    PER_PAGE_COMMITS,
    get_pr_commit_messages,
)
from tests.fixtures.actions_env import set_github_env_vars


@pytest.fixture(scope="module", autouse=True)
def setup_env():
    set_github_env_vars()


@patch("github_actions.action.run.request_github_api")
@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "pull_request"})
def test__get_pr_commit_messages__single_page(
    mock_request_github_api,
):
    # mock github api request
    mock_request_github_api.return_value = (
        200,
        [{"commit": {"message": "feat: commit message"}}],
    )

    payload = {"number": 10, "pull_request": {"commits": 2}}
    with patch("builtins.open", mock_open(read_data=json.dumps(payload))):
        event = GitHubEvent()
        result = get_pr_commit_messages(event)
        assert result == ["feat: commit message"]

    mock_request_github_api.assert_called_once_with(
        method="GET",
        url="/repos/opensource-nepal/commitlint/pulls/10/commits",
        token="token",
        params={"per_page": PER_PAGE_COMMITS, "page": 1},
    )


@patch("github_actions.action.run.request_github_api")
@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "pull_request"})
def test__get_pr_commit_messages__multiple_page(
    mock_request_github_api,
):
    # mock github api request
    mock_request_github_api.side_effect = [
        (
            200,
            [{"commit": {"message": "feat: commit message1"}}],
        ),
        (
            200,
            [{"commit": {"message": "feat: commit message2"}}],
        ),
    ]

    payload = {"number": 10, "pull_request": {"commits": 60}}
    with patch("builtins.open", mock_open(read_data=json.dumps(payload))):
        event = GitHubEvent()
        result = get_pr_commit_messages(event)
        assert result == ["feat: commit message1", "feat: commit message2"]

    assert mock_request_github_api.call_count == 2
    mock_request_github_api.assert_any_call(
        method="GET",
        url="/repos/opensource-nepal/commitlint/pulls/10/commits",
        token="token",
        params={"per_page": PER_PAGE_COMMITS, "page": 1},
    )

    mock_request_github_api.assert_any_call(
        method="GET",
        url="/repos/opensource-nepal/commitlint/pulls/10/commits",
        token="token",
        params={"per_page": PER_PAGE_COMMITS, "page": 2},
    )


@patch("github_actions.action.run.request_github_api")
@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "pull_request"})
def test__get_pr_commit_messages__api_failure(
    mock_request_github_api,
):
    mock_request_github_api.return_value = (500, None)
    payload = {"number": 10, "pull_request": {"commits": 60}}
    with patch("builtins.open", mock_open(read_data=json.dumps(payload))):
        with pytest.raises(SystemExit):
            event = GitHubEvent()
            get_pr_commit_messages(event)


@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "pull_request"})
def test__get_pr_commit_messages__exceed_max_commits():
    payload = {"number": 10, "pull_request": {"commits": MAX_PR_COMMITS + 1}}
    with patch("builtins.open", mock_open(read_data=json.dumps(payload))):
        with pytest.raises(SystemExit):
            event = GitHubEvent()
            get_pr_commit_messages(event)
