# type: ignore
# pylint: disable=all

import pytest

from commitlint.linter.utils import is_ignored


@pytest.mark.parametrize(
    "commit_message, expected_result",
    [
        ("Merge pull request #123", True),
        ("Merge feature-branch into production", True),
        ("Merge branch hotfix-123", True),
        ("Merge tag release-v2.0.1", True),
        ('Revert "Undo last commit"', True),
        ("revert Fix-Typo", True),
        ("Merged bugfix-789 in master", True),
        ("Merged PR #987: Update documentation", True),
        ("Merge remote-tracking branch upstream/develop", True),
        ("Automatic merge from CI/CD", True),
        ("Auto-merged feature-branch into staging", True),
        ("Merge tag v3.5.0", True),
        ("Merge pull request #456: Feature XYZ", True),
        ('Revert "Apply security patch"', True),
        ("Merged PR #321: Bugfix - Resolve issue with login", True),
        ("Merge my feature", False),
        ("Add new feature", False),
        ("feat: this is conventional commit format", False),
        ("Bump urllib3 from 1.26.5 to 1.26.17", True),
        ("bump @babel/traverse from 7.22.17 to 7.24.0", True),
        ("Bump feature1 from feature2", False),
    ],
)
def test__is_ignored(commit_message, expected_result):
    result = is_ignored(commit_message)
    assert result == expected_result
