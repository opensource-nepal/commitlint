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

from .commitlint import check_commit_message


def main() -> None:
    """
    Main function for cli to check a commit message.
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

    if args.file:
        commit_message_filepath = os.path.abspath(args.file)
        with open(commit_message_filepath, encoding="utf-8") as commit_message_file:
            commit_message = commit_message_file.read().strip().split("\n\n")[0]
    elif args.commit_message:
        commit_message = args.commit_message.strip()
    else:
        parser.error("Please provide either a commit message or a file.")

    check_commit_message(commit_message)


if __name__ == "__main__":
    main()
