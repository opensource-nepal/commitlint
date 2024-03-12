"""
This module provides detailed functionality for linting commit messages according
to conventional commit standards.
"""

from typing import List, Tuple

from .utils import is_ignored, remove_comments
from .validators import (
    HeaderLengthValidator,
    PatternValidator,
    SimplePatternValidator,
    run_validators,
)


def lint_commit_message(
    commit_message: str, skip_detail: bool = False
) -> Tuple[bool, List[str]]:
    """
    Lints a commit message.

    Args:
        commit_message (str): The commit message to be linted.
        skip_detail (bool, optional): Whether to skip the detailed error linting
            (default is False).

    Returns:
        Tuple[bool, List[str]]: Returns success as a first element and list of errors
            on the second elements. If success is true, errors will be empty.
    """

    # perform processing and pre checks
    # removing unnecessary commit comments
    commit_message = remove_comments(commit_message)

    # checking if commit message should be ignored
    if is_ignored(commit_message):
        return True, []

    # for skip_detail check
    if skip_detail:
        return run_validators(
            commit_message,
            validator_classes=[HeaderLengthValidator, SimplePatternValidator],
            fail_fast=True,
        )

    return run_validators(
        commit_message, validator_classes=[HeaderLengthValidator, PatternValidator]
    )
