"""
This script contains actions to be taken based on GitHub events,
specifically for push and pull_request events.
"""

import os
import subprocess
import sys
from typing import Optional, Union

from event import GithubEvent

# Events
EVENT_PUSH = "push"
EVENT_PULL_REQUEST = "pull_request"

# Inputs
INPUT_FAIL_ON_ERROR = "INPUT_FAIL_ON_ERROR"

# Status
STATUS_SUCCESS = "success"
STATUS_FAILURE = "failure"


def _handle_pr_event(event: GithubEvent) -> None:
    """
    Handle pull_request GitHub event.

    Args:
        event (GithubEvent): An instance of the GithubEvent class representing
            the GitHub event.

    Raises:
        EnvironmentError: If the base SHA and head SHA cannot be retrieved from
            the event payload.
    """
    try:
        to_commit = event.payload["pull_request"]["head"]["sha"]

        # getting from_commit using the total commits count
        _total_commits = event.payload["pull_request"]["commits"]
        from_commit = f"{to_commit}~{_total_commits-1}"
        _check_commits(from_commit, to_commit)
    except KeyError:
        raise EnvironmentError("Unable to retrieve Base SHA and Head SHA") from None


def _handle_push_event(event: GithubEvent) -> None:
    """
    Handle push GitHub event.

    Args:
        event (GithubEvent): An instance of the GithubEvent class representing
            the GitHub event.

    Raises:
        EnvironmentError: If the from hash and to hash cannot be retrieved from
        the event payload.
    """
    try:
        commits = event.payload["commits"]
        from_commit = commits[0]["id"]
        to_commit = commits[-1]["id"]
        _check_commits(from_commit, to_commit)
    except KeyError:
        raise EnvironmentError("Unable to retrieve From hash and To hash") from None


def _write_output(name: str, value: Union[str, int]) -> None:
    """
    Writes an output to the GitHub Actions environment.

    Args:
        name (str): The name of the output variable.
        value: The value to be assigned to the output variable.

    Raises:
        OSError: If there is an issue opening or writing to the output file.
    """
    output_file_path = os.environ.get("GITHUB_OUTPUT", "")
    with open(file=output_file_path, mode="a", encoding="utf-8") as output_file:
        output_file.write(f"{name}={value}\n")


def _get_input(key: str) -> Optional[str]:
    """
    Reads the github action input

    Args:
        key (str): The environment variable to parse

    Returns:
        str or None: The value of the input or None if it is not set
    """
    return os.environ.get(key)


def _parse_boolean_input(val: Optional[str]) -> bool:
    """
    Parses the input environment key of boolean type in the YAML 1.2
    "core schema" specification.
    Support boolean input list:
    `true | True | TRUE | false | False | FALSE` .
    ref: https://yaml.org/spec/1.2/spec.html#id2804923

    Args:
        key (str, optional): The name of the environment variable to parse.

    Returns:
        bool: The parsed boolean value.

    Raises:
        TypeError: If the environment variable's value does not meet the
        YAML 1.2 "core schema" specification for booleans.
    """

    if val in {"true", "True", "TRUE"}:
        return True
    if val in {"false", "False", "FALSE"}:
        return False
    raise TypeError(
        """
        Input does not meet YAML 1.2 "Core Schema" specification.\n'
        Support boolean input list:
        `true | True | TRUE | false | False | FALSE
        """
    )


def _check_commits(from_hash: str, to_hash: str) -> None:
    """Check commits using commitlint.

    Args:
        from_hash (str): The hash of the starting commit.
        to_hash (str): The hash of the ending commit.
    """
    sys.stdout.write(f"Commit from {from_hash} to {to_hash}\n")
    try:
        output = subprocess.check_output(
            [
                "commitlint",
                "--from-hash",
                from_hash,
                "--to-hash",
                to_hash,
            ],
            text=True,
        ).strip()
        sys.stdout.write(f"{output}\n")

        _write_output("status", STATUS_SUCCESS)
        _write_output("exit_code", 0)

    except subprocess.CalledProcessError as error:
        sys.stderr.write("::error::Commit validation failed!\n")
        _write_output("status", STATUS_FAILURE)
        _write_output("exit_code", error.returncode)
        val = _get_input(INPUT_FAIL_ON_ERROR)
        fail_on_error = _parse_boolean_input(val)
        if fail_on_error:
            sys.exit(1)


def main() -> None:
    """Main entry point for the GitHub Actions workflow."""
    event = GithubEvent()

    if event.event_name == EVENT_PUSH:
        _handle_push_event(event)
    elif event.event_name == EVENT_PULL_REQUEST:
        _handle_pr_event(event)
    elif event.event_name is None:
        sys.stdout.write("No any events, skipping\n")
    else:
        sys.stdout.write(f"Skipping for event {event.event_name}\n")


if __name__ == "__main__":
    main()
