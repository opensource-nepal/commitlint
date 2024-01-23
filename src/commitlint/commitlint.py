"""
This module provides functionality for validating commit messages according
to conventional commit standards.

Usage:
------

```python
from commitlint import check_commit_message

commit_message = "feat(module): add module documentation"
success, errors = check_commit_message(commit_message)
```
"""
import re
from typing import List, Tuple

from .constants import COMMIT_HEADER_MAX_LENGTH
from .messages import HEADER_LENGTH_ERROR, INCORRECT_FORMAT_ERROR

CONVENTIONAL_COMMIT_PATTERN = (
    r"(?s)"  # To explicitly make . match new line
    r"(?P<type>build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
    r"(?P<scope>\(\S+\))?!?:"
    r"(?: (?P<description>[^\n\r]+))"
    r"((\n\n(?P<body>.*))|(\s*))?$"
)

IGNORED_PATTERN = (
    r"^((Merge pull request)|(Merge (.*?) into (.*?)|(Merge branch (.*?)))(?:\r?\n)*$)|"
    r"^(Merge tag (.*?))(?:\r?\n)*$|"
    r"^(R|r)evert (.*)|"
    r"^(Merged (.*?)(in|into) (.*)|Merged PR (.*): (.*))$|"
    r"^Merge remote-tracking branch(\s*)(.*)$|"
    r"^Automatic merge(.*)$|"
    r"^Auto-merged (.*?) into (.*)$"
)


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
    return bool(re.match(IGNORED_PATTERN, commit_message))


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


def check_commit_message(commit_message: str) -> Tuple[bool, List[str]]:
    """
    Checks the validity of a commit message. Returns success and error list.

    Args:
        commit_message (str): The commit message to be validated.

    Returns:
        Tuple[bool, List[str]]: Returns success as a first element and list
        of errors on the second elements. If success is true, errors will be
        empty.
    """
    # default values
    success = True
    errors: List[str] = []

    # removing unnecessary commit comments
    commit_message = remove_comments(commit_message)

    # checking if commit message should be ignored
    if is_ignored(commit_message):
        return success, errors

    # checking the length of header
    header = commit_message.split("\n").pop()
    if len(header) > COMMIT_HEADER_MAX_LENGTH:
        success = False
        errors.append(HEADER_LENGTH_ERROR)

    # matching commit message with the commit pattern
    pattern_match = re.match(CONVENTIONAL_COMMIT_PATTERN, commit_message)
    if pattern_match is None:
        success = False
        errors.append(INCORRECT_FORMAT_ERROR)

    return success, errors
