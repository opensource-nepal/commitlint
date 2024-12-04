"""Commit message validation module.

This module provides functionality to validate commit messages according to
conventional commit standards.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Union, cast

from .. import console
from ..constants import COMMIT_HEADER_MAX_LENGTH, COMMIT_TYPES
from ..messages import (
    COMMIT_TYPE_INVALID_ERROR,
    COMMIT_TYPE_MISSING_ERROR,
    DESCRIPTION_FULL_STOP_END_ERROR,
    DESCRIPTION_LINE_BREAK_ERROR,
    DESCRIPTION_MISSING_ERROR,
    DESCRIPTION_MULTIPLE_SPACE_START_ERROR,
    DESCRIPTION_NO_LEADING_SPACE_ERROR,
    HEADER_LENGTH_ERROR,
    INCORRECT_FORMAT_ERROR,
    SCOPE_EMPTY_ERROR,
    SCOPE_WHITESPACE_ERROR,
    SPACE_AFTER_COMMIT_TYPE_ERROR,
    SPACE_AFTER_SCOPE_ERROR,
)


class CommitValidator(ABC):
    """Abstract Base validator for commit message."""

    def __init__(self, commit_message: str, **kwargs: Dict[str, Any]) -> None:
        self._commit_message = commit_message
        self._errors: List[str] = []

        # start validation
        self.validate(**kwargs)

    @abstractmethod
    def validate(self, **kwargs: Dict[str, Any]) -> None:
        """Performs the validation."""
        raise NotImplementedError  # pragma: no cover

    def add_error(self, error: str) -> None:
        """Adds an error to the list of errors."""
        self._errors.append(error)

    def is_valid(self) -> bool:
        """Checks if there are any errors."""
        return len(self._errors) == 0

    @property
    def errors(self) -> List[str]:
        """Get the list of errors."""
        return self._errors

    @property
    def commit_message(self) -> str:
        """Gets the commit message."""
        return self._commit_message


class HeaderLengthValidator(CommitValidator):
    """Validator for checking commit header length."""

    def validate(self, **kwargs: Dict[str, Any]) -> None:
        """
        Validates the length of the commit header.

        Returns:
            None
        """
        max_header_length = kwargs.get("max_header_length")

        if max_header_length:
            header_length = cast(int, max_header_length)
        else:
            header_length = COMMIT_HEADER_MAX_LENGTH

        header = self.commit_message.split("\n")[0]

        if len(header) > int(header_length):
            self.add_error(HEADER_LENGTH_ERROR)


class SimplePatternValidator(CommitValidator):
    """
    A simple validator for commit messages using the conventional commit regex
    pattern. This validator doesn't check for the detailed error message.
    """

    _RE_TYPES = "|".join(COMMIT_TYPES)
    COMMIT_PATTERN = (
        r"(?s)"  # To explicitly make . match new line
        rf"(?P<type>{_RE_TYPES})"
        r"(?P<scope>\(\S+\))?!?:"
        r"(?: (?P<description>[^\s][^\n\r]+[^\.]))"
        r"((\n\n(?P<body>.*))|(\s*))?$"
    )

    def validate(self, **kwargs: Dict[str, Any]) -> None:
        """
        Validates the commit message using the regex pattern.

        Returns:
            None
        """
        pattern_match = re.match(self.COMMIT_PATTERN, self.commit_message)
        if pattern_match is None:
            self.add_error(INCORRECT_FORMAT_ERROR)


class PatternValidator(CommitValidator):
    """
    A Detailed validator for commit message using the conventional commit regex
    pattern. This validator checks for the detailed error message.
    """

    COMMIT_PATTERN = (
        r"(?s)"  # To explicitly make . match new line
        r"(?P<type>\w+\s*)?"
        r"(?:\((?P<scope>[^\)]*)\)(?P<space_after_scope>\s*))?"
        r"!?(?P<colon>:\s?)?"
        r"(?:(?P<description>[^\n\r]+))?"
        r"(?P<body_separation>\n?\n?)"
        r"(((?P<body>.*))|(\s*))?$"
    )

    def validate(self, **kwargs: Dict[str, Any]) -> None:
        """
        Validates the commit message using the regex pattern.

        Returns:
            None
        """

        # Matching commit message with the commit pattern
        pattern_match = re.match(self.COMMIT_PATTERN, self.commit_message)
        if pattern_match is None or pattern_match.group("colon") is None:
            self.add_error(INCORRECT_FORMAT_ERROR)
            return

        self.re_match = pattern_match

        validators = [
            self.validate_commit_type,
            self.validate_commit_type_no_space_after,
            self.validate_scope,
            self.validate_scope_no_space_after,
            self.validate_description,
            self.validate_description_no_multiple_whitespace,
            self.validate_description_no_line_break,
            self.validate_description_no_full_stop_at_end,
        ]

        for validator in validators:
            error = validator()
            if error:
                self.add_error(error)

    def validate_commit_type(self) -> Union[None, str]:
        """
        Validates the commit type.

        Returns:
            Union[None, str]: If the commit type is valid, returns None; otherwise,
                returns an error message.
        """
        commit_type = self.re_match.group("type")
        if commit_type is None:
            return COMMIT_TYPE_MISSING_ERROR

        commit_type = commit_type.strip()
        if commit_type not in COMMIT_TYPES:
            return COMMIT_TYPE_INVALID_ERROR % commit_type

        return None

    def validate_commit_type_no_space_after(self) -> Union[None, str]:
        """
        Validates that there is no space after the commit type.

        Returns:
            Union[None, str]: If there is no space after the commit type, returns
                None; otherwise, returns an error message.
        """
        commit_type = self.re_match.group("type")

        if commit_type and commit_type.endswith(" "):
            commit_type = commit_type.strip()
            return SPACE_AFTER_COMMIT_TYPE_ERROR

        return None

    def validate_scope(self) -> Union[None, str]:
        """
        Validates the commit scope.

        Returns:
            Union[None, str]: If the commit scope is valid, returns None; otherwise,
                returns an error message.
        """
        scope = self.re_match.group("scope")
        if scope is not None:
            if scope == "":
                return SCOPE_EMPTY_ERROR

            if " " in scope:
                return SCOPE_WHITESPACE_ERROR

        return None

    def validate_scope_no_space_after(self) -> Union[None, str]:
        """
        Validates that there is no space after the commit scope.

        Returns:
            Union[None, str]: If there is no space after the commit scope, returns
                None; otherwise, returns an error message.
        """
        space_after_scope = self.re_match.group("space_after_scope")
        if space_after_scope and " " in space_after_scope:
            return SPACE_AFTER_SCOPE_ERROR

        return None

    def validate_description(self) -> Union[None, str]:
        """
        Validates the commit description.

        Returns:
            Union[None, str]: If the description is valid, returns None; otherwise,
                returns an error message.
        """
        if not self.re_match.group("description"):
            return DESCRIPTION_MISSING_ERROR

        if not self.re_match.group("colon").endswith(" "):
            return DESCRIPTION_NO_LEADING_SPACE_ERROR

        return None

    def validate_description_no_multiple_whitespace(
        self,
    ) -> Union[None, str]:
        """
        Validates that there are no multiple whitespace characters at the beginning of
          the description.

        Returns:
            Union[None, str]: If the description has no multiple whitespace characters
                at the beginning, returns None; otherwise, returns an error message.
        """
        if self.re_match.group("description") and self.re_match.group(
            "description"
        ).startswith(" "):
            return DESCRIPTION_MULTIPLE_SPACE_START_ERROR

        return None

    def validate_description_no_line_break(
        self,
    ) -> Union[None, str]:
        """
        Validates that the description has no line break at the end.

        Returns:
            Union[None, str]: If there is no line break at the end of the
                description, returns None; otherwise, returns an error message.
        """
        if self.re_match.group("body_separation") == "\n" and self.re_match.group(
            "body"
        ):
            return DESCRIPTION_LINE_BREAK_ERROR

        return None

    def validate_description_no_full_stop_at_end(
        self,
    ) -> Union[None, str]:
        """
        Validates that the description doesn't have full stop at the end.

        Returns:
            Union[None, str]: If there is no full stop at the end of the description,
                returns None; otherwise, returns an error message.
        """
        if self.re_match.group("description") and self.re_match.group(
            "description"
        ).strip().endswith("."):
            return DESCRIPTION_FULL_STOP_END_ERROR

        return None


def run_validators(
    validator_classes: List[CommitValidator],
    fail_fast: bool = False,
) -> Tuple[bool, List[str]]:
    """Runs the provided validators for the commit message.

    Args:
        commit_message (str): The commit message to validate.
        validator_classes (List[Type[CommitValidator]]): List of validator classes to
            run.
        fail_fast (bool, optional): Return early if one validator fails. Defaults to
            False.

    Returns:
        Tuple[bool, List[str]]: Returns success as the first element and a list of
            errors as the second element. If success is True, errors will be empty.
    """

    success = True
    errors: List[str] = []

    for validator_instance in validator_classes:
        console.verbose(f"running validator {validator_instance.__class__.__name__}")
        if not validator_instance.is_valid():
            console.verbose(
                f"{validator_instance.__class__.__name__}: validation failed"
            )
            if fail_fast:
                console.verbose(f"fail_fast: {fail_fast}, skipping further validations")
                # returning immediately if any error occurs.
                return False, validator_instance.errors

            success = False
            errors.extend(validator_instance.errors)

    return success, errors
