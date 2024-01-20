"""
This module provides constant messages used in the application for various scenarios.
"""

from .constants import COMMIT_HEADER_MAX_LENGTH

VALIDATION_SUCCESSFUL = "Commit validation: successful!"

CORRECT_OUTPUT_FORMAT = (
    "Correct commit format:\n"
    "---------------------------------------\n"
    "<type>(<optional scope>): <description>\n"
    "---------------------------------------\n"
    "For more details visit "
    "https://www.conventionalcommits.org/en/v1.0.0/"
)
INCORRECT_FORMAT_ERROR = (
    "Commit message does not follow conventional commits format."
    f"\n{CORRECT_OUTPUT_FORMAT}"
)
HEADER_LENGTH_ERROR = (
    f"Header must not be longer than {COMMIT_HEADER_MAX_LENGTH} characters."
)
