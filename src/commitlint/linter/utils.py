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
    return bool(re.match(IGNORE_COMMIT_PATTERNS, commit_message))


def remove_comments(msg: str) -> str:
    """Removes comments from the commit message.

    For `git commit --verbose`, excluding the diff generated message,
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
        msg(str): The commit message to remove comments.

    Returns:
        str: The commit message without comments.
    """

    lines: List[str] = []
    for line in msg.split("\n"):
        if "# ------------------------ >8 ------------------------" in line:
            # ignoring all the verbose message below this line
            break
        if not line.startswith("#"):
            lines.append(line)

    return "\n".join(lines)
