"""
This script contains actions to be taken based on GitHub events,
specifically for push and pull_request events.
"""
import subprocess
import sys

from event import GithubEvent

EVENT_PUSH = "push"
EVENT_PULL_REQUEST = "pull_request"


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
                "python",
                "-m",
                "src.commitlint.cli",
                "--from-hash",
                from_hash,
                "--to-hash",
                to_hash,
            ],
            text=True,
        ).strip()
        sys.stdout.write(f"{output}\n")
    except subprocess.CalledProcessError:
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
