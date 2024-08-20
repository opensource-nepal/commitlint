# type: ignore
# pylint: disable=all

import json
import os
from unittest.mock import mock_open, patch

import pytest

from github_actions.action.event import GitHubEvent
from tests.fixtures.actions_env import set_github_env_vars

MOCK_PAYLOAD = {"key": "value"}


@pytest.fixture(scope="module")
def github_event():
    set_github_env_vars()
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_PAYLOAD))):
        return GitHubEvent()


def test__github_event__initialization(github_event):
    assert github_event.event_name == "push"
    assert github_event.sha == "commitlint_sha"
    assert github_event.ref == "refs/heads/main"
    assert github_event.workflow == "commitlint_ci"
    assert github_event.action == "action"
    assert github_event.actor == "actor"
    assert github_event.repository == "opensource-nepal/commitlint"
    assert github_event.job == "job"
    assert github_event.run_attempt == "9"
    assert github_event.run_number == "8"
    assert github_event.run_id == "7"
    assert github_event.event_path == "/tmp/github_event.json"
    assert github_event.payload == MOCK_PAYLOAD


def test__github_event__to_dict(github_event):
    event_dict = github_event.to_dict()
    assert event_dict["event_name"] == "push"
    assert event_dict["sha"] == "commitlint_sha"
    assert event_dict["ref"] == "refs/heads/main"
    assert event_dict["workflow"] == "commitlint_ci"
    assert event_dict["action"] == "action"
    assert event_dict["actor"] == "actor"
    assert event_dict["repository"] == "opensource-nepal/commitlint"
    assert event_dict["job"] == "job"
    assert event_dict["run_attempt"] == "9"
    assert event_dict["run_number"] == "8"
    assert event_dict["run_id"] == "7"
    assert event_dict["event_path"] == "/tmp/github_event.json"
    assert event_dict["payload"] == MOCK_PAYLOAD


def test__github_event__str(github_event):
    event_str = str(github_event)
    assert "push" in event_str
    assert "commitlint_sha" in event_str
    assert "refs/heads/main" in event_str
    assert "commitlint_ci" in event_str
    assert "action" in event_str
    assert "actor" in event_str
    assert "opensource-nepal/commitlint" in event_str
    assert "job" in event_str
    assert "9" in event_str


def test__github_event__env_error():
    os.environ.pop("GITHUB_EVENT_NAME")
    with pytest.raises(EnvironmentError):
        GitHubEvent()
