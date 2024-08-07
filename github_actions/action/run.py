"""
This module runs the actions based on GitHub events, specifically for push,
pull_request and pull_request_target events.
"""

import os
import subprocess
import sys
from math import ceil
from typing import Iterable, List, Optional, Tuple, cast

from .event import GitHubEvent
from .utils import (
    get_boolean_input,
    get_input,
    request_github_api,
    write_line_to_file,
    write_output,
)

# Events
EVENT_PUSH = "push"
EVENT_PULL_REQUEST = "pull_request"
EVENT_PULL_REQUEST_TARGET = "pull_request_target"

# Inputs
INPUT_TOKEN = "token"
INPUT_FAIL_ON_ERROR = "fail_on_error"
INPUT_VERBOSE = "verbose"

# Status
STATUS_SUCCESS = "success"
STATUS_FAILURE = "failure"

MAX_PR_COMMITS = 250


def get_push_commit_messages(event: GitHubEvent) -> Iterable[str]:
    """
    Return push commits.

    Args:
        event (GitHubEvent): An instance of the GitHubEvent class representing
            the GitHub event.

    Returns:
        List[str]: List of github commits.
    """
    return (commit_data["message"] for commit_data in event.payload["commits"])


def get_pr_commit_messages(event: GitHubEvent) -> Iterable[str]:
    """
    Return PR commits.

    Args:
        event (GitHubEvent): An instance of the GitHubEvent class representing
            the GitHub event.

    Returns:
        List[str]: List of github commits.
    """
    token = get_input(INPUT_TOKEN)
    repo = event.repository
    pr_number: int = event.payload["number"]
    total_commits: int = event.payload["pull_request"]["commits"]

    if total_commits > MAX_PR_COMMITS:
        sys.exit(
            "::error:: GitHub API doesn't support PRs with more than "
            f"{MAX_PR_COMMITS} commits.\n"
            "Please refer to "
            "https://docs.github.com/en/rest/pulls/pulls"
            "?apiVersion=2022-11-28#list-commits-on-a-pull-request"
        )

    # pagination
    per_page = 50
    total_page = ceil(total_commits / per_page)

    commits: List[str] = []
    for page in range(1, total_page + 1):
        status, data = request_github_api(
            method="GET",
            url=f"/repos/{repo}/pulls/{pr_number}/commits",
            token=token,
            params={"per_page": per_page, "page": page},
        )

        if status != 200:
            sys.exit(f"::error::Github API failed with status code {status}")

        commits.extend(commit_data["commit"]["message"] for commit_data in data)

    return commits


def run_commitlint(commit_message: str) -> Tuple[bool, Optional[str]]:
    """
    Run the commitlint for the given commit message.

    Args:
        commit_message (str): A commit message to check with commitlint.

    Returns:
        Tuple[bool, Optional[str]]: A tuple with the success status as the first
            element and error message as the second element.
    """

    try:
        commands = ["commitlint", commit_message, "--hide-input"]

        verbose = get_boolean_input(INPUT_VERBOSE)
        if verbose:
            commands.append("--verbose")

        output = subprocess.check_output(commands, text=True, stderr=subprocess.PIPE)
        if output:
            sys.stdout.write(f"{output}")

        return True, None
    except subprocess.CalledProcessError as error:
        if error.stdout:
            sys.stdout.write(f"{error.stdout}")

        return False, str(error.stderr)


def check_commit_messages(commit_messages: Iterable[str]) -> None:
    """
    Check the commit messages and create outputs for GitHub Actions.

    Args:
        commit_messages (Iterable[str]): List of commit messages to check.

    Raises:
        SystemExit: If any of the commit messages is invalid.
    """
    failed_commits_count = 0

    for commit_message in commit_messages:
        commit_message_header = commit_message.split("\n")[0]
        sys.stdout.write(f"\n⧗ {commit_message_header}\n")

        success, error = run_commitlint(commit_message)
        if success:
            continue

        error = (
            cast(str, error)
            .replace("%", "%25")
            .replace("\r", "%0D")
            .replace("\n", "%0A")
        )
        sys.stdout.write(f"::error title={commit_message_header}::{error}")
        failed_commits_count += 1

    # GitHub step summary path
    github_step_summary = os.environ["GITHUB_STEP_SUMMARY"]

    if failed_commits_count == 0:
        # success
        write_line_to_file(github_step_summary, "commitlint: All commits passed!")
        write_output("status", STATUS_SUCCESS)
        write_output("exit_code", 0)
        return

    # failure
    write_line_to_file(
        github_step_summary, f"commitlint: {failed_commits_count} commit(s) failed!"
    )
    write_output("status", STATUS_FAILURE)
    write_output("exit_code", 1)
    fail_on_error = get_boolean_input(INPUT_FAIL_ON_ERROR)
    if fail_on_error:
        sys.exit(1)


def _handle_pr_event(event: GitHubEvent) -> None:
    """
    Handle pull_request GitHub event.

    Args:
        event (GitHubEvent): An instance of the GitHubEvent class representing
            the GitHub event.
    """
    commit_messages = get_pr_commit_messages(event)
    check_commit_messages(commit_messages)


def _handle_push_event(event: GitHubEvent) -> None:
    """
    Handle push GitHub event.

    Args:
        event (GitHubEvent): An instance of the GitHubEvent class representing
            the GitHub event.
    """
    commit_messages = get_push_commit_messages(event)
    check_commit_messages(commit_messages)


def run_action() -> None:
    """Run commitlint action"""
    event = GitHubEvent()

    if event.event_name == EVENT_PUSH:
        _handle_push_event(event)
    elif event.event_name in (EVENT_PULL_REQUEST, EVENT_PULL_REQUEST_TARGET):
        _handle_pr_event(event)
    else:
        sys.stdout.write(f"Skipping for event {event.event_name}\n")
