"""This module contains source for commitlint"""
import re
import sys

COMMIT_MAX_LENGTH = 72


def is_conventional_commit(commit_message: str) -> bool:
    """
    Checks if a commit message follows the conventional commit format.

    Args:
        commit_message (str): The commit message to be checked.

    Returns:
        bool: True if the commit message follows the conventional commit format,
              False otherwise.
    """
    pattern = re.compile(r"^(\w+)(\([^\)]+\))?: .+")
    return bool(pattern.match(commit_message))


def is_valid_length(commit_message: str, max_length: int) -> bool:
    """
    Checks if a commit message has a valid length.

    Args:
        commit_message (str): The commit message to be checked.
        max_length (int): The maximum allowed length for the commit message.

    Returns:
        bool: True if the commit message length is valid, False otherwise.
    """
    return len(commit_message) <= max_length


def check_commit_message(commit_message: str) -> None:
    """
    Check the validity of a commit message.

    Args:
        commit_message (str): The commit message to be validated.

    Raises:
        SystemExit: Exits the program with status code 1 if the commit message
                    violates length or conventional commit format rules.

    Returns:
        None: This function does not return any value; it either exits or
              continues based on the validity of the commit message.
    """
    if not is_valid_length(commit_message, max_length=COMMIT_MAX_LENGTH):
        sys.stderr.write(
            "Commit message is too long. "
            f"Max length is {COMMIT_MAX_LENGTH} characters.\n"
        )
        sys.exit(1)

    if not is_conventional_commit(commit_message):
        sys.stderr.write("Commit message does not follow conventional commit format.\n")
        sys.exit(1)
