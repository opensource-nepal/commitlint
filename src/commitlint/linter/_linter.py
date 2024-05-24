"""
This module provides detailed functionality for linting commit messages according
to conventional commit standards.
"""

from typing import List, Tuple

from .. import console
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
    console.verbose("linting commit message:")
    console.verbose(f"----------\n{commit_message}\n----------")

    # perform processing and pre checks
    # removing unnecessary commit comments
    console.verbose("removing comments from the commit message")
    commit_message = remove_comments(commit_message)

    # checking if commit message should be ignored
    console.verbose("checking if the commit message is in ignored list")
    if is_ignored(commit_message):
        console.verbose("commit message ignored, skipping lint")
        return True, []

    # for skip_detail check
    if skip_detail:
        console.verbose("running simple validators for linting")
        return run_validators(
            commit_message,
            validator_classes=[HeaderLengthValidator, SimplePatternValidator],
            fail_fast=True,
        )

    console.verbose("running detailed validators for linting")
    return run_validators(
        commit_message, validator_classes=[HeaderLengthValidator, PatternValidator]
    )
