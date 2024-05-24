"""
commitlint (cli): Command-Line Interface for Commitlint

This script provides a command-line interface (CLI) to check if a commit message
follows the conventional commit format using the commitlint module.

Usage:
    1. Check a commit message directly:
        commitlint "Your commit message here"

    2. Check a commit message from a file:
        commitlint --file path/to/your/file.txt

"""

import argparse
import os
import sys
from typing import List

from . import console
from .__version__ import __version__
from .config import config
from .exceptions import CommitlintException
from .git_helpers import get_commit_message_of_hash, get_commit_messages_of_hash_range
from .linter import lint_commit_message
from .linter.utils import remove_comments
from .messages import VALIDATION_FAILED, VALIDATION_SUCCESSFUL


def get_args() -> argparse.Namespace:
    """
    Parse CLI arguments for checking if a commit message.

    Returns:
        argparse.Namespace: The parsed CLI arguments.

    Raises:
        argparse.ArgumentError: If any argument error.
    """
    parser = argparse.ArgumentParser(
        description="Check if a commit message follows the conventional commit format."
    )

    # version
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # for commit message check
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "commit_message", nargs="?", type=str, help="The commit message to be checked"
    )
    group.add_argument(
        "--file", type=str, help="Path to a file containing the commit message"
    )
    group.add_argument("--hash", type=str, help="Commit hash")
    group.add_argument("--from-hash", type=str, help="From commit hash")
    # --to-hash is optional
    parser.add_argument("--to-hash", type=str, help="To commit hash", default="HEAD")

    # feature options
    parser.add_argument(
        "--skip-detail",
        action="store_true",
        help="Skip the detailed error message check",
    )

    output_group = parser.add_mutually_exclusive_group(required=False)
    # --quiet option is optional
    output_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Ignore stdout and stderr",
        default=False,
    )

    # --verbose option is optional
    output_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
        default=False,
    )

    # parsing args
    args = parser.parse_args()

    return args


def _show_errors(
    commit_message: str,
    errors: List[str],
    skip_detail: bool = False,
) -> None:
    """
    Display a formatted error message for a list of errors.

    Args:
        commit_message (str): The commit message to display.
        errors (List[str]): A list of error messages to be displayed.
        skip_detail (bool): Whether to skip the detailed error message.

    """
    error_count = len(errors)
    commit_message = remove_comments(commit_message)

    console.error(f"⧗ Input:\n{commit_message}\n")

    if skip_detail:
        console.error(VALIDATION_FAILED)
        return

    console.error(f"✖ Found {error_count} error(s).")
    for error in errors:
        console.error(f"- {error}")


def _get_commit_message_from_file(filepath: str) -> str:
    """
    Reads and returns the commit message from the specified file.

    Args:
        filepath (str): The path to the file containing the commit message.

    Returns:
        str: The commit message read from the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an issue reading the file.
    """
    abs_filepath = os.path.abspath(filepath)
    console.verbose(f"reading commit message from file {abs_filepath}")
    with open(abs_filepath, encoding="utf-8") as commit_message_file:
        commit_message = commit_message_file.read().strip()
        return commit_message


def _handle_commit_message(commit_message: str, skip_detail: bool) -> None:
    """
    Handles a single commit message, checks its validity, and prints the result.

    Args:
        commit_message (str): The commit message to be handled.
        skip_detail (bool): Whether to skip the detailed error linting.

    Raises:
        SystemExit: If the commit message is invalid.
    """
    success, errors = lint_commit_message(commit_message, skip_detail=skip_detail)

    if success:
        console.success(VALIDATION_SUCCESSFUL)
        return

    _show_errors(commit_message, errors, skip_detail=skip_detail)
    sys.exit(1)


def _handle_multiple_commit_messages(
    commit_messages: List[str], skip_detail: bool
) -> None:
    """
    Handles multiple commit messages, checks their validity, and prints the result.

    Args:
        commit_messages (List[str]): List of commit messages to be handled.
        skip_detail (bool): Whether to skip the detailed error linting.
    Raises:
        SystemExit: If any of the commit messages is invalid.
    """
    has_error = False

    for commit_message in commit_messages:
        success, errors = lint_commit_message(commit_message, skip_detail=skip_detail)
        if success:
            console.verbose("lint success")
            continue

        has_error = True
        _show_errors(commit_message, errors, skip_detail=skip_detail)
        console.error("")

    if has_error:
        sys.exit(1)

    console.success(VALIDATION_SUCCESSFUL)


def main() -> None:
    """
    Main function for cli to check a commit message.
    """
    args = get_args()

    # setting config based on args
    config.quiet = args.quiet
    config.verbose = args.verbose

    console.verbose("starting commitlint")
    try:
        if args.file:
            console.verbose("checking commit from file")
            commit_message = _get_commit_message_from_file(args.file)
            _handle_commit_message(commit_message, skip_detail=args.skip_detail)
        elif args.hash:
            console.verbose("checking commit from hash")
            commit_message = get_commit_message_of_hash(args.hash)
            _handle_commit_message(commit_message, skip_detail=args.skip_detail)
        elif args.from_hash:
            console.verbose("checking commit from hash range")
            commit_messages = get_commit_messages_of_hash_range(
                args.from_hash, args.to_hash
            )
            _handle_multiple_commit_messages(
                commit_messages, skip_detail=args.skip_detail
            )
        else:
            console.verbose("checking commit message")
            commit_message = args.commit_message.strip()
            _handle_commit_message(commit_message, skip_detail=args.skip_detail)
    except CommitlintException as ex:
        console.error(f"{ex}")
        sys.exit(1)


if __name__ == "__main__":
    main()  # pragma: no cover
