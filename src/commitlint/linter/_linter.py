"""
This module provides detailed functionality for linting commit messages according
to conventional commit standards.
"""

from typing import List, Tuple

from .. import console
from .utils import is_ignored, remove_comments
from .validators import (
    CommitValidator,
    HeaderLengthValidator,
    PatternValidator,
    SimplePatternValidator,
    run_validators,
)


def lint_commit_message(
    commit_message: str,
    max_header_length: int,
    skip_detail: bool = False,
    disable_max_header_length: bool = False,
    strip_comments: bool = False,
) -> Tuple[bool, List[str]]:
    """
    Lints a commit message.

    Args:
        disable_max_header_length: flag to disable the max header length check
        max_header_length: maximum length of commit message header
        commit_message (str): The commit message to be linted.
        skip_detail (bool, optional): Whether to skip the detailed error linting
            (default is False).
        strip_comments (bool, optional): Whether to remove comments from the
            commit message (default is False).

    Returns:
        Tuple[bool, List[str]]: Returns success as a first element and list of errors
            on the second elements. If success is true, errors will be empty.
    """
    console.verbose("linting commit message:")
    console.verbose(f"----------\n{commit_message}\n----------")

    # perform processing and pre checks
    # removing unnecessary commit comments
    if strip_comments:
        console.verbose("removing comments from the commit message")
        commit_message = remove_comments(commit_message)

    # checking if commit message should be ignored
    console.verbose("checking if the commit message is in ignored list")
    if is_ignored(commit_message):
        console.verbose("commit message ignored, skipping lint")
        return True, []

    validator_instances: List[CommitValidator] = []

    if not disable_max_header_length:
        validator_instances.append(
            HeaderLengthValidator(
                commit_message=commit_message,
                **{"max_header_length": max_header_length},  # type: ignore
            )
        )

    # for skip_detail check
    if skip_detail:
        console.verbose("running simple validators for linting")

        validator_instances.append(
            SimplePatternValidator(commit_message=commit_message)
        )

        return run_validators(
            validator_classes=validator_instances,
            fail_fast=True,
        )

    validator_instances.append(PatternValidator(commit_message=commit_message))

    console.verbose("running detailed validators for linting")
    return run_validators(validator_classes=validator_instances)
