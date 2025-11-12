"""
Contains the utility methods for linters.
"""

import re
from typing import List

from ..constants import IGNORE_COMMIT_PATTERNS


def is_ignored(commit_message: str) -> bool:
    """
    Checks if a commit message should be ignored.

    Some commit messages like merge, revert, auto merge, etc is ignored
    from linting.

    Args:
        commit_message (str): The commit message to check.

    Returns:
        bool: True if the commit message should be ignored, False otherwise.
    """
    commit_first_line = commit_message.splitlines()[0]
    return bool(re.match(IGNORE_COMMIT_PATTERNS, commit_first_line))


def remove_comments(commit_message: str) -> str:
    """Removes comments from the commit message.

    Args:
        commit_message(str): The commit message to remove comments.

    Returns:
        str: The commit message without comments.
    """
    commit_message = remove_diff_from_commit_message(commit_message)

    lines: List[str] = []
    for line in commit_message.split("\n"):
        if not line.startswith("#"):
            lines.append(line)

    return "\n".join(lines)


def remove_diff_from_commit_message(commit_message: str) -> str:
    """Removes commit diff from the commit message.

    For `git commit --verbose`, removing the diff generated message,
    for example:

    ```bash
    ...
    # ------------------------ >8 ------------------------
    # Do not modify or remove the line above.
    # Everything below it will be ignored.
    diff --git a/... b/...
    ...
    ```

    Args:
        commit_message (str): The commit message to remove diff.

    Returns:
        str: The commit message without diff.
    """
    verbose_commit_separator = "# ------------------------ >8 ------------------------"
    return commit_message.split(verbose_commit_separator)[0].strip()
