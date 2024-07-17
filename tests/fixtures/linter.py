# type: ignore
# pylint: disable=all
from typing import List, Tuple

from commitlint.constants import COMMIT_HEADER_MAX_LENGTH
from commitlint.messages import (
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

# LINTER_FIXTURE_PARAMS contains test data for the function `lint_commit_message`. The
# purpose of creating this data is to ensure consistent results for both detailed and
# simple commit message linting processes.
#
# The data consists of tuples, each representing a test case with the following
# structure:
# (commit_message, expected_success, expected_errors)
#
# - commit_message: The commit message to be tested.
# - expected_success: A boolean indicating whether the commit message is expected to
#   pass or fail the linting.
# - expected_errors: A list of error messages expected for detailed linting (not for
#       simple linting).
LINTER_FIXTURE_PARAMS: Tuple[Tuple[str, bool, List[str], List[str]], ...] = (
    # success
    ("feat: add new feature", True, []),
    ("feat: add new feature\n\nthis is body", True, []),
    (
        "feat: add new feature\n\nthis is body" + "a" * COMMIT_HEADER_MAX_LENGTH,
        True,
        [],
    ),
    ("feat: add new feature\n\nthis is body\n\ntest", True, []),
    ("feat: add new feature\n", True, []),
    ("build(deps-dev): bump @babel/traverse from 7.22.17 to 7.24.0", True, []),
    ("feat!: breaking feature", True, []),
    # ignored commits (success)
    ("Merge pull request #123", True, []),
    ("Bump urllib3 from 1.26.5 to 1.26.17", True, []),
    ("Bump github.com/ollama/ollama from 0.1.48 to 0.2.0", True, []),
    ("bump @babel/traverse from 7.22.17 to 7.24.0", True, []),
    (
        "Bump github.com/ollama/ollama from 0.1.48 to 0.2.0\n\nthis is a commit body",
        True,
        [],
    ),
    # incorrect format check
    ("feat add new feature", False, [INCORRECT_FORMAT_ERROR]),
    # header length check
    ("feat: " + "a" * (COMMIT_HEADER_MAX_LENGTH - 1), False, [HEADER_LENGTH_ERROR]),
    ("feat: " + "a" * (COMMIT_HEADER_MAX_LENGTH - 1), False, [HEADER_LENGTH_ERROR]),
    (
        "Test " + "a" * (COMMIT_HEADER_MAX_LENGTH + 1),
        False,
        [HEADER_LENGTH_ERROR, INCORRECT_FORMAT_ERROR],
    ),
    # commit type check
    (": add new feature", False, [COMMIT_TYPE_MISSING_ERROR]),
    ("(invalid): add new feature", False, [COMMIT_TYPE_MISSING_ERROR]),
    ("invalid: add new feature", False, [COMMIT_TYPE_INVALID_ERROR % "invalid"]),
    ("feat (test): add new feature", False, [SPACE_AFTER_COMMIT_TYPE_ERROR]),
    (
        "invalid (test): add new feature",
        False,
        [COMMIT_TYPE_INVALID_ERROR % "invalid", SPACE_AFTER_COMMIT_TYPE_ERROR],
    ),
    # scope check
    ("feat(): add new feature", False, [SCOPE_EMPTY_ERROR]),
    ("feat( ): add new feature", False, [SCOPE_WHITESPACE_ERROR]),
    ("feat(hello world): add new feature", False, [SCOPE_WHITESPACE_ERROR]),
    ("feat(test) : add new feature", False, [SPACE_AFTER_SCOPE_ERROR]),
    (
        "feat (test) : add new feature",
        False,
        [SPACE_AFTER_COMMIT_TYPE_ERROR, SPACE_AFTER_SCOPE_ERROR],
    ),
    # description check
    ("feat:add new feature", False, [DESCRIPTION_NO_LEADING_SPACE_ERROR]),
    ("feat:  add new feature", False, [DESCRIPTION_MULTIPLE_SPACE_START_ERROR]),
    ("feat: add new feature\nhello baby", False, [DESCRIPTION_LINE_BREAK_ERROR]),
    ("feat(test):", False, [DESCRIPTION_MISSING_ERROR]),
    ("feat(test): ", False, [DESCRIPTION_MISSING_ERROR]),
    ("feat(test): add new feature.", False, [DESCRIPTION_FULL_STOP_END_ERROR]),
)
