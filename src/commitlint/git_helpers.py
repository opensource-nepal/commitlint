"""
This module contains the git related helper functions.
"""
import subprocess
from typing import List

from .exceptions import GitCommitNotFoundException, GitInvalidCommitRangeException


def get_commit_message_of_hash(commit_hash: str) -> str:
    """
    Retrieve the commit message for a given Git commit hash.

    Args:
        commit_hash (str): The Git commit hash for which the commit message is to
            be retrieved.

    Returns:
        str: The commit message associated with the specified commit hash.

    Raises:
        GitCommitNotFoundException: If the specified commit hash is not found
            or if there is an error retrieving the commit message.
    """
    try:
        # Run 'git show --format=%B -s' command to get the commit message
        commit_message = subprocess.check_output(
            ["git", "show", "--format=%B", "-s", commit_hash],
            text=True,
            stderr=subprocess.PIPE,
        ).strip()

        return commit_message
    except subprocess.CalledProcessError:
        raise GitCommitNotFoundException(
            f"Failed to retrieve commit message for hash {commit_hash}"
        ) from None


def get_commit_messages_of_hash_range(
    from_hash: str, to_hash: str = "HEAD"
) -> List[str]:
    """
    Retrieve an array of commit messages for a range of Git commit hashes.

    Note:
        This function will not support initial commit as from_hash.

    Args:
        from_hash (str): The starting Git commit hash.
        to_hash (str, optional): The ending Git commit hash or branch
            (default is "HEAD").

    Returns:
        List[str]: A list of commit messages for the specified commit range.

    Raises:
        GitCommitNotFoundException: If the commit hash of `from_hash` is not found
            or if there is an error retrieving the commit message.

        GitInvalidCommitRangeException: If the commit range of from_hash..to_hash is not
            found or if there is an error retrieving the commit message.
    """
    # as the commit range doesn't support initial commit hash,
    # commit message of `from_hash` is taken separately
    from_commit_message = get_commit_message_of_hash(from_hash)

    try:
        # Runs the below git command:
        # git log --format=%B --reverse FROM_HASH..TO_HASH
        # This outputs the commit messages excluding of FROM_HASH
        delimiter = "========commit-delimiter========"
        hash_range = f"{from_hash}..{to_hash}"

        commit_messages_output = subprocess.check_output(
            ["git", "log", f"--format=%B{delimiter}", "--reverse", hash_range],
            text=True,
            stderr=subprocess.PIPE,
        )
        commit_messages = commit_messages_output.split(f"{delimiter}\n")
        return [from_commit_message] + [
            commit_message.strip()
            for commit_message in commit_messages
            if commit_message.strip()
        ]
    except subprocess.CalledProcessError:
        raise GitInvalidCommitRangeException(
            f"Failed to retrieve commit messages for the range {from_hash} to {to_hash}"
        ) from None
