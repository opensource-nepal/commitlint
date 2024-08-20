# type: ignore
# pylint: disable=all

import json
import os
from unittest.mock import mock_open, patch

import pytest

from github_actions.action.event import GitHubEvent
from github_actions.action.run import run_action
from tests.fixtures.actions_env import set_github_env_vars


@pytest.fixture(scope="module", autouse=True)
def setup_env():
    set_github_env_vars()


@pytest.fixture(autouse=True)
def mock_open_file():
    with patch("builtins.open", mock_open(read_data=json.dumps({}))) as mocked_open:
        yield mocked_open


@patch("github_actions.action.run._handle_push_event")
@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "push"})
def test__run_action__calls_handle_push_events(mock_handle_push_event):
    run_action()
    mock_handle_push_event.assert_called_once()
    args, _ = mock_handle_push_event.call_args
    assert type(args[0]) == GitHubEvent
    assert args[0].event_name == "push"


@patch("github_actions.action.run._handle_pr_event")
@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "pull_request"})
def test__run_action__calls_handle_pr_events(mock_handle_pr_event):
    run_action()
    mock_handle_pr_event.assert_called_once()
    args, _ = mock_handle_pr_event.call_args
    assert type(args[0]) == GitHubEvent
    assert args[0].event_name == "pull_request"


@patch("github_actions.action.run._handle_pr_event")
@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "pull_request_target"})
def test__run_action__calls_handle_pr_events_for_pull_request_target(
    mock_handle_pr_event,
):
    run_action()
    mock_handle_pr_event.assert_called_once()
    args, _ = mock_handle_pr_event.call_args
    assert type(args[0]) == GitHubEvent
    assert args[0].event_name == "pull_request_target"


@patch("sys.stdout.write")
@patch.dict(os.environ, {**os.environ, "GITHUB_EVENT_NAME": "workflow_dispatch"})
def test__run_action__skips_unknown_event(mock_stdout_write):
    run_action()
    mock_stdout_write.assert_called_once_with("Skipping for event workflow_dispatch\n")
