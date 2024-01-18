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

from .commitlint import check_commit_message
from .messages import COMMIT_SUCCESSFUL


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
    parser.add_argument(
        "commit_message", nargs="?", type=str, help="The commit message to be checked."
    )
    parser.add_argument(
        "--file", type=str, help="Path to a file containing the commit message."
    )

    args = parser.parse_args()

    if not args.file and not args.commit_message:
        parser.error("Please provide either a commit message or a file.")

    return args


def _show_errors(errors: List[str]) -> None:
    """
    Display a formatted error message for a list of errors.

    Args:
        errors (List[str]): A list of error messages to be displayed.

    Returns:
        None
    """
    sys.stderr.write(f"✖ Found {len(errors)} errors.\n\n")
    for error in errors:
        sys.stderr.write(f"- {error}\n\n")


def main() -> None:
    """
    Main function for cli to check a commit message.
    """
    args = get_args()

    if args.file:
        commit_message_filepath = os.path.abspath(args.file)
        with open(commit_message_filepath, encoding="utf-8") as commit_message_file:
            commit_message = commit_message_file.read().strip()
    else:
        commit_message = args.commit_message.strip()

    success, errors = check_commit_message(commit_message)

    if success:
        sys.stdout.write(f"{COMMIT_SUCCESSFUL}\n")
        sys.exit(0)

    _show_errors(errors)
    sys.exit(1)


if __name__ == "__main__":
    main()
