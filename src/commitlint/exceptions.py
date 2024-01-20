"""Custom exceptions module for Commitlint."""


class CommitlintException(Exception):
    """Base exception for Commitlint."""


class GitException(CommitlintException):
    """Exceptions related to Git."""


class GitCommitNotFoundException(GitException):
    """Exception raised when a Git commit could not be retrieved."""


class GitInvalidCommitRangeException(GitException):
    """Exception raised when an invalid commit range was provided."""
