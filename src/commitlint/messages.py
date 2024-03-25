"""
This module provides constant messages used in the application for various scenarios.
"""

from .constants import COMMIT_HEADER_MAX_LENGTH, COMMIT_TYPES

VALIDATION_SUCCESSFUL = "Commit validation: successful!"
VALIDATION_FAILED = "Commit validation: failed!"

INCORRECT_FORMAT_ERROR = (
    "Commit message does not follow the Conventional Commits format."
)
HEADER_LENGTH_ERROR = (
    f"Header length cannot exceed {COMMIT_HEADER_MAX_LENGTH} characters."
)
COMMIT_TYPE_MISSING_ERROR = "Type is missing."
COMMIT_TYPE_INVALID_ERROR = (
    f"Invalid type '%s'. Type must be one of: {', '.join(COMMIT_TYPES)}."
)
SPACE_AFTER_COMMIT_TYPE_ERROR = "There cannot be a space after the type."
SCOPE_EMPTY_ERROR = "Scope cannot be empty."
SPACE_AFTER_SCOPE_ERROR = "There cannot be a space after the scope."
SCOPE_WHITESPACE_ERROR = "Scope cannot contain spaces."
DESCRIPTION_NO_LEADING_SPACE_ERROR = "Description must have a leading space."
DESCRIPTION_MULTIPLE_SPACE_START_ERROR = (
    "Description cannot start with multiple spaces."
)
DESCRIPTION_LINE_BREAK_ERROR = "Description cannot contain line breaks."
DESCRIPTION_MISSING_ERROR = "Description is missing."
DESCRIPTION_FULL_STOP_END_ERROR = "Description cannot end with full stop."
