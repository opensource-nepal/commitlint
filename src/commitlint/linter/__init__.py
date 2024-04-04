"""Main module for commit linters and validators"""

from ._linter import lint_commit_message

__all__ = [
    "lint_commit_message",
]
